"""Module "database".

File:
    database.py

About:
    ...
"""

from typing import NoReturn, Any
from .credentials import Credentials
from .connection import Connection


class Database:
    """DOCSTRING"""

    def __init__(
        self,
        dialect: str,
        driver: str,
        database: str,
        creds: Credentials,
        debug: bool = False,
    ) -> NoReturn:
        con = Connection(
            dialect=dialect, driver=driver, database=database, creds=creds, debug=debug
        )
        self._engine = con.engine

    def create_tables(self, base: Any) -> NoReturn:
        base.metadata.create_all(self._engine)

    def drop_tables(self, base: Any) -> NoReturn:
        base.metadata.drop_all(self._engine)
