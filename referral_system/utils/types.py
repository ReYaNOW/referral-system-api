from enum import StrEnum, auto

from sqlalchemy.sql import Delete, Insert, Select, Update

SQLStatement = Select | Insert | Update | Delete


class ResultType(StrEnum):
    ONE = auto()
    MANY = auto()
    NONE = auto()
