import logging

from .logging_config import Logger

# Set the custom logger class as the default logger class
logging.setLoggerClass(Logger)


logger = logging.getLogger("app")
strands_logger = logging.getLogger("strands")

__all__ = ["logger", "strands_logger"]
