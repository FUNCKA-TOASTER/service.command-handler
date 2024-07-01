"""Module "logger".

File:
    formatters.py

About:
    This file provides functions for creating logging
    formatters with optional color support.
"""

import logging
from logging import Formatter
from colorama import Fore


def get_formatter(colored: bool) -> Formatter:
    """Returns a logging formatter based on the specified color preference.

    Args:
        colored (bool): Flag indicating whether to use colored output.

    Returns:
        logging.Formatter: Logging formatter object.
    """

    return __colored() if colored else __mono()


def __colored() -> Formatter:
    formatter = logging.Formatter(
        Fore.RED
        + "[ %(name)s | %(levelname)s | %(asctime)s ] "
        + Fore.WHITE
        + "Message: %(message)s"
    )

    return formatter


def __mono() -> Formatter:
    formatter = logging.Formatter(
        "[ %(name)s | %(levelname)s | %(asctime)s ] " + "Message: %(message)s"
    )

    return formatter
