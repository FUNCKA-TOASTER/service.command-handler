from typing import List, Optional, Iterable
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
                user_permission = get_user_permission(TOASTER_DB, event)
                if user_permission >= permission_lvl.value:
                    return obj(name, args, event)

                else:
                    raise PermissionError(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                user_permission = get_user_permission(TOASTER_DB, event)
                if user_permission >= permission_lvl:
                    return original(self, name, args, event)

                else:
                    raise PermissionError(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_mark(peer_mark: PeerMark):
    """DOCSTRING"""

    exception_message = "Command execution aborted. Wrong peer mark."

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                mark = get_peer_mark(TOASTER_DB, event)
                if mark == peer_mark.value:
                    return obj(name, args, event)

                else:
                    raise RuntimeError(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                mark = get_peer_mark(TOASTER_DB, event)
                if mark == peer_mark:
                    return original(self, name, args, event)

                else:
                    raise RuntimeError(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_attachments(attachemnts: Iterable):
    pass  # TODO: Write me
