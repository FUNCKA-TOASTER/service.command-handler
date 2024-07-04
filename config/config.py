"""Module "config".

File:
    config.py

About:
    This file defines configuration variables used
    throughout the application, including service names,
    API tokens, broker addresses, and other settings.
"""

import os
from toaster.credentials import (
    AlchemyCredentials,
    AlchemySetup,
    RedisCredentials,
)

# Service name used for identification
SERVICE_NAME = "toaster.command-handling-service"

# Broker subscription channel name
CHANNEL_NAME = "command"

# API token obtained from environment variable
TOKEN: str = os.getenv("TOKEN")

# Group ID for identifying specific groups
GROUP_ID: int = int(os.getenv("GROUPID"))

# API version used for API requests
API_VERSION: str = "5.199"

# Max count of arguments in command
MAX_ARG_COUNT = 10

# Redis (broker) credentials
REDIS_CREDS = RedisCredentials(
    host="172.18.0.40",
    port=6379,
    db=0,
)

# Setup for sqlalchemy. Driver, Database and DBMS.
ALCHEMY_SETUP = AlchemySetup(
    dialect="mysql",
    driver="pymysql",
    database="toaster_dev",  # TODO: Позже заменить на toaster
)

# DBMS credentials that includes host, port, user, password.
DBMS_CREDS = AlchemyCredentials(
    host=os.getenv("SQL_HOST"),
    port=int(os.getenv("SQL_PORT")),
    user=os.getenv("SQL_USER"),
    pswd=os.getenv("SQL_PSWD"),
)
