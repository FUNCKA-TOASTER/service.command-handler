from vk_api import VkApiError
from logger import logger
import config
from db import db
from .abc import ABCHandler
from .commands import command_list


class CommandHandler(ABCHandler):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """

    async def _handle(self, event: dict, kwargs) -> bool:
        await self._delete_ownmessage(event)

        command_text: str = event.get("text")
        command_text_wo_prefix: str = command_text[1:]

        # command arguments
        arguments: list = command_text_wo_prefix.split(" ")[
            0 : config.MAX_ARG_COUNT + 1
        ]
        # command name
        command: str = arguments.pop(0)

        selected = command_list.get(command)

        if selected is None:
            log_text = f'Could not recognize command "{command}"'
            await logger.info(log_text)

            return False

        selected = selected(super().api)

        conversation_mark = await self._get_conv_mark(event)

        if conversation_mark not in selected.MARK:
            log_text = (
                f'Could not execute command in "{conversation_mark}" conversation'
            )
            await logger.info(log_text)

            return False

        user_lvl = await self._get_userlvl(event)

        if selected.PERMISSION <= user_lvl:
            result = await selected(event, argument_list=arguments)

            log_text = (
                f"Event <{event.get('event_id')}> with " f"arg list <{arguments}> "
            )

            if result:
                log_text += f"triggered /{selected.NAME} command."

            else:
                log_text += "did not triggered any command."

            await logger.info(log_text)
            return result

        else:
            log_text = (
                f"User {event.get('user_name')} have"
                " not permissions to execute this command."
            )
            await logger.info(log_text)

            return False

    async def _get_userlvl(self, event: dict) -> int:
        tech_admin = db.execute.select(
            schema="toaster_settings",
            table="staff",
            fields=("user_id",),
            user_id=event.get("user_id"),
            staff_role="TECH",
        )

        if bool(tech_admin):
            if event.get("user_id") == tech_admin[0][0]:
                return 2

        user_lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=("user_permission",),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
        )

        if bool(user_lvl):
            return int(user_lvl[0][0])

        return 0

    async def _delete_ownmessage(self, event: dict):
        try:
            super().api.messages.delete(
                delete_for_all=1, peer_id=event.get("peer_id"), cmids=event.get("cmid")
            )

        except VkApiError as error:
            log_text = f"Could not delete own command message: {error}"
            await logger.info(log_text)

    async def _get_conv_mark(self, event: dict):
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id"),
        )
        already_marked = bool(mark)

        if already_marked:
            return mark[0][0]

        return "UNDEFINED"


command_handler = CommandHandler()
