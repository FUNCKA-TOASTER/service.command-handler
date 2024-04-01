from .commands import (
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
