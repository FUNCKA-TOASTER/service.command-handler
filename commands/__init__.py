from .commands import (
    TestCommand,
)


command_list = {
    TestCommand.NAME: TestCommand,
}


__all__ = ("command_list",)
