from typing import List, Optional, Iterable
from toaster.broker.events import Event


def requires_permission(permission_lvl: int):
    """DOCSTRING"""

    # TODO: Сделать нормальные сообщения
    exception_message = "Лвл малый!"

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                # TODO: Тут должны быть скрипты из алхимии для получения прав пользователя
                if event[0] >= permission_lvl:
                    return obj(name, args, event)
                else:
                    raise Exception(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                if event[0] >= permission_lvl:
                    return original(self, name, args, event)
                else:
                    raise Exception(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_mark(peer_mark: str):
    """DOCSTRING"""

    # TODO: Сделать нормальные сообщения
    exception_message = "Не та метка!"

    def decorator(obj: object):
        if not isinstance(obj, type):

            def wrapper(name: str, args: Optional[List[str]], event: Event):
                # TODO: Тут должны быть скрипты из алхимии для получения метки беседы
                if event[1] == peer_mark:
                    return obj(name, args, event)
                else:
                    raise Exception(exception_message)

            return wrapper

        else:
            original = obj.__call__

            def new_call(self, name: str, args: Optional[List[str]], event: Event):
                if event[1] == peer_mark:
                    return original(self, name, args, event)
                else:
                    raise Exception(exception_message)

            obj.__call__ = new_call
            return obj

    return decorator


def requires_attachments(attachemnts: Iterable):
    pass  # TODO: Write me
