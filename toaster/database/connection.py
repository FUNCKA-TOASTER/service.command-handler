"""Module "database".

File:
    connection.py

About:
    ...
"""

from typing import NoReturn
from sqlalchemy import create_engine, Engine
from urllib.parse import quote
from .credentials import Credentials


class Connection:
    """DOCSTRING"""

    def __init__(
        self,
        dialect: str,
        driver: str,
        database: str,
        creds: Credentials,
        debug: bool = False,
    ) -> NoReturn:
        connection_uri = (
            f"{dialect}+{driver}"
            "://"
            f"{quote(creds.user)}:{quote(creds.pswd)}"
            "@"
            f"{creds.host}:{creds.port}"
            "/"
            f"{database}"
        )
        self._engine = create_engine(connection_uri, echo=debug)

    @property
    def engine(self) -> Engine:
        return self._engine


# TODO: Переделать в функцию, возвращающую URI и не более.
# Функционал инициализации engine увести в класс Database.


def build_connection_uri():
    pass
