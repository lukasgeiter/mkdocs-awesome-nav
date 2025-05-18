from pathlib import PurePosixPath
from typing import Optional

from mkdocs.plugins import get_plugin_logger

_logger = get_plugin_logger("awesome-nav")


def format_log_message(message: str, path: Optional[PurePosixPath | str] = None) -> str:
    if path is None:
        return message
    return f"{message} [{path}]"


def log_info(message: str, path: Optional[PurePosixPath | str] = None) -> None:
    _logger.info(format_log_message(message, path))


def log_warning(message: str, path: Optional[PurePosixPath | str] = None) -> None:
    _logger.warning(format_log_message(message, path))


def log_error(message: str, path: Optional[PurePosixPath | str] = None) -> None:
    _logger.error(format_log_message(message, path))
