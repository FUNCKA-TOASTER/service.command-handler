from .commands import (
    Mark,
    Permission,
    Say,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
}


__all__ = ("command_list",)
