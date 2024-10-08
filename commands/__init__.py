"""Module "commands".

File:
    __init__.py

About:
    Initializing the "commands" module.
"""

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
    Profile,
    AddCurseWord,
    AddLinkPattern,
    Kick,
    Warn,
    Unwarn,
)


command_list = {
    Mark.NAME: Mark,
    Permission.NAME: Permission,
    Say.NAME: Say,
    Game.NAME: Game,
    Copy.NAME: Copy,
    Settings.NAME: Settings,
    Delay.NAME: Delay,
    Expire.NAME: Expire,
    Punishment.NAME: Punishment,
    Profile.NAME: Profile,
    AddCurseWord.NAME: AddCurseWord,
    AddLinkPattern.NAME: AddLinkPattern,
    Kick.NAME: Kick,
    Warn.NAME: Warn,
    Unwarn.NAME: Unwarn,
    Delete.NAME: Delete,
}


__all__ = ("command_list",)
