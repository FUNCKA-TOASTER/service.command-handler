"""Module "rules".

File:
    rules.py

About:
    File describing rules that check the fulfillment
    of certain conditions immediately before executing
    a bot command.
"""

from typing import List, Optional, Callable
from funcka_bots.broker.events import Event
from db import TOASTER_DB
from toaster.enums import UserPermission, PeerMark
from toaster.scripts import (
    get_peer_mark,
    get_user_permission,
)


def requires_permission(permission_lvl: UserPermission) -> Callable:
    """Checks whether the user has the necessary rights
    to issue a given command.

    Args:
        permission_lvl (UserPermission): User permission lvl.

    Raises:
        PermissionError: Access rejected. Low level of access rights.

    Returns:
        Callable: Wrapper.
    """

    exception_message = "Access rejected. Low level of access rights."

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                user_permission = get_user_permission(
                    db_instance=TOASTER_DB,
                    uuid=event.user.uuid,
                    bpid=event.peer.bpid,
                )
                if user_permission.value >= permission_lvl.value:
                    return obj(name, args, event)

                else:
                    raise PermissionError(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                user_permission = get_user_permission(
                    db_instance=TOASTER_DB,
                    uuid=event.user.uuid,
                    bpid=event.peer.bpid,
                )
                if user_permission.value >= permission_lvl.value:
                    return original(self, name, args, event)

                else:
                    raise PermissionError(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_mark(*peer_marks: PeerMark) -> Callable:
    """Checks if the peer has the required
    tag to execute the command.

    Args:
        *peer_marks (PeerMark): Necessary peer marks.

    Raises:
        RuntimeError: Command execution aborted. Wrong peer mark.

    Returns:
        Callable: Wrapper.
    """

    exception_message = "Command execution aborted. Wrong peer mark."

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                mark = get_peer_mark(
                    db_instance=TOASTER_DB,
                    bpid=event.peer.bpid,
                )
                required = [peer_mark.value for peer_mark in peer_marks]
                if mark.value in required:
                    return obj(name, args, event)

                else:
                    raise RuntimeError(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                mark = get_peer_mark(
                    db_instance=TOASTER_DB,
                    bpid=event.peer.bpid,
                )
                required = [peer_mark.value for peer_mark in peer_marks]
                if mark.value in required:
                    return original(self, name, args, event)

                else:
                    raise RuntimeError(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_attachments(*attachments: str) -> Callable:
    """Checks whether the message that invoked the
    command has the required attachments.

    Args:
        *attachments (str): Necessary attachments names.

    Raises:
        ValueError: The message does not have attachments
        in the form of forwarding.

    Returns:
        Callable: Wrapper.
    """

    exception_message = (
        "The message does not have attachments in the form of forwarding."
    )

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                if set(attachments).issubset(event.message.attachments):
                    return obj(name, args, event)

                else:
                    raise ValueError(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                if set(attachments) & set(event.message.attachments):
                    return original(self, name, args, event)

                else:
                    raise ValueError(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator
