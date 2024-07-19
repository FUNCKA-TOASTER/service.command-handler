from .commands import (
    Mark,
    Permission,
    Say,
    Delete,
    Game,
    Copy,
    Settings,
    Delay,
    Expire,
    Punishment,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
    Delete.NAME: Delete,
    Game.NAME: Game,
    Copy.NAME: Copy,
    Settings.NAME: Settings,
    Delay.NAME: Delay,
    Expire.NAME: Expire,
    Punishment.NAME: Punishment,
}


__all__ = ("command_list",)
