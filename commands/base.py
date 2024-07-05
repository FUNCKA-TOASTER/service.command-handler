import re
from typing import Union, Optional, Tuple, List
from abc import ABC, abstractmethod
from vk_api import VkApi
from toaster.broker.events import Event


class BaseCommand(ABC):
    """DOCSTRING"""

    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api

    def __call__(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        return self._handle(name, args, event)

    @abstractmethod
    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        """DOCSTRING"""

    @property
    def name(self):
        return self.name

    @staticmethod
    def is_tag(tag: str) -> bool:
        pattern = r"^\[id[-+]?\d+\|\@?.*\]"
        return bool(re.findall(pattern, tag))

    @staticmethod
    def id_from_tag(tag: str) -> int:
        sep_pos = tag.find("|")
        return int(tag[3:sep_pos])

    def name_from_id(self, uuid: Union[str, int]) -> Optional[Tuple[str, str]]:
        user_info = self.api.users.get(user_ids=uuid, fields=["domain"])

        if not user_info:
            return None

        return (user_info[0].get("first_name"), user_info[0].get("last_name"))

    def initiate_session(self, conv_id: int, cmid: int) -> None:
        pass
        # interval = db.execute.select(
        #     schema="toaster_settings",
        #     table="delay",
        #     fields=("delay",),
        #     conv_id=conv_id,
        #     setting_name="menu_session",
        # )

        # interval = int(interval[0][0]) if interval else 0
        # query = f"""
        # INSERT INTO
        #     menu_sessions(conv_id, cm_id, expired)
        # VALUES

        #     (
        #         '{conv_id}',
        #         '{cmid}',
        #         NOW() + INTERVAL {interval} MINUTE
        #     );
        # """
        # db.execute.raw(schema="toaster", query=query)
