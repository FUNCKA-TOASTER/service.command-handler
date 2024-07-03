from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy.dialects.mysql import (
    TINYINT,
    BIGINT,
    INTEGER,
    VARCHAR,
    DATETIME,
)


BaseModel = declarative_base()

# TODO: Прописать ondelete в местах, где это нужно
# TODO: Задать Annotated для повторяющихся типов


# Таблицы основных элементов
class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    first_name: Mapped[str] = mapped_column(VARCHAR(100))
    last_name: Mapped[str] = mapped_column(VARCHAR(100))
    url: Mapped[str] = mapped_column(VARCHAR(255))


class PeerMark(Enum):
    LOG = "LOG"
    CHAT = "CHAT"


class Peer(BaseModel):
    __tablename__ = "peers"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    mark: Mapped[PeerMark]


# Таблицы данных о пользователе и сообщениях
class UserPermission(Enum):
    user = 0
    moderator = 1
    administrator = 2


class Permission(BaseModel):
    __tablename__ = "permissions"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    uuid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.uuid"), primary_key=True
    )
    permission: Mapped[UserPermission]


class Warn(BaseModel):
    __tablename__ = "warns"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    uuid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.uuid"), primary_key=True
    )
    points: Mapped[int] = mapped_column(TINYINT(10))
    expired: Mapped[datetime] = mapped_column(DATETIME)


class Session(BaseModel):
    __tablename__ = "sessions"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    cmid: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    expired: Mapped[datetime] = mapped_column(DATETIME)


class Message(BaseModel):
    __tablename__ = "messages"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    uuid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.uuid"), primary_key=True
    )
    count: Mapped[int] = mapped_column(BIGINT)


class Queue(BaseModel):
    __tablename__ = "queues"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    uuid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.uuid"), primary_key=True
    )
    expired: Mapped[int] = mapped_column(DATETIME)


# Таблицы настроект узлов
class SettingStatus(Enum):
    active = True
    inactive = False


class SettingDestination(Enum):
    filter = "filter"
    system = "system"


class Setting(BaseModel):
    __tablename__ = "settings"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    name: Mapped[str] = mapped_column(VARCHAR(30), primary_key=True)
    status: Mapped[SettingStatus]
    destination: Mapped[SettingDestination]
    points: Mapped[int] = mapped_column(TINYINT(10))


class Cursed(BaseModel):
    __tablename__ = "curses"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    word: Mapped[str] = mapped_column(VARCHAR(40), primary_key=True)


class Delay(BaseModel):
    __tablename__ = "delays"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    setting: Mapped[str] = mapped_column(VARCHAR(30), primary_key=True)
    delay: Mapped[int] = mapped_column(INTEGER)


class UrlType(Enum):
    url = "domain"
    domain = "url"


class UrlStatus(Enum):
    allowed = "allowed"
    forbidden = "forbidden"


class Url(BaseModel):
    __tablename__ = "urls"

    bpid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("peers.bpid"), primary_key=True
    )
    type: Mapped[UrlType] = mapped_column(primary_key=True)
    pattern: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    status: Mapped[UrlStatus]


class StaffRole(Enum):
    TECH = "TECH"
    SYS = "SYS"
    ADM = "ADM"


class Staff(BaseModel):
    __tablename__ = "staffs"

    uuid: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.uuid"), primary_key=True, unique=True
    )
    role: Mapped[StaffRole]
