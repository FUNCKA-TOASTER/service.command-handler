from .commands import (
    TestCommand,
    MarkCommand,
    PermissionCommand
)


command_list = {
    TestCommand.NAME: TestCommand,
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand
}


__all__ = (
    "command_list",
)
