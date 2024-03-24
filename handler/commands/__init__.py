from .commands import (
    TestCommand,
    MarkCommand,
    PermissionCommand,
    GameCommand,
    SayCommand,
    DeleteCommand
)


command_list = {
    TestCommand.NAME: TestCommand,
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand,
    GameCommand.NAME: GameCommand,
    SayCommand.NAME: SayCommand,
    DeleteCommand.NAME: DeleteCommand
}


__all__ = (
    "command_list",
)
