"""Service "toaster.comman-handling-service".

File:
    start.py


About:
    This service is responsible for receiving custom
    events from the Redis channel "command", processing
    these events, and executing actions based on the
    command name specified in the event text.
"""

from toaster.broker import Subscriber, build_connection
from toaster.logger import Logger

# from handler import CommandHandler
import config


def main():
    """Entry point."""

    subscriber = Subscriber(client=build_connection(config.REDIS_CREDS))
    logger = Logger()
    # handler = CommandHandler()

    logger.info("Waiting for events...")
    for event in subscriber.listen(channel_name=config.CHANNEL_NAME):
        logger.info(f"Recived new event: \n{event}")
        # handler(event)


if __name__ == "__main__":
    main()
