from vk_api import VkApiError
from tools.keyboards import (
    Keyboard,
    Callback,
    ButtonColor
)
from db import db
from logger import logger
from .base import BaseCommand


class MarkCommand(BaseCommand):
    """Mark command.
    Initializes conversation marking process.
    Allows:
        - To mark conversation as "CHAT" or "LOG".
        - Update the data about conversation.
        - Delete conversation mark.
    """
    PERMISSION = 2
    NAME = "mark"

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "⚠️ Вы хотите пометить новую беседу? \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="CHAT",
                    payload={
                        "call_action": "set_mark",
                        "mark": "CHAT"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="LOG",
                    payload={
                        "call_action": "set_mark",
                        "mark": "LOG"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_row()
            .add_button(
                Callback(
                    label="Обновить данные беседы",
                    payload={
                        "call_action": "update_conv_data"
                    }
                ),
                ButtonColor.SECONDARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Сбросить метку",
                    payload={
                        "call_action": "drop_mark"
                    }
                ),
                ButtonColor.NEGATIVE
            )
            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class PermissionCommand(BaseCommand):
    """Permission command.
    Sets new permission role to user.
    Allows:
        - Set "Administrator" role.
        - Set "Moderator" role.
        - Set "User" role.
    """
    PERMISSION = 2
    NAME = "permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get('argument_list')

        if not args:
            return False

        user_tag = args[0]

        if not self.is_tag(user_tag):
            return False

        answer_text = f"⚠️ Уровни доступа пользователя {user_tag} \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="Модератор",
                    payload={
                        "call_action": "set_permission",
                        "permission": 1,
                        "target": self.id_from_tag(user_tag)
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Администратор",
                    payload={
                        "call_action": "set_permission",
                        "permission": 2,
                        "target": self.id_from_tag(user_tag)
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Пользователь",
                    payload={
                        "call_action": "set_permission",
                        "permission": 0,
                        "target": self.id_from_tag(user_tag)
                    }
                ),
                ButtonColor.NEGATIVE
            )
            .add_row()

            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class GameCommand(BaseCommand):
    """Game command.
    Includes menu with the choice of the game.
    Allows:
        - Roll.
        - Coindflip.
    """
    PERMISSION = 0
    NAME = "game"

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "🎲 Потянуло на азарт? :)\n\n" \
            "Выберите игру из списка ниже:"

        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="Рулетка",
                    payload={
                        "call_action": "game_roll"
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Бросок монетки",
                    payload={
                        "call_action": "game_coinflip"
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class SayCommand(BaseCommand):
    """Say command.
    Sends a message from the face of the bot.
    Maximum 10 words.
    """
    PERMISSION = 1
    NAME = "say"

    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get('argument_list')

        if not args:
            return False

        answer_text = " ".join(args)

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text
        )



class DeleteCommand(BaseCommand):
    """Delete command.
    Deleting forwarded messages.
    """
    PERMISSION = 1
    NAME = "delete"

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            cmid = event["reply"].get("conversation_message_id")
            peer_id = event.get("peer_id")
            await self._delete_message(cmid, peer_id)

            return True

        elif event.get("forward"):
            for msg in event["forward"]:
                peer_id = msg.get("peer_id")
                cmid = msg.get("conversation_message_id")
                await self._delete_message(cmid, peer_id)

            return True

        return False


    async def _delete_message(self, cmid: int, peer_id: int):
        try:
            self.api.messages.delete(
                delete_for_all=1,
                peer_id=peer_id,
                cmids=cmid
            )

        except VkApiError as error:
            log_text = f"Could not delete <{cmid}> message: {error}"
            await logger.info(log_text)



class CopyCommand(BaseCommand):
    """Copy command.
    Copying text of forwarded message.
    """
    PERMISSION = 1
    NAME = "copy"

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("reply"):
            answer_text = event["reply"].get("text")
            self.api.messages.send(
                peer_id=event.get("peer_id"),
                random_id=0,
                message=answer_text
            )

            return True

        return False



class SettingsCommand(BaseCommand):
    """Setting command.
    Opens the settings selection menu.
    """
    PERMISSION = 2
    NAME = "settings"

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = "🚸 Выберите необходимую группу настроек:"

        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="Фильтры",
                    payload={
                        "call_action": "filters_settings",
                        "page": "1"
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_button(
                Callback(
                    label="Системы",
                    payload={
                        "call_action": "systems_settings",
                        "page": "1"
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class DelayCommand(BaseCommand):
    """Smd command.
    It sets a slow mode delay in minutes.
    """
    PERMISSION = 1
    NAME = "smd"

    async def _handle(self, event: dict, kwargs) -> bool:
        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="Медленный режим",
                    payload={
                        "call_action": "slow_mode_delay",
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_button(
                Callback(
                    label="Возраст аккаунта",
                    payload={
                        "call_action": "account_age_delay",
                    }
                ),
                ButtonColor.PRIMARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        answer_text = "🚸 Выберите настройку:"

        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True




class KickCommand(BaseCommand):
    """Kick command.
    Permanently removes user from conversation.
    """
    PERMISSION = 2
    NAME = "kick"

    #TODO: Добавить распознование владельца команды
    # (Во избежание самокика)
    async def _handle(self, event: dict, kwargs) -> bool:
        args = kwargs.get('argument_list')

        user_id = None

        if args and self.is_tag(args[0]):
            user_id = self.id_from_tag(args[0])

        elif event.get('reply', False):
            #TODO: Добавить удаление сообщения нарушителя.
            user_id = event.get('reply').get("from_id")

        if user_id is not None:
            try:
                self.api.messages.removeChatUser(
                    chat_id=event.get("chat_id"),
                    user_id=user_id
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
                db.execute.raw(
                    schema="toaster",
                    query=query
                )

                return True

            except VkApiError:
                return False

        return False
