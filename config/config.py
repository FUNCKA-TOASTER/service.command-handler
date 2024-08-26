"""Module "config".

File:
    config.py

About:
    This file defines the used variables
    and configuration objects.
"""

import os
from funcka_bots.credentials import RabbitMQCredentials

BROKER_CREDS = RabbitMQCredentials(
    host=os.getenv("rabbitmq_host"),
    port=os.getenv("rabbitmq_port"),
    vhost=os.getenv("rabbitmq_vhost"),
    user=os.getenv("rabbitmq_user"),
    pswd=os.getenv("rabbitmq_pswd"),
)

BROKER_QUEUE_NAME = "command"

VK_GROUP_TOKEN: str = os.getenv("vk_group_token")

VK_GROUP_ID: int = int(os.getenv("vk_group_id"))

VK_API_VERSION: str = "5.199"

MAX_ARG_COUNT = 10
