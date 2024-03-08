from .commands import (
    TestCommand,
    MarkCommand,
    PermissionCommand
)


command_list = {
    TestCommand.name: TestCommand,
    PermissionCommand.name: PermissionCommand,
    MarkCommand.name: MarkCommand
}


__all__ = (
    "command_list",
)
