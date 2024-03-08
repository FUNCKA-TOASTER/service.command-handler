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
        command_text: str = event.get("text")
        command_text_wo_prefix: str = command_text[1:]

        #command arguments
        arguments: list = command_text_wo_prefix.split(" ")[0:config.MAX_ARG_COUNT+1]
        #command name
        command: str = arguments.pop(0)

        selected = command_list.get(command)

        if selected is None:
            log_text = f"Could not recognize command {command}"
            await logger.info(log_text)

            return False

        selected = selected(super().api)

        user_lvl = self.__get_userlvl(event)
        if selected.permission <= user_lvl:
            result = await selected(event, argument_list=arguments)

            log_text = f"Event <{event.get('event_id')}> with " \
                       f"arg list <{arguments}> "

            if result:
                log_text += f"triggered /{selected.COMMAND_NAME} command."
            else:
                log_text += "did not triggered any command."

            await logger.info(log_text)
            return result

        return False


    async def __get_userlvl(self, event: dict) -> int:
        tech_admin = db.execute.select(
            schema="toaster_settings",
            table="staff",
            fields=("user_id",),
            user_id=event.get("from_id"),
            staff_role="TECH"
        )

        if bool(tech_admin):
            if event.get("from_id") == tech_admin[0][0]:
                return 2

        user_lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=("user_permission",),
            conv_id=event.peer_id
        )

        if bool(user_lvl):
            return int(user_lvl[0][0])

        return 0



command_handler = CommandHandler()
