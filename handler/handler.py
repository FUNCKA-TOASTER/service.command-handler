from logger import logger
import config
from .abc import ABCHandler
from .commands import command_list


class CommandHandler(ABCHandler):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """
    #TODO: integrate DB
    # db = DataBase()

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

        #TODO: integrate DB
        #selected = selected(self.db, super().api)
        selected = selected(super().api)

        user_lvl = 2 #self.__get_userlvl(event)
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


    #TODO: integrate DB
    # async def __get_userlvl(self, event: dict) -> int:
    #     if event.from_id == config.TECH_ADMIN_ID:
    #         return 2

    #     user_lvl = self.db.permissions.select(
    #         fields=("user_permission",),
    #         conv_id=event.peer_id
    #     )

    #     if bool(user_lvl):
    #         return int(user_lvl[0][0])

    #     return 0



command_handler = CommandHandler()
