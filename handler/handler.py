from typing import Tuple, List, NoReturn, Optional, Any, Union
from loguru import logger
from vk_api import VkApi, VkApiError
from toaster.broker.events import Event
from commands import command_list
import config


CommandData = Tuple[str, List[str]]
ExecResult = Optional[Union[bool, NoReturn]]


class CommandHandler:
    """DOCSTRING"""

    def __call__(self, event: Event) -> None:
        try:
            name, args = self._recognize_command(event)
            if self._execute(name, args, event):
                logger.info(f"Command '{name}' executed.")

        except Exception as error:
            logger.error(error)

        finally:
            self._delete_own_message(event)

    def _execute(self, name: str, args: List[str], event: Event) -> ExecResult:
        selected = command_list.get(name)
        if selected is None:
            raise KeyError(f'Could not recognize command "{name}"')

        comamnd_obj = selected(self._get_api())
        return comamnd_obj(name, args, event)

    def _recognize_command(self, event: Event) -> CommandData:
        command_text = event.message.text
        if not command_text:
            raise ValueError("Message does not contain any text.")

        command_text_wo_prefix = command_text[1:]
        arguments = command_text_wo_prefix.split(" ")[0 : config.MAX_ARG_COUNT + 1]
        command = arguments.pop(0)

        return (command, arguments)

    def _delete_own_message(self, event: Event):
        try:
            api = self._get_api()
            api.messages.delete(
                delete_for_all=1,
                peer_id=event.peer.bpid,
                cmids=event.message.cmid,
            )

        except VkApiError as error:
            logger.info(f"Could not delete own command message: {error}")

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
