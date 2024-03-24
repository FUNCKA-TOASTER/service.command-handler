from vk_api import VkApiError
from tools.keyboards import (
    Keyboard,
    Callback,
    ButtonColor
)
from logger import logger
from .base import BaseCommand


class TestCommand(BaseCommand):
    """Test command.
    Sends test content to the chat where the command was called:
        Message
        Attachments
        Keyboard
        e.t.c
    """
    PERMISSION = 2
    NAME = "test"

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = f"Вызвана комманда <{self.NAME}> " \
                      f"с аргументами {kwargs.get('argument_list')}."

        keyboard = (
            Keyboard(
                inline=True,
                one_time=False,
                owner_id=event.get("user_id")
            )
            .add_row()
            .add_button(
                Callback(
                    label="Позитив",
                    payload={
                        "call_action": "positive_test"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Негатив",
                    payload={
                        "call_action": "negative_test"
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
                        "call_action": "mark_as_chat"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="LOG",
                    payload={
                        "call_action": "mark_as_log"
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
                        "call_action": "set_moderator_permission",
                        "target": self.id_from_tag(user_tag)
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Администратор",
                    payload={
                        "call_action": "set_administrator_permission",
                        "target": self.id_from_tag(user_tag)
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Пользователь",
                    payload={
                        "call_action": "set_user_permission",
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
    Sends a message from the face of the bot.
    Maximum 10 words.
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
            peer_id = event.get("peer_id")
            for msg in event["forward"]:
                cmid = msg.get("conversation_message_id")
                await self._delete_message(cmid, peer_id)

            return True

        else:
            return False


    async def _delete_message(self, cmid: int, peer_id: int):
        try:
            self.api.messages.delete(
                delete_for_all=1,
                peer_id=peer_id,
                cmid=cmid
            )

        except VkApiError as error:
            log_text = f"Could not delete <{cmid}> message: {error}"
            await logger.info(log_text)
