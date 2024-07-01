"""Module "database".

File:
    credentials.py

About:
    ...
"""

from typing import NamedTuple


class Credentials(NamedTuple):
    """DOCSTRING"""

    host: str
    port: int
    user: str
    pswd: str
