"""
Health check logic for temporary albums.
"""

from typing import TYPE_CHECKING, NamedTuple

from typeguard import typechecked

from immich_autotag.albums.album.album_response_wrapper import AlbumResponseWrapper

if TYPE_CHECKING:
    pass

import datetime
import enum


# Modes for date source logic in temporary album health check
class TemporaryAlbumDateCheckMode(enum.Enum):
    ALBUM = "album"  # Trust album-provided dates
    ASSETS = "assets"  # Trust asset-calculated dates
    DEVELOPER = "developer"  # Compare both and raise if mismatch


class DateRange(NamedTuple):
    """Represents a range between two dates."""

    min_date: datetime.datetime
    max_date: datetime.datetime


def _ensure_datetime(date_value: datetime.datetime | str) -> datetime.datetime:
    """
    Converts string dates to datetime objects.
    Assumes input is not None (caller must check before calling).
    """
    if isinstance(date_value, str):
        return datetime.datetime.fromisoformat(date_value)
    return date_value


def _get_asset_dates(
    album_wrapper: AlbumResponseWrapper,
) -> DateRange | None:
    """
    Loads assets from album and extracts min/max dates.
    Returns DateRange with (min_date, max_date) or None if insufficient dates found.
    """
    from immich_autotag.context.immich_context import ImmichContext

    context = ImmichContext.get_default_instance()
    assets = album_wrapper.wrapped_assets(context)

    if not assets or len(assets) < 2:
        return None

    dates = [date for date in (a.get_best_date() for a in assets) if date is not None]
    if len(dates) < 2:
        return None

    return DateRange(min_date=min(dates), max_date=max(dates))


def _get_date_range_days(
    min_date: datetime.datetime, max_date: datetime.datetime
) -> int:
    """Calculates the number of days between two datetime objects."""
    return (max_date - min_date).days


@typechecked
def is_temporary_album_healthy(
    album_wrapper: AlbumResponseWrapper,
    max_days_apart: int = 30,
    date_check_mode: "TemporaryAlbumDateCheckMode" = TemporaryAlbumDateCheckMode.ALBUM,
) -> bool:
    """
    Returns True if all assets in the temporary album are within max_days_apart of each other.
    Optimized: ALBUM mode avoids loading assets if album dates are available.
    """
    album_min_date = album_wrapper.get_start_date()
    album_max_date = album_wrapper.get_end_date()

    if date_check_mode == TemporaryAlbumDateCheckMode.ALBUM:
        # Fast path: trust album-provided dates if available
        if album_min_date and album_max_date:
            min_dt = _ensure_datetime(album_min_date)
            max_dt = _ensure_datetime(album_max_date)
            delta = _get_date_range_days(min_dt, max_dt)
            return delta <= max_days_apart

        # Slow fallback: load assets only if album dates are missing
        asset_dates = _get_asset_dates(album_wrapper)
        if asset_dates is None:
            return True
        delta = _get_date_range_days(asset_dates.min_date, asset_dates.max_date)
        return delta <= max_days_apart

    elif date_check_mode == TemporaryAlbumDateCheckMode.ASSETS:
        # Always use asset-calculated dates
        asset_dates = _get_asset_dates(album_wrapper)
        if asset_dates is None:
            return True
        delta = _get_date_range_days(asset_dates.min_date, asset_dates.max_date)
        return delta <= max_days_apart

    elif date_check_mode == TemporaryAlbumDateCheckMode.DEVELOPER:
        # Compare both sources, allow 1 day diff, raise if mismatch
        asset_dates = _get_asset_dates(album_wrapper)
        if asset_dates is None:
            return True

        if album_min_date and album_max_date:
            album_min_dt = _ensure_datetime(album_min_date)
            album_max_dt = _ensure_datetime(album_max_date)

            min_diff = abs((asset_dates.min_date.date() - album_min_dt.date()).days)
            max_diff = abs((asset_dates.max_date.date() - album_max_dt.date()).days)

            if min_diff > 1 or max_diff > 1:
                raise RuntimeError(
                    f"Temporary album date mismatch: calculated min/max {asset_dates.min_date.date()} - {asset_dates.max_date.date()} "
                    f"vs album-provided {album_min_dt.date()} - {album_max_dt.date()} (allowed diff: 1 day)"
                )
            delta = _get_date_range_days(album_min_dt, album_max_dt)
        else:
            delta = _get_date_range_days(asset_dates.min_date, asset_dates.max_date)

        return delta <= max_days_apart

    else:
        raise ValueError(f"Unknown TemporaryAlbumDateCheckMode: {date_check_mode}")


@typechecked
def cleanup_unhealthy_album(
    album_wrapper: AlbumResponseWrapper,
):
    """
    Deletes the album if it is unhealthy.
    """
    from immich_autotag.albums.albums.album_collection_wrapper import (
        AlbumCollectionWrapper,
    )

    album_name = album_wrapper.get_album_name()
    collection = AlbumCollectionWrapper.get_instance()
    from immich_autotag.context.immich_client_wrapper import ImmichClientWrapper

    client = ImmichClientWrapper.get_default_instance()

    collection.delete_album(
        wrapper=album_wrapper,
        client=client.get_client(),
        reason="Unhealthy temporary album deleted automatically",
    )
    print(f"Deleted unhealthy album: {album_name}")
