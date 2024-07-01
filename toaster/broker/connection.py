"""Module "broker".

File:
    connection.py

About:
    This file provides a connection to a Redis server.
    It defines a Connection class that initializes a
    connection to Redis using specified host, port,
    and database number.
"""

from redis import Redis
from typing import NoReturn


class Connection:
    """A class to manage connection to a Redis server.

    Description:
        This class initializes a connection to a Redis server
        using the provided host, port, and database index.
        It provides a property to access the Redis client.

    Attributes:
        client (Redis): The Redis client used for interacting with the Redis server.
    """

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0
    ) -> NoReturn:
        self.client = Redis(host=host, port=port, db=db)

    @property
    def client(self) -> Redis:
        return self.client
