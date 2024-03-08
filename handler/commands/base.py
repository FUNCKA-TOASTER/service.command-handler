import re
from vk_api import VkApi
from .abc import ABCHandler


class BaseCommand(ABCHandler):
    """Command handler base class.
    """
    _PERMISSION_LVL = 0
    _COMMAND_NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api


    async def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me


    @property
    def permission(self) -> int:
        """Returns the access level
        to execute the command.

        Returns:
            int: permission lvl.
        """
        return self._PERMISSION_LVL


    @property
    def name(self) -> str:
        """Returns the command name.

        Returns:
            str: command name.
        """
        return self._COMMAND_NAME


    def is_tag(self, tag: str) -> bool:
        """Takes a string as input, determines
        is the line a VK user tag.

        Args:
            tag (str): The string that
            is assumed to be the user tag.

        Returns:
            bool: Is tag?
        """
        pattern = r"^\[id[-+]?\d+\|\@?\w+\]"
        return bool(re.search(pattern, tag))


    def id_from_tag(self, tag: str) -> int:
        """_summary_

        Args:
            tag (str): _description_

        Returns:
            int: _description_
        """
        sep_pos = tag.find("|")
        return int(tag[3:sep_pos])
