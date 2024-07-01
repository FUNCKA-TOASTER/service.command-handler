"""Module "config".

File:
    config.py

About:
    This file defines configuration variables used
    throughout the application, including service names,
    API tokens, broker addresses, and other settings.
"""

import os

# Service name used for identification
SERVICE_NAME = "toaster.command-handling-service"

# Address of the message broker
BROKER_ADDR = "172.18.0.40"

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

# Host Address for DBMS
DBMS_HOST = os.getenv("SQL_HOST")

# Port for DBMS
DBMS_PORT = int(os.getenv("SQL_PORT"))

# User for DBMS
DBMS_USER = os.getenv("SQL_USER")

# Password for DBMS user
DBMS_PSWD = os.getenv("SQL_PSWD")

# Name of the used DBMS
DBMS_NAME = "mysql"

# Driver for DBMS
DBMS_DRIVER = "pymysql"
