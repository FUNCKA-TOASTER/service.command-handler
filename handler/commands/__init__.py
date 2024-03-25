from .commands import (
    TestCommand,
    MarkCommand,
    PermissionCommand,
    GameCommand,
    SayCommand,
    DeleteCommand,
    CopyCommand,
    SettingsCommand,
    SlowModeDelayCommand
)


command_list = {
    TestCommand.NAME: TestCommand,
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand,
    GameCommand.NAME: GameCommand,
    SayCommand.NAME: SayCommand,
    DeleteCommand.NAME: DeleteCommand,
    CopyCommand.NAME: CopyCommand,
    SettingsCommand.NAME: SettingsCommand,
    SlowModeDelayCommand.NAME: SlowModeDelayCommand
}


__all__ = (
    "command_list",
)
