from typing import Optional, List
from toaster.broker.events import Event
from rules import requires_mark, requires_permission
from .base import BaseCommand


class TestCommand(BaseCommand):
    """DOCSTRING"""

    NAME = "test"

    def _handle(self, event: Event, args: Optional[List[str]]) -> bool:
        answer_text = "⚠️ Тестовая команда!"

        answer = self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
        )

        return True
