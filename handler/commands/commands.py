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
    COMMAND_NAME = "test"
    _permission_lvl = 2

    async def _handle(self, event: dict, kwargs) -> bool:
        answer_text = f"Вызвана комманда <{self.COMMAND_NAME}> " \
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
        print(keyboard)
        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True
