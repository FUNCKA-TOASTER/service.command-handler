"""Module "database".

File:
    database.py

About:
    ...
"""

from typing import Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

BaseModel = declarative_base()


class Database:
    """DOCSTRING"""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        self._engine = create_engine(connection_uri, echo=debug)
        self._session = sessionmaker(bind=self._engine, autoflush=False)

    def site_create_tables(self, base: Any) -> None:
        base.metadata.create_all(self._engine)

    def site_drop_tables(self, base: Any) -> None:
        base.metadata.drop_all(self._engine)

    def create_tables(self) -> None:
        BaseModel.metadata.create_all(self._engine)

    def drop_tables(self) -> None:
        BaseModel.metadata.create_all(self._engine)

    @property
    def engine(self) -> Engine:
        return self._engine

    def make_session(self) -> Session:
        return self._session()
