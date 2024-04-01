from .commands import (
    MarkCommand,
    PermissionCommand,
    GameCommand,
    SayCommand,
    DeleteCommand,
    CopyCommand,
    SettingsCommand,
    SlowModeDelayCommand,
    KickCommand
)


command_list = {
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand,
    GameCommand.NAME: GameCommand,
    SayCommand.NAME: SayCommand,
    DeleteCommand.NAME: DeleteCommand,
    CopyCommand.NAME: CopyCommand,
    SettingsCommand.NAME: SettingsCommand,
    SlowModeDelayCommand.NAME: SlowModeDelayCommand,
    KickCommand.NAME: KickCommand
}


__all__ = (
    "command_list",
)
