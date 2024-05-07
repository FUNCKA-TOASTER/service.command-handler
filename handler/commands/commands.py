from vk_api import VkApiError
from tools.keyboards import Keyboard, Callback, ButtonColor
from db import db
from logger import logger
from producer import producer
from .base import BaseCommand


class MarkCommand(BaseCommand):
    PERMISSION = 2
    NAME = "mark"
    MARK = ("UNDEFINED", "LOG", "CHAT")

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

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        await producer.command_alert(event, self.NAME)

        return True


class PermissionCommand(BaseCommand):
    PERMISSION = 2
    NAME = "permission"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        if not args:
            return False

        user_tag = args[0]

        if not self.is_tag(user_tag):
            return False

        answer_text = (
            f"⚠️ Уровни доступа пользователя {user_tag} \n\n"
            "Выберите необходимое дествие из меню ниже:"
        )

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="Модератор",
                    payload={
                        "call_action": "set_permission",
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
                        "call_action": "set_permission",
                        "permission": 2,
                        "target": self.id_from_tag(user_tag),
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_button(
                Callback(
                    label="Пользователь",
                    payload={
                        "call_action": "set_permission",
                        "permission": 0,
                        "target": self.id_from_tag(user_tag),
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)

        return True


class GameCommand(BaseCommand):
    PERMISSION = 0
    NAME = "game"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "🎲 Потянуло на азарт? :)\n\n" "Выберите игру из списка ниже:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(label="Рулетка", payload={"call_action": "game_roll"}),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Бросок монетки", payload={"call_action": "game_coinflip"}
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)

        return True


class SayCommand(BaseCommand):
    PERMISSION = 1
    NAME = "say"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        if not args:
            return False

        answer_text = " ".join(args)

        self.api.messages.send(
            peer_ids=event.get("peer_id"), random_id=0, message=answer_text
        )
        await producer.command_alert(event, self.NAME)


class DeleteCommand(BaseCommand):
    PERMISSION = 1
    NAME = "delete"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            cmids = [str(event["reply"].get("conversation_message_id"))]

        elif event.get("forward"):
            cmids = [
                str(msg.get("conversation_message_id")) for msg in event["forward"]
            ]

        else:
            return False

        await producer.command_alert(event, self.NAME)
        await self._delete_message(cmids, event.get("peer_id"))

        return True

    async def _delete_message(self, cmids: list, peer_id: int):
        try:
            ids = ",".join(cmids)
            self.api.messages.delete(delete_for_all=1, cmids=ids, peer_id=peer_id)

        except VkApiError as error:
            log_text = f"Could not delete <{cmids}> message: {error}"
            await logger.info(log_text)


class CopyCommand(BaseCommand):
    PERMISSION = 1
    NAME = "copy"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            answer_text = event["reply"].get("text")
            self.api.messages.send(
                peer_ids=event.get("peer_id"), random_id=0, message=answer_text
            )
            await producer.command_alert(event, self.NAME)
            return True

        return False


class SettingsCommand(BaseCommand):
    PERMISSION = 2
    NAME = "settings"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "🚸 Выберите необходимую группу настроек:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="Фильтры",
                    payload={"call_action": "filters_settings", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Системы",
                    payload={"call_action": "systems_settings", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)
        return True


class DelayCommand(BaseCommand):
    PERMISSION = 2
    NAME = "delay"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="Медленный режим",
                    payload={
                        "call_action": "change_delay",
                        "setting": "slow_mode",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Возраст аккаунта",
                    payload={
                        "call_action": "change_delay",
                        "setting": "account_age",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Срок сессий",
                    payload={
                        "call_action": "change_delay",
                        "setting": "menu_session",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        answer_text = "🚸 Выберите настройку:"

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)
        return True


class ExpireCommand(BaseCommand):
    PERMISSION = 2
    NAME = "expire"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="Зеленая зона",
                    payload={
                        "call_action": "change_delay",
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
                        "call_action": "change_delay",
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
                        "call_action": "change_delay",
                        "setting": "red_zone",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        answer_text = "🚸 Выберите зону:"

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)
        return True


class PunishmentCommand(BaseCommand):
    PERMISSION = 2
    NAME = "punishment"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "🚸 Выберите необходимую группу настроек:"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="Фильтры",
                    payload={"call_action": "filters_punishment", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Системы",
                    payload={"call_action": "systems_punishment", "page": "1"},
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)
        return True


class KickCommand(BaseCommand):
    PERMISSION = 1
    NAME = "kick"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        user_id = None

        if args and self.is_tag(args[0]):
            user_id = self.id_from_tag(args[0])

        elif event.get("reply", False):
            # TODO: Добавить удаление сообщения нарушителя.
            user_id = event.get("reply").get("from_id")

        if user_id is not None:
            if user_id == event.get("user_id"):
                return False

            try:
                user_name = self.name_from_id(user_id)
                self.api.messages.removeChatUser(
                    chat_id=event.get("chat_id"), user_id=user_id
                )

                query = f"""
                INSERT INTO 
                    kicked
                    (
                        conv_id,
                        user_id,
                        user_name,
                        kick_date
                    )
                VALUES
                    (
                        '{event.get("peer_id")}',
                        '{user_id}',
                        '{self.name_from_id(user_id)}',
                        NOW()
                    )
                ON DUPLICATE KEY UPDATE
                        user_name = '{user_name}',
                        kick_date = NOW();
                """
                db.execute.raw(schema="toaster", query=query)
                await producer.initiate_warn(event, 0, user_id, user_name, 0)
                await producer.command_alert(event, self.NAME)
                await producer.kick_alert(event, user_id, user_name)
                return True

            except VkApiError:
                return False

        return False


class WarnCommand(BaseCommand):
    PERMISSION = 1
    NAME = "warn"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        user_id = None

        if args and self.is_tag(args[0]):
            user_id = self.id_from_tag(args[0])
            if len(args) > 1:
                warns = int(args[1]) if args[1].isnumeric() else 1
            else:
                warns = 1

            target_cmid = None

        elif event.get("reply", False):
            user_id = event.get("reply").get("from_id")
            if len(args):
                warns = int(args[0]) if args[0].isnumeric() else 1
            else:
                warns = 1

            target_cmid = event["reply"].get("conversation_message_id")

        if user_id is not None:
            if user_id == event.get("user_id"):
                return False

            user_name = self.name_from_id(user_id)
            await producer.initiate_warn(event, warns, user_id, user_name, target_cmid)
            await producer.command_alert(event, self.NAME)
            return True

        return False


class UnwarnCommand(BaseCommand):
    PERMISSION = 1
    NAME = "unwarn"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        user_id = None

        if args and self.is_tag(args[0]):
            user_id = self.id_from_tag(args[0])
            if len(args) > 1:
                warns = int(args[1]) if args[1].isnumeric() else 1
            else:
                warns = 1

        elif event.get("reply", False):
            user_id = event.get("reply").get("from_id")
            if len(args):
                warns = int(args[0]) if args[0].isnumeric() else 1
            else:
                warns = 1

        if user_id is not None:
            target_cmid = None
            user_name = self.name_from_id(user_id)
            await producer.initiate_warn(event, -warns, user_id, user_name, target_cmid)
            await producer.command_alert(event, self.NAME)
            return True

        return False


# TODO: В дальнейшем придумать, как сделать более лаконично.
class AddCurseWordCommand(BaseCommand):
    PERMISSION = 2
    NAME = "acw"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        if args:
            new_word = args[0].lower()

            db.execute.insert(
                schema="toaster_settings",
                table="curse_words",
                on_duplicate="update",
                conv_id=event.get("peer_id"),
                word=new_word,
            )
            await producer.command_alert(event, self.NAME)
            return True

        return False


# TODO: В дальнейшем придумать, как сделать более лаконично.
class AddURLFilterPatternCommand(BaseCommand):
    PERMISSION = 2
    NAME = "aufp"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get("argument_list")

        if args:
            pattern_type = args[0].lower()
            pattern_status = args[1].lower()
            pattern = args[2].lower()

            db.execute.insert(
                schema="toaster_settings",
                table="url_filter",
                on_duplicate="update",
                conv_id=event.get("peer_id"),
                type=pattern_type,
                status=pattern_status,
                pattern=pattern,
            )
            await producer.command_alert(event, self.NAME)
            return True

        return False


class ProfileCommand(BaseCommand):
    PERMISSION = 0
    NAME = "profile"
    MARK = ("CHAT",)

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = (
            f"🚸 Профиль: [id{event.get('user_id')}|{event.get('user_name')}] \n"
        )

        warn_info = self._get_warns(event)
        if warn_info:
            warn_count, warn_expire = warn_info
            answer_text += f"Предупреждения: {warn_count} \n"
            answer_text += f"Истекает: {warn_expire} \n"
        else:
            answer_text += "Предупреждения: 0 \n"

        answer_text += "-- \n"

        queue_expire = self._get_queue(event)
        if queue_expire:
            answer_text += "В очереди: Да \n"
            answer_text += f"Истекает: {queue_expire} \n"
        else:
            answer_text += "В очереди: Нет"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(label="Закрыть", payload={"call_action": "cancel_command"}),
                ButtonColor.NEGATIVE,
            )
        )

        send_info = self.api.messages.send(
            peer_ids=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        peer_id, cmid = send_info[0]["peer_id"], send_info[0]["conversation_message_id"]
        self.initiate_session(peer_id, cmid)

        await producer.command_alert(event, self.NAME)
        return True

    def _get_warns(self, event) -> tuple:
        result = db.execute.select(
            schema="toaster",
            table="warn_points",
            fields=("points", "expire"),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
        )

        return result[0] if result else ()

    def _get_queue(self, event) -> str:
        result = db.execute.select(
            schema="toaster",
            table="slow_mode_queue",
            fields=("prohibited_until",),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
        )

        return result[0][0] if result else ""
