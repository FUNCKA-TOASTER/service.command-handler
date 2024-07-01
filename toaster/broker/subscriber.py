"""Module "broker".

File:
    subscriber.py

About:
    This file contains the implementation of the
    Subscriber class, which listens to Redis channels
    and deserializes incoming messages. It provides
    methods for initializing the Redis client, subscribing
    to channels, and listening for messages.
"""

import dill as pickle
from typing import (
    NoReturn,
    Any,
    ByteString,
)
from .connection import Connection


class Subscriber:
    """Initializes the Subscriber with a Redis pubsub client.

    Descriprion:
        Class for subscribing to Redis channels and deserializing
        incoming messages.

    Args:
        host (str): Redis server hostname (default is "localhost").
        port (int): Redis server port (default is 6379).
        db (int): Redis database index (default is 0).

    Attributes:
        client (Redis): Redis client instance.
    """

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0
    ) -> NoReturn:
        con = Connection(
            host=host,
            port=port,
            db=db,
        )
        r = con.client
        self.client = r.pubsub()

    # TODO: Make logs
    # TODO: handle possible exeptions
    def listen(self, channel_name: str) -> Any:
        """Listens to messages on a specified Redis channel and deserializes them.

        Args:
            channel_name (str): Name of the Redis channel to listen to.

        Yields:
            object: Deserialized object received from the channel.
        """

        self.client.subscribe(channel_name)
        for event in self.client.listen():
            if event.get("type") == "message":
                yield self.__deserialize(event.get("data"))

    @staticmethod
    def __deserialize(data: ByteString) -> Any:
        return pickle.loads(data=data)
