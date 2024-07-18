from typing import Optional, List
from toaster.broker.events import Event
from toaster.keyboards import Keyboard, ButtonColor, Callback
from rules import requires_mark, requires_permission, requires_attachments
from data import UserPermission, PeerMark
from .base import BaseCommand


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


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class Permission(BaseCommand):
    NAME = "permission"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if not args or not self.is_tag(user_tag := args[0]):
            return False

        answer_text = (
            f"⚠️ Уровни доступа пользователя {user_tag} \n\n"
            "Выберите необходимое дествие из меню ниже:"
        )

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="Модератор",
                    payload={
                        "action_name": "set_permission",
                        "permission": 1,
                        "target": self.id_from_tag(user_tag),
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_button(
                Callback(
                    label="Администратор",
                    payload={
                        "action_name": "set_permission",
                        "permission": 2,
                        "target": self.id_from_tag(user_tag),
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_button(
                Callback(
                    label="Сбросить",
                    payload={
                        "action_name": "drop_permission",
                        "target": self.id_from_tag(user_tag),
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_row()
            .add_button(
                Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        # TODO: Создать сессию меню
        # TODO: Алерт о вызове команды

        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class Say(BaseCommand):
    NAME = "say"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if not args:
            return False

        answer_text = " ".join(args)

        self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=answer_text,
        )

        return True


@requires_mark(PeerMark.CHAT)
@requires_attachments(("reply", "forward"))
@requires_permission(UserPermission.moderator)
class Delete(BaseCommand):
    NAME = "delete"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if "reply" in event.message.attachments:
            self.api.messages.delete(
                delete_for_all=1,
                cmids=event.message.reply.cmid,
                peer_id=event.message.reply.bpid,
            )

        elif "forward" in event.message.attachments:
            for reply in event.message.forward:
                self.api.messages.delete(
                    delete_for_all=1,
                    cmids=reply.cmid,
                    peer_id=event.peer.bpid,
                )
        else:
            return False

        return True
