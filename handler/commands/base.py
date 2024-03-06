from vk_api import VkApi
from .abc import ABCHandler


class BaseCommand(ABCHandler):
    """Command handler base class.
    """
    _permission_lvl = 0
    COMMAND_NAME = "None"

    def __init__(self, api: VkApi):
        #self.db = db
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
        return self._permission_lvl
