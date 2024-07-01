"""Module "config".

File:
    __init__.py

About:
    This file initializes the configuration variables
    used throughout the service. It imports and exposes
    key configuration constants such as API token,
    service name, and other settings required for proper
    operation.
"""

from .config import (
    BROKER_ADDR,  # Address of the message broker
    CHANNEL_NAME,  # Broker subscription channel name
    TOKEN,  # API token
    GROUP_ID,  # ID of the group
    SERVICE_NAME,  # Name of the service
    MAX_ARG_COUNT,  # Maxcount of arguments
    API_VERSION,  # Version of the API
    DBMS_HOST,  # DBMS Host address
    DBMS_PORT,  # DBMS port
    DBMS_PSWD,  # DBMS password
    DBMS_USER,  # DBMS user name
    DBMS_NAME,  # Name of the used DBMS
)


__all__ = (
    "BROKER_ADDR",
    "CHANNEL_NAME",
    "TOKEN",
    "GROUP_ID",
    "SERVICE_NAME",
    "MAX_ARG_COUNT",
    "API_VERSION",
    "DBMS_HOST",
    "DBMS_PORT",
    "DBMS_PSWD",
    "DBMS_USER",
    "DBMS_NAME",
)
