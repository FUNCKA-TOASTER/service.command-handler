from .commands import (
    Mark,
    Permission,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
}


__all__ = ("command_list",)
