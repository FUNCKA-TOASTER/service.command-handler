from .commands import (
    Mark,
    Permission,
    Say,
    Delete,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
    Delete.NAME: Delete,
}


__all__ = ("command_list",)
