"""Module "handler".

File:
    handler.py

About:
    File describing command handler class.
"""

import json
from typing import Tuple, List, NoReturn, Optional, Any, Union
from loguru import logger
from vk_api import VkApi, VkApiError
from db import TOASTER_DB
from funcka_bots.broker.events import Event
from funcka_bots.handler import ABCHandler
from toaster.scripts import get_log_peers
from commands import command_list
import config


CommandData = Tuple[str, List[str]]
ExecResult = Optional[Union[bool, NoReturn]]


class CommandHandler(ABCHandler):
    """Command handler class."""

    def __call__(self, event: Event) -> None:
        try:
            name, args = self._recognize_command(event)
            if self._execute(name, args, event):
                logger.info(f"Command '{name}' executed with args {args}.")
                self._alert_about_execution(event, name, args)
                return

        except Exception as error:
            logger.error(error)

        else:
            logger.info("Not a single command was executed.")

        finally:
            self._delete_own_message(event)

    def _execute(self, name: str, args: List[str], event: Event) -> ExecResult:
        selected = command_list.get(name)
        if selected is None:
            raise KeyError(f"Could not recognize command '{name}'")

        comamnd_obj = selected(self._get_api())
        return comamnd_obj(name, args, event)

    @staticmethod
    def _recognize_command(event: Event) -> CommandData:
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

    def _alert_about_execution(self, event: Event, name: str, args: List[str]):
        answer_text = (
            f"[id{event.user.uuid}|{event.user.name}] вызвал команду. \n"
            f"Беседа: {event.peer.name} \n"
            f"Команда: {name} \n"
        )

        if args:
            answer_text += f"Аргументы: {args}"

        forward = {
            "peer_id": event.peer.bpid,
            "conversation_message_ids": None,
        }

        if event.message.reply:
            forward["conversation_message_ids"] = [event.message.reply.cmid]

        elif event.message.forward:
            cmids = [reply.cmid for reply in event.message.forward]
            forward["conversation_message_ids"] = cmids

        api = self._get_api()

        for bpid in get_log_peers(db_instance=TOASTER_DB):
            api.messages.send(
                peer_ids=bpid,
                random_id=0,
                message=answer_text,
                forward=json.dumps(forward),
            )

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
