# pylint: disable=arguments-differ, invalid-name

from typing import Self

from cumplo_common.models.base_model import StrEnum
from cumplo_common.models.subject import Subject


class Template(StrEnum):
    _name_: str
    subject: Subject
    is_recurring: bool

    def __new__(cls, value: str, subject: Subject, is_recurring: bool) -> Self:  # noqa: FBT001
        obj = str.__new__(cls, value)
        obj.is_recurring = is_recurring
        obj._value_ = value
        obj.subject = subject
        return obj

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}.{self.subject.name}>"

    PROMISING = "promising", Subject.FUNDING_REQUESTS, True
    INITIALIZED = "initialized", Subject.INVESTMENTS, False
    SUCCESSFUL = "successful", Subject.INVESTMENTS, False
    FAILED = "failed", Subject.INVESTMENTS, False
