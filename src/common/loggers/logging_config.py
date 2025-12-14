import logging
import json
from enum import Enum

from ..config import settings


class LogFormat(Enum):
    GREY = "\x1b[37;20m"  # Debug
    BLUE = "\x1b[34;20m"  # Info
    GREEN = "\x1b[32;20m"  # Alternative for Info
    YELLOW = "\x1b[33;20m"  # Warning
    RED = "\x1b[31;20m"  # Error
    BOLD_RED = "\x1b[31;1m"  # Critical
    RESET = "\x1b[0m"


# Mapping log levels to colors using a dictionary
LEVEL_COLOR_MAP = {
    logging.DEBUG: LogFormat.GREY.value,  # Debug: Grey
    logging.INFO: LogFormat.BLUE.value,  # Info: Blue
    logging.WARNING: LogFormat.YELLOW.value,  # Warning: Yellow
    logging.ERROR: LogFormat.RED.value,  # Error: Red
    logging.CRITICAL: LogFormat.BOLD_RED.value,  # Critical: Bold Red
}


class JsonFormatter(logging.Formatter):
    def get_color(self, level):
        # Get the color from the mapping, default to reset if level is not found
        return LEVEL_COLOR_MAP.get(level, LogFormat.RESET.value)

    def format(self, record):
        color = self.get_color(record.levelno)
        log_entry = {
            "timestamp": self.formatTime(record),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return color + json.dumps(log_entry) + LogFormat.RESET.value


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        # Set logging level based on the DEBUG setting
        if settings.DEBUG:  # Assuming settings.DEBUG is a boolean
            self.setLevel(logging.DEBUG)  # Enable DEBUG logging
        else:
            self.setLevel(logging.WARNING)  # Default to WARNING for production

        self.propagate = False

        # Create a console handler
        handler = logging.StreamHandler()

        # Set handler level to match logger's level
        handler.setLevel(self.level)

        # Use the custom JSON formatter
        formatter = JsonFormatter()
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.addHandler(handler)
