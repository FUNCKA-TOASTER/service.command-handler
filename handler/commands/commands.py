from tools.keyboards import (
    Keyboard,
    Callback,
    ButtonColor
)
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
        user_tag = kwargs.get('argument_list')[0]

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
