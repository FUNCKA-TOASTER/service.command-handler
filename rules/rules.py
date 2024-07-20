from typing import List, Optional
from toaster.broker.events import Event
from data import UserPermission, PeerMark
from data import TOASTER_DB
from data.scripts import (
    get_peer_mark,
    get_user_permission,
)


def requires_permission(permission_lvl: UserPermission):
    """DOCSTRING"""

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


def requires_mark(*peer_marks: PeerMark):
    """DOCSTRING"""

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


def requires_attachments(*attachments: str):
    """DOCSTRING"""

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
