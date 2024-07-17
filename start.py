"""Service "toaster.comman-handling-service".

File:
    start.py

About:
    This service is responsible for receiving custom
    events from the Redis channel "command", processing
    these events, and executing actions based on the
    command name specified in the event text.
"""

import sys
from loguru import logger
from toaster.broker import Subscriber, build_connection
from handler import CommandHandler
import config


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def main():
    """Entry point."""

    setup_logger()
    subscriber = Subscriber(client=build_connection(config.REDIS_CREDS))
    handler = CommandHandler()

    for event in subscriber.listen(channel_name=config.CHANNEL_NAME):
        handler(event)


if __name__ == "__main__":
    main()
