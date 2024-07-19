from .commands import (
    Mark,
    Permission,
    Say,
    Delete,
    Game,
    Copy,
    Settings,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
    Delete.NAME: Delete,
    Game.NAME: Game,
    Copy.NAME: Copy,
    Settings.NAME: Settings,
}


__all__ = ("command_list",)
