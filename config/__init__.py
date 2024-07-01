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
    DBMS_NAME,  # Name of the used DBMS
    DBMS_DRIVER,  # Driver for DBMS
    DBMS_CREDS,  # Driver for DBMS
)


__all__ = (
    "BROKER_ADDR",
    "CHANNEL_NAME",
    "TOKEN",
    "GROUP_ID",
    "SERVICE_NAME",
    "MAX_ARG_COUNT",
    "API_VERSION",
    "DBMS_NAME",
    "DBMS_DRIVER",
    "DBMS_CREDS",
)
