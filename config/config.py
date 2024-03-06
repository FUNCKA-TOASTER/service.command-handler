"""Module "config".
"""
import os

SERVICE_NAME = "toaster.command-handling-service"

QUEUE_BROKER_IP = "172.18.0.40"

TOKEN: str = os.getenv("TOKEN")
GROUP_ID: int = int(os.getenv("GROUPID"))
