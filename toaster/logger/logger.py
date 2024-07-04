"""Module "logger".

File:
    logger.py

About:
    his file defines a Singleton Logger class that
    provides logging functionalities for the application.
    It initializes a logger with a specified service name
    from the configuration and sets up a stream handler
    with a formatter obtained from the formatters module.
"""

import logging
import config
from typing import TypeVar
from .formatters import get_formatter


T = TypeVar("T", bound="Logger")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    """Initializes the Logger with instance.

    Description:
        Singleton Logger class that provides logging functionalities.
        (like stream handler using a colored formatter for output.)

    Attributes:
        logger (logging.Logger): Logger instance initialized with the service name from config..
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(config.SERVICE_NAME)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(get_formatter(colored=True))

        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, text: str) -> None:
        """Logs an informational message.

        Args:
            text (str): Message text to log.
        """

        self.logger.info(text)

    def debug(self, text: str) -> None:
        """Logs a debug message.

        Args:
            text (str): Message text to log.
        """

        self.logger.debug(text)

    def warning(self, text: str) -> None:
        """Logs a warning message.

        Args:
            text (str): Message text to log.
        """

        self.logger.warning(text)

    def error(self, text: str) -> None:
        """Logs an error message.

        Args:
            text (str): Message text to log.
        """

        self.logger.error(text)

    def critical(self, text: str) -> None:
        """Logs a critical message.

        Args:
            text (str): Message text to log.
        """

        self.logger.critical(text)
