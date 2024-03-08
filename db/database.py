from .connection import Connection
from .execute import Executer
from .preset import Preseter


class DataBase(object):
    """
    The main class is the database view.
    Organizes a connection and implements
    access to table properties using
    object-relational methods of the base table.
    """
    def __init__(self, host: str, port: int, user: str, password: str):
        self._tunnel = Connection(
            host=host,
            port=port,
            user=user,
            password=password
        )

        self._execute = Executer(
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

        self._preset = Preseter(
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )


    @property
    def execute(self):
        return self._execute


    @property
    def preset(self):
        return self._preset



db = DataBase(
    host="host",
    port=1,
    user="user",
    password="password"
)
