from typing import Optional, List
from toaster.broker.events import Event
from toaster.keyboards import Keyboard, ButtonColor, Callback
from rules import requires_mark, requires_permission
from data import UserPermission, PeerMark
from .base import BaseCommand


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class Test(BaseCommand):
    NAME = "test"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "⚠️ Тестовая команда!"

        answer = self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
        )

        return True


@requires_permission(UserPermission.administrator)
class Mark(BaseCommand):
    NAME = "mark"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = (
            "⚠️ Вы хотите задать метку беседе? \n\n"
            "Выберите необходимое дествие из меню ниже:"
        )

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="CHAT", payload={"action_name": "set_mark", "mark": "CHAT"}
                ),
                ButtonColor.POSITIVE,
            )
            .add_button(
                Callback(
                    label="LOG", payload={"action_name": "set_mark", "mark": "LOG"}
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Обновить данные беседы",
                    payload={"action_name": "update_peer_data"},
                ),
                ButtonColor.SECONDARY,
            )
            .add_row()
            .add_button(
                Callback(label="Сбросить метку", payload={"action_name": "drop_mark"}),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                ButtonColor.NEGATIVE,
            )
        )

        answer = self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        return True
