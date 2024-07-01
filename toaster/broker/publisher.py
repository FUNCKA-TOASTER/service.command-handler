"""Module "broker".

File:
    publisher.py

About:
    This file contains the implementation of the
    Publisher class, which facilitates publishing
    serialized objects to Redis channels. It provides
    methods for initializing the Redis client, serializing
    objects, and publishing them to specified channels.
"""

import dill as pickle
from typing import (
    NoReturn,
    ByteString,
    Any,
)
from .connection import Connection


class Publisher:
    """Initializes the Publisher with a Redis client.

    Description:
        Class for publishing serialized objects to Redis channels.

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
        self.client = con.client

    # TODO: make logs
    # TODO: handle possible exeptions
    def publish(self, obj: Any, channel_name: str) -> int:
        """Publishes a serialized object to a Redis channel.

        Args:
            obj (object): Object to be serialized and published.
            channel_name (str): Name of the Redis channel to publish to.

        Returns:
            int: Status code indicating the result of the publish operation.
        """

        data = self.__serialize(obj)
        status = self.client.publish(channel_name, data)

        return status

    @staticmethod
    def __serialize(obj: Any) -> ByteString:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)
