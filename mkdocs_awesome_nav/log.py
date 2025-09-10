from pathlib import PurePosixPath
from typing import Optional, Literal

from mkdocs.config import config_options, Config
from mkdocs.plugins import get_plugin_logger

_logger = get_plugin_logger("awesome-nav")


LogLevel = Literal["info", "warning", "error"]


def _log_level_choice():
    return config_options.Optional(config_options.Choice[LogLevel](["info", "warning", "error"]))


class LogLevelsConfig(Config):
    nav_override = _log_level_choice()
    root_title = _log_level_choice()
    root_hide = _log_level_choice()
    no_matches = _log_level_choice()


levels = LogLevelsConfig()


def format_log_message(message: str, path: Optional[PurePosixPath | str] = None) -> str:
    if path is None:
        return message
    return f"{message} [{path}]"


def write(level: LogLevel, message: str, path: Optional[PurePosixPath | str] = None):
    formatted = format_log_message(message, path)
    match level:
        case "info":
            _logger.info(formatted)
        case "warning":
            _logger.warning(formatted)
        case "error":
            _logger.error(formatted)
