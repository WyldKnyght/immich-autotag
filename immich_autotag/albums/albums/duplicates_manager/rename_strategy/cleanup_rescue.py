"""
Album Cleanup Rescue Operation

This module implements the one-time rescue operation to fix corrupted album names and merge duplicates, as described in the maintenance plan.
Activation is controlled by a config flag. When enabled, only this process runs.
"""

import re

from immich_autotag.albums.albums.album_collection_wrapper import AlbumCollectionWrapper
from immich_autotag.albums.albums.duplicates_manager.rename_strategy.constants import (
    RENAMED_BY_AUTOTAG_DUPLICATE_USER_ALBUM_SUFFIX,
)
from immich_autotag.report.modification_entries_list import ModificationEntriesList

RENAMED_PATTERN = re.compile(
    rf"({re.escape(RENAMED_BY_AUTOTAG_DUPLICATE_USER_ALBUM_SUFFIX)})+"
)


def _restore_original_name(name: str) -> str:
    """
    Removes repeated renaming suffixes from album names.
    Example: '2025-11-22-original_name__RENAMED_BY_AUTOTAG_DUPLICATE_USER_ALBUM__RENAMED_BY_AUTOTAG_DUPLICATE_USER_ALBUM'
    becomes '2025-11-22-original_name'
    """
    return RENAMED_PATTERN.split(name)[0]


def cleanup_album_names(
    album_collection: AlbumCollectionWrapper,
) -> ModificationEntriesList:
    """
    Rescue function for catastrophic album renaming/duplication bugs.

    Context:
    During development, a bug in the duplicate album handling logic caused the renaming suffix
    (e.g., '__RENAMED_BY_AUTOTAG_DUPLICATE_USER_ALBUM__') to be appended multiple times to album names,
    or even to all albums, not just true duplicates. This led to situations where many albums had
    corrupted names with repeated or unnecessary suffixes, and some albums were no longer properly deduplicated.

    Purpose:
    This function scans all albums, detects those with corrupted names (multiple or spurious renaming suffixes),
    and attempts to restore their original names by stripping all suffixes. It also merges duplicates as needed.
    The goal is to recover from a catastrophic state caused by the faulty renaming/duplication strategy and
    leave the album collection in a consistent, deduplicated state.

    Usage:
    Should be run as a one-time maintenance operation when such corruption is detected. Controlled by config flag.
    """

    # Get client and report
    client = album_collection.get_client()
    tag_mod_report = album_collection.get_modification_report()

    # Iterate over all non-deleted albums
    from immich_autotag.report.modification_entries_list import ModificationEntriesList

    modifications = ModificationEntriesList()
    for album in album_collection.get_albums():
        original_name = _restore_original_name(album.get_album_name())
        current_name = album.get_album_name()
        if original_name and original_name != current_name:
            mod_entry = album.rename_album(
                new_name=original_name,
                client=client,
                modification_report=tag_mod_report,
            )
            if mod_entry is not None:
                modifications.append(mod_entry)
    return modifications


# Entry point for rescue operation


def run_album_cleanup_rescue() -> ModificationEntriesList:
    """
    Runs the album cleanup rescue operation and returns all modification entries performed.
    """
    album_collection = AlbumCollectionWrapper.get_instance()
    modifications = cleanup_album_names(album_collection)
    # If you want to persist changes, ensure the collection is saved via the appropriate method if available
    return modifications


def report_album_cleanup_modifications(
    modifications: "ModificationEntriesList",
) -> None:
    """
    Prints a summary of the modifications performed during album cleanup rescue.
    """
    if modifications and len(modifications.entries()) > 0:
        print(
            f"[MAINTENANCE] Rescue operation completed. {len(modifications.entries())} album(s) renamed."
        )
        for entry in modifications.entries():
            print(f"  - {entry}")
    else:
        print(
            "[MAINTENANCE] Rescue operation completed. No album renames were necessary."
        )
