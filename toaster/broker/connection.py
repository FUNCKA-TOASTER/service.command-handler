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
from toaster.credentials import RedisCredentials


def build_connection(creds: RedisCredentials) -> Redis:
    return Redis(
        host=creds.host,
        port=creds.port,
        db=creds.db,
    )
