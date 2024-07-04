"""Module "credentials".

File:
    credentials.py

About:
    ...
"""

from typing import NamedTuple


class AlchemyCredentials(NamedTuple):
    """DOCSTRING"""

    host: str
    port: int
    user: str
    pswd: str


class AlchemySetup(NamedTuple):
    """DOCSTRING"""

    dialect: str
    driver: str
    database: str


class RedisCredentials(NamedTuple):
    """DOCSTRING"""

    host: str
    port: int
    user: str
    pswd: str
