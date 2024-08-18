"""Module "commands".

File:
    commands.py

About:
    File describing Possible commands recognized by the bot.
"""

from typing import Optional, List
from db import TOASTER_DB
from toaster.broker.events import Event
from toaster.keyboards import Keyboard, ButtonColor, Callback
from toaster_utils.enums import (
    UserPermission,
    PeerMark,
    LinkStatus,
    LinkType,
)
from toaster_utils.scripts import (
    get_user_warns,
    get_user_queue_status,
    insert_pattern,
    insert_cursed,
    open_menu_session,
)
from rules import (
    requires_mark,
    requires_permission,
    requires_attachments,
)
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

        self.api.messages.send(
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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

        return True


@requires_mark(PeerMark.CHAT)
class Profile(BaseCommand):
    NAME = "profile"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        answer_text = f"🚸 Профиль: [id{event.user.uuid}|{event.user.name}] \n"

        warn_info = get_user_warns(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
        )
        if warn_info:
            warn_count, warn_expire = warn_info
            answer_text += f"Предупреждения: {warn_count} \n"
            answer_text += f"Истекает: {warn_expire} \n"
        else:
            answer_text += "Предупреждения: 0 \n"

        answer_text += "-- \n"

        queue_expire = get_user_queue_status(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
        )
        if queue_expire:
            answer_text += "В очереди: Да \n"
            answer_text += f"Истекает: {queue_expire} \n"
        else:
            answer_text += "В очереди: Нет"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
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

        cmid = send_info[0]["conversation_message_id"]
        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class Kick(BaseCommand):
    NAME = "kick"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if args and self.is_tag(args[0]):
            target_id = self.id_from_tag(args[0])
            if len(args) > 1:
                mode = "global" if args[1] == "global" else "local"
            else:
                mode = "local"

        elif event.message.reply:
            target_id = event.message.reply.uuid
            if len(args) > 0:
                mode = "global" if args[0] == "global" else "local"
            else:
                mode = "local"

        else:
            return False

        if target_id == event.user.uuid:
            return False

        comment = "Модератор исключил вас из беседы"
        self._publish_punishment(
            type="kick",
            comment=comment,
            mode=mode,
            event=event,
            target_id=target_id,
        )
        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class Warn(BaseCommand):
    NAME = "warn"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if args and self.is_tag(args[0]):
            target_id = self.id_from_tag(args[0])
            if len(args) > 1:
                points = int(args[1]) if args[1].isnumeric() else 1
            else:
                points = 1

        elif event.message.reply:
            target_id = event.message.reply.uuid
            if len(args) > 0:
                points = int(args[0]) if args[0].isnumeric() else 1
            else:
                points = 1

        else:
            return False

        if target_id == event.user.uuid:
            return False

        comment = "Модератор вынес предупреждение"
        self._publish_punishment(
            type="warn",
            comment=comment,
            points=points,
            event=event,
            target_id=target_id,
        )
        return True


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.moderator)
class Unwarn(BaseCommand):
    NAME = "unwarn"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if args and self.is_tag(args[0]):
            target_id = self.id_from_tag(args[0])
            if len(args) > 1:
                points = int(args[1]) if args[1].isnumeric() else 1
            else:
                points = 1

        elif event.message.reply:
            target_id = event.message.reply.uuid
            if len(args) > 0:
                points = int(args[0]) if args[0].isnumeric() else 1
            else:
                points = 1

        else:
            return False

        if target_id == event.user.uuid:
            return False

        comment = "Модератор снял предупреждение"
        self._publish_punishment(
            type="unwarn",
            comment=comment,
            points=points,
            event=event,
            target_id=target_id,
        )
        return True


@requires_mark(PeerMark.CHAT)
@requires_attachments("reply", "forward")
@requires_permission(UserPermission.moderator)
class Delete(BaseCommand):
    NAME = "delete"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if not event.message.reply and not event.message.forward:
            return False

        comment = "Модератор удалил сообщения."
        self._publish_punishment(
            type="delete",
            comment=comment,
            event=event,
            target_id=0,
        )
        return True


# TODO: Подумать, как можно фиксануть
# Опасные команды. не использовать кроме тех, кро знает как
@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class AddLinkPattern(BaseCommand):
    NAME = "alp"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if args:
            pattern_type = LinkType(args[0].lower())
            pattern_status = LinkStatus(args[1].lower())
            pattern = args[2].lower()

            insert_pattern(
                db_instance=TOASTER_DB,
                bpid=event.peer.bpid,
                type=pattern_type,
                status=pattern_status,
                pattern=pattern,
            )

            return True

        return False


@requires_mark(PeerMark.CHAT)
@requires_permission(UserPermission.administrator)
class AddCurseWord(BaseCommand):
    NAME = "acw"

    def _handle(self, name: str, args: Optional[List[str]], event: Event) -> bool:
        if args:
            new_word = args[0].lower()
            insert_cursed(
                db_instance=TOASTER_DB,
                bpid=event.peer.bpid,
                word=new_word,
            )

            return True

        return False
