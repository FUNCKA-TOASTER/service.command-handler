from .commands import (
    TestCommand,
)


command_list = {
    TestCommand.COMMAND_NAME: TestCommand,
}


__all__ = (
    "command_list",
)
