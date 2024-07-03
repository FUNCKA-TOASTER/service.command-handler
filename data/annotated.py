from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

# TODO: Комментарий
BPID = Annotated[int, mapped_column(BIGINT, ForeignKey("peers.bpid"), primary_key=True)]

# TODO: Комментарий
UUID = Annotated[int, mapped_column(BIGINT, ForeignKey("users.uuid"), primary_key=True)]
