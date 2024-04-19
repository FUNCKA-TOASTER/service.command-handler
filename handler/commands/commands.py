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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

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
            peer_id=event.get("peer_id"), random_id=0, message=answer_text
        )


class DeleteCommand(BaseCommand):
    PERMISSION = 1
    NAME = "delete"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            msgids = [event["reply"].get("id")]

        elif event.get("forward"):
            msgids = [msg.get("id") for msg in event["forward"]]

        else:
            return False

        await self._delete_message(msgids)
        return True

    async def _delete_message(self, msgids: list):
        try:
            self.api.messages.delete(delete_for_all=1, message_ids=msgids)

        except VkApiError as error:
            log_text = f"Could not delete <{msgids}> message: {error}"
            await logger.info(log_text)


class CopyCommand(BaseCommand):
    PERMISSION = 1
    NAME = "copy"
    MARK = ("LOG", "CHAT")

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            answer_text = event["reply"].get("text")
            self.api.messages.send(
                peer_id=event.get("peer_id"), random_id=0, message=answer_text
            )

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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

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
                        "call_action": "slow_mode_delay",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_button(
                Callback(
                    label="Возраст аккаунта",
                    payload={
                        "call_action": "account_age_delay",
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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

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
                        "call_action": "green_zone_delay",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Жёлтая зона",
                    payload={
                        "call_action": "yellow_zone_delay",
                    },
                ),
                ButtonColor.PRIMARY,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Красная зона",
                    payload={
                        "call_action": "red_zone_delay",
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

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json,
        )

        return True


class KickCommand(BaseCommand):
    PERMISSION = 2
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
                        user_name = '{self.name_from_id(user_id)}',
                        kick_date = NOW();
                """
                db.execute.raw(schema="toaster", query=query)

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

        elif event.get("reply", False):
            user_id = event.get("reply").get("from_id")
            if len(args):
                warns = int(args[0]) if args[0].isnumeric() else 1
            else:
                warns = 1

        if user_id is not None:
            if user_id == event.get("user_id"):
                return False

            user_name = self.name_from_id(user_id)
            producer.initiate_warn(event, warns, user_id, user_name)

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

            return True

        return False
