from typing import Tuple, List, NoReturn, Optional, Any
from loguru import logger
from vk_api import VkApi
from toaster.broker.events import Event
from commands import command_list
import config


CommandData = Tuple[str, List[str]]


class CommandHandler:
    """DOCSTRING"""

    def __call__(self, event: Event) -> None:
        try:
            command_data = self._recognize_command(event)
            self._execute(**command_data)

        except Exception as error:
            logger.error(error)

    # TODO: В будущем система взаимодействия с обьектом команды будет изменена
    # Так что это надо будет поправить.
    def _execute(self, name: str, args: List[str], event: Event) -> Optional[NoReturn]:
        selected = command_list.get(name)
        if selected is None:
            raise KeyError(f'Could not recognize command "{name}"')

        comamnd_obj = selected(self._get_api())
        comamnd_obj(event, argument_list=args)

    def _recognize_command(self, event: Event) -> CommandData:
        command_text = event.message.text
        if not command_text:
            raise ValueError("Message does not contain any text.")

        command_text_wo_prefix = command_text[1:]
        arguments = command_text_wo_prefix.split(" ")[0 : config.MAX_ARG_COUNT + 1]
        command = arguments.pop(0)

        return (command, arguments)

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        self.api = session.get_api()
