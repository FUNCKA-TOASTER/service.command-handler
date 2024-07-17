from typing import Optional, List
from toaster.broker.events import Event
from toaster.keyboards import Keyboard, ButtonColor, Callback
from rules import requires_mark, requires_permission
from data import UserPermission, PeerMark
from .base import BaseCommand


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class TestCommand(BaseCommand):
    """DOCSTRING"""

    NAME = "test"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "⚠️ Тестовая команда!"

        answer = self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
        )

        return True


class MarkCommand(BaseCommand):
    NAME = "mark"

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = (
            "⚠️ Вы хотите пометить новую беседу? \n\n"
            "Выберите необходимое дествие из меню ниже:"
        )

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="CHAT", payload={"call_action": "set_mark", "mark": "CHAT"}
                ),
                ButtonColor.POSITIVE,
            )
            .add_button(
                Callback(
                    label="LOG", payload={"call_action": "set_mark", "mark": "LOG"}
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Обновить данные беседы",
                    payload={"call_action": "update_conv_data"},
                ),
                ButtonColor.SECONDARY,
            )
            .add_row()
            .add_button(
                Callback(label="Сбросить метку", payload={"call_action": "drop_mark"}),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        answer = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        return True
