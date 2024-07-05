from typing import Optional, List
from toaster.broker.events import Event
from .base import BaseCommand


class TestCommand(BaseCommand):
    """DOCSTRING"""

    NAME = "test"

    def _handle(self, event: Event, args: Optional[List[str]]) -> bool:
        pass
