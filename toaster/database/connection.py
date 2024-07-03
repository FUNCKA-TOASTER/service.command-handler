"""Module "database".

File:
    connection.py

About:
    ...
"""

from urllib.parse import quote
from .credentials import Credentials, Setup


def build_connection_uri(setup: Setup, creds: Credentials) -> str:
    return (
        f"{setup.dialect}+{setup.driver}://"
        f"{quote(creds.user)}:{quote(creds.pswd)}@"
        f"{creds.host}:{creds.port}/"
        f"{setup.database}"
    )
