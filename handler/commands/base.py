import re
from vk_api import VkApi
from .abc import ABCHandler


class BaseCommand(ABCHandler):
    """Command handler base class."""

    PERMISSION = 0
    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api

    async def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me

    @staticmethod
    def is_tag(tag: str) -> bool:
        """Takes a string as input, determines
        is the line a VK user tag.

        Args:
            tag (str): The string that
            is assumed to be the user tag.

        Returns:
            bool: Is tag?
        """
        pattern = r"^\[id[-+]?\d+\|\@?.*\]"
        return bool(re.findall(pattern, tag))

    @staticmethod
    def id_from_tag(tag: str) -> int:
        """_summary_

        Args:
            tag (str): _description_

        Returns:
            int: _description_
        """
        sep_pos = tag.find("|")
        return int(tag[3:sep_pos])

    def name_from_id(self, user_id) -> str:
        """_summary_

        Args:
            user_id (_type_): _description_

        Returns:
            str: _description_
        """
        user_info = self.api.users.get(user_ids=user_id, fields=["domain"])

        if not user_info:
            return None

        user_name = " ".join(
            [user_info[0].get("first_name"), user_info[0].get("last_name")]
        )

        return user_name
