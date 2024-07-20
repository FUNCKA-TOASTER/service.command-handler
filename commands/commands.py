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
@requires_attachments("reply", "forward")
@requires_permission(UserPermission.moderator)
class Delete(BaseCommand):
    NAME = "delete"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if "reply" in event.message.attachments:
            self.api.messages.delete(
                delete_for_all=1,
                cmids=event.message.reply.cmid,
                peer_id=event.peer.bpid,
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


@requires_mark(PeerMark.CHAT)
class Game(BaseCommand):
    NAME = "game"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "🎲 Потянуло на азарт? :)\n\n" "Выберите игру из списка ниже:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(label="Рулетка", payload={"action_name": "game_roll"}),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Бросок монетки", payload={"action_name": "game_coinflip"}
                ),
                ButtonColor.PRIMARY,
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

        return True


@requires_mark(PeerMark.CHAT)
@requires_attachments("reply")
@requires_permission(UserPermission.moderator)
class Copy(BaseCommand):
    NAME = "copy"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        self.api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=event.message.reply.text,
        )
        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class Settings(BaseCommand):
    NAME = "settings"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "🚸 Выберите необходимую группу настроек:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="Фильтры",
                    payload={"action_name": "filters_settings", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Системы",
                    payload={"action_name": "systems_settings", "page": "1"},
                ),
                ButtonColor.PRIMARY,
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

        # TODO: создать сессию меню

        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class Delay(BaseCommand):
    NAME = "delay"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "🚸 Выберите настройку:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="Медленный режим",
                    payload={
                        "action_name": "change_delay",
                        "setting_name": "slow_mode",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Возраст аккаунта",
                    payload={
                        "action_name": "change_delay",
                        "setting_name": "account_age",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Срок сессий",
                    payload={
                        "action_name": "change_delay",
                        "setting_name": "menu_session",
                    },
                ),
                ButtonColor.PRIMARY,
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

        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class Expire(BaseCommand):
    NAME = "expire"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "🚸 Выберите зону:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="Зеленая зона",
                    payload={
                        "action_name": "change_delay",
                        "setting": "green_zone",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Жёлтая зона",
                    payload={
                        "action_name": "change_delay",
                        "setting": "yellow_zone",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Красная зона",
                    payload={
                        "action_name": "change_delay",
                        "setting": "red_zone",
                    },
                ),
                ButtonColor.PRIMARY,
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
        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class Punishment(BaseCommand):
    NAME = "punishment"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = "🚸 Выберите необходимую группу настроек:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="Фильтры",
                    payload={"action_name": "filters_punishment", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Системы",
                    payload={"action_name": "systems_punishment", "page": "1"},
                ),
                ButtonColor.PRIMARY,
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
        return True
