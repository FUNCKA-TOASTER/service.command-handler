from .commands import (
    TestCommand,
)


command_list = {
    TestCommand.name: TestCommand,
}


__all__ = ("command_list",)
