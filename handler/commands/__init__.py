from .commands import (
    MarkCommand,
    PermissionCommand,
    GameCommand,
    SayCommand,
    DeleteCommand,
    CopyCommand,
    SettingsCommand,
    DelayCommand,
    KickCommand,
    AddCurseWordCommand,
)


command_list = {
    PermissionCommand.NAME: PermissionCommand,
    MarkCommand.NAME: MarkCommand,
    GameCommand.NAME: GameCommand,
    SayCommand.NAME: SayCommand,
    DeleteCommand.NAME: DeleteCommand,
    CopyCommand.NAME: CopyCommand,
    SettingsCommand.NAME: SettingsCommand,
    DelayCommand.NAME: DelayCommand,
    KickCommand.NAME: KickCommand,
    AddCurseWordCommand.NAME: AddCurseWordCommand,
}


__all__ = ("command_list",)
