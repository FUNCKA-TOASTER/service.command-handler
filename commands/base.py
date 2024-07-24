"""Module "commands".

File:
    base.py

About:
    File describing base bot command class.
"""

import re
from typing import Union, Optional, Tuple, List
from abc import ABC, abstractmethod
from vk_api import VkApi
from toaster.broker.events import Event


class BaseCommand(ABC):
    """Base class of the bot command."""

    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api

    def __call__(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        return self._handle(name, args, event)

    @abstractmethod
    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        """The main function of command execution.

        Args:
            name (str): Comamnd name.
            args (Optional[List[str]]): Command arguments.
            event (Event): Custom Event object.

        Returns:
            bool: Execution status.
        """

    @staticmethod
    def is_tag(tag: str) -> bool:
        """Checks whether the argument is a user tag.

        Args:
            tag (str): User tag construct.

        Returns:
            bool: Status flag.
        """
        pattern = r"^\[id[-+]?\d+\|\@?.*\]"
        return bool(re.findall(pattern, tag))

    @staticmethod
    def id_from_tag(tag: str) -> int:
        """Extracts the user id from the tag construct.

        Args:
            tag (str): User tag construct.

        Returns:
            int: User ID.
        """
        sep_pos = tag.find("|")
        return int(tag[3:sep_pos])

    def name_from_id(self, uuid: Union[str, int]) -> Optional[Tuple[str, str]]:
        """Gets the username by its ID.

        Args:
            uuid (Union[str, int]): User ID.

        Returns:
            Optional[Tuple[str, str]]: First name-last name pair.
        """
        user_info = self.api.users.get(user_ids=uuid, fields=["domain"])

        if not user_info:
            return None

        return (user_info[0].get("first_name"), user_info[0].get("last_name"))
