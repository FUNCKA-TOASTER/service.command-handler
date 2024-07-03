"""Module "database".

File:
    database.py

About:
    ...
"""

from typing import NoReturn, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    """DOCSTRING"""

    def __init__(self, connection_uri: str, debug: bool = False):
        self._engine = create_engine(connection_uri)
        self._session = sessionmaker(bind=self._engine, autoflush=False)

    def create_tables(self, base: Any) -> NoReturn:
        base.metadata.create_all(self._engine)

    def drop_tables(self, base: Any) -> NoReturn:
        base.metadata.drop_all(self._engine)

    @property
    def engine(self):
        return self._engine

    def make_session(self):
        return self.session()
