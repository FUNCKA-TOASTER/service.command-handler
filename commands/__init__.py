from .commands import (
    Test,
    Mark,
)


command_list = {
    Test.NAME: Test,
    Mark.NAME: Mark,
}


__all__ = ("command_list",)
