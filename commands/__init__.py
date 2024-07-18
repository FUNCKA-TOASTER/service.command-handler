from .commands import (
    Mark,
    Permission,
    Say,
    Delete,
    Game,
    Copy,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
    Delete.NAME: Delete,
    Game.NAME: Game,
    Copy.NAME: Copy,
}


__all__ = ("command_list",)
