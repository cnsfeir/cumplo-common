# pylint: disable=arguments-differ, invalid-name

from enum import StrEnum
from typing import Self

from cumplo_common.models.topic import Topic


class Template(StrEnum):
    _name_: str
    topic: Topic

    def __new__(cls, value: str, topic: Topic) -> Self:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.topic = topic
        return obj

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}.{self.topic.name}>"

    PROMISING = "promising", Topic.FUNDING_REQUESTS
    INITIALIZED = "initialized", Topic.INVESTMENTS
    SUCCESSFUL = "successful", Topic.INVESTMENTS
    FAILED = "failed", Topic.INVESTMENTS
