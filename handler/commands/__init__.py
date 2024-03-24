from .commands import (
    TestCommand,
    MarkCommand,
    PermissionCommand,
    GameCommand
)


command_list = {
    TestCommand.NAME: TestCommand,
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand,
    GameCommand.NAME: GameCommand
}


__all__ = (
    "command_list",
)
