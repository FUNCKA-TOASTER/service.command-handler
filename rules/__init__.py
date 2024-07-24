"""Module "rules".

File:
    __init__.py

About:
    Initializing the "rules" module.
"""

from .rules import (
    requires_mark,
    requires_permission,
    requires_attachments,
)


__all__ = (
    "requires_mark",
    "requires_permission",
    "requires_attachments",
)
