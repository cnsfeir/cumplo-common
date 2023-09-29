# pylint: disable=arguments-differ, invalid-name

from typing import Self

from cumplo_common.models import StrEnum
from cumplo_common.models.topic import Topic


class Template(StrEnum):
    _name_: str
    topic: Topic
    is_recurring: bool

    def __new__(cls, value: str, topic: Topic, is_recurring: bool) -> Self:
        obj = str.__new__(cls, value)
        obj.is_recurring = is_recurring
        obj._value_ = value
        obj.topic = topic
        return obj

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}.{self.topic.name}>"

    PROMISING = "promising", Topic.FUNDING_REQUESTS, True
    INITIALIZED = "initialized", Topic.INVESTMENTS, False
    SUCCESSFUL = "successful", Topic.INVESTMENTS, False
    FAILED = "failed", Topic.INVESTMENTS, False
