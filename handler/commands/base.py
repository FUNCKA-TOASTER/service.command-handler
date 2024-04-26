import re
from vk_api import VkApi
from db import db
from .abc import ABCHandler


class BaseCommand(ABCHandler):
    """Command handler base class."""

    PERMISSION = 0
    NAME = "None"
    MARK = ()

    def __init__(self, api: VkApi):
        self.api = api

    @staticmethod
    def is_tag(tag: str) -> bool:
        pattern = r"^\[id[-+]?\d+\|\@?.*\]"
        return bool(re.findall(pattern, tag))

    @staticmethod
    def id_from_tag(tag: str) -> int:
        sep_pos = tag.find("|")
        return int(tag[3:sep_pos])

    def name_from_id(self, user_id) -> str:
        user_info = self.api.users.get(user_ids=user_id, fields=["domain"])

        if not user_info:
            return None

        user_name = " ".join(
            [user_info[0].get("first_name"), user_info[0].get("last_name")]
        )

        return user_name

    def initiate_session(self, conv_id: int, message_id: int) -> None:
        cmid = self.api.messages.getById(message_ids=message_id)["items"][0][
            "conversation_message_id"
        ]
        cmid = int(cmid)
        interval = db.execute.select(
            schema="toaster_settings",
            table="delay",
            fields=("delay",),
            conv_id=conv_id,
            setting_name="menu_session",
        )

        interval = int(interval[0][0]) if interval else 0
        query = f"""
        INSERT INTO 
            menu_sessions(conv_id, cm_id, expired)
        VALUES 
	        (
                '{conv_id}',
                '{cmid}',
                NOW() + INTERVAL {interval} MINUTE
            );
        """
        db.execute.raw(schema="toaster", query=query)
