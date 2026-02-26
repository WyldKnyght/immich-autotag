from __future__ import annotations

from immich_autotag.config.manager import ConfigManager
from immich_autotag.logging.init import initialize_logging


def init_config_and_logging() -> ConfigManager:
    from immich_autotag.logging.levels import LogLevel
    from immich_autotag.logging.utils import log

    log("ConfigManager initialized successfully", level=LogLevel.INFO)
    initialize_logging()
    from immich_autotag.statistics.statistics_manager import StatisticsManager

    StatisticsManager.get_instance().save()

    from immich_autotag.utils.user_help import init_config_and_print_welcome

    manager = init_config_and_print_welcome()

    return manager
