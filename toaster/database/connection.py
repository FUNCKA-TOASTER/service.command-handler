"""Module "database".

File:
    connection.py

About:
    ...
"""

from urllib.parse import quote
from toaster.credentials import AlchemySetup, AlchemyCredentials


def build_connection_uri(setup: AlchemySetup, creds: AlchemyCredentials) -> str:
    return (
        f"{setup.dialect}+{setup.driver}://"
        f"{quote(creds.user)}:{quote(creds.pswd)}@"
        f"{creds.host}:{creds.port}/"
        f"{setup.database}"
    )
