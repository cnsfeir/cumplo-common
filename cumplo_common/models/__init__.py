import enum
from abc import ABC
from collections.abc import Generator
from json import loads
from typing import Any, Self

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, model_validator


class BaseModel(PydanticBaseModel, ABC):
    """Base class for all models in the project"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        frozen=True,
    )

    def __hash__(self) -> int:
        return hash(self.model_dump_json(exclude_none=True))

    def __str__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __repr__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def json(self, *args: Any, **kwargs: Any) -> dict:  # type: ignore[override]
        """
        Returns the model as a JSON parsed dict

        Returns:
            dict: JSON parsed dict representation of the model
        """
        return loads(self.model_dump_json(exclude_none=True, *args, **kwargs))

    @model_validator(mode="before")
    @classmethod
    def _ignore_computed_fields(cls, values: dict) -> dict:
        """
        Ignores computed fields when validating the model
        """
        if not (core_schema := cls.__dict__.get("__pydantic_core_schema__")):
            return values

        for definition in core_schema.get("definitions", [core_schema]):
            for field in definition.get("schema", {}).get("schema", {}).get("computed_fields", []):
                values.pop(field.get("property_name"), None)

        return values


class StrEnum(enum.StrEnum):
    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        """Returns the enum member case insensitively"""
        if isinstance(value, str):
            for member in cls:
                if member.casefold() == value.casefold():
                    return member
        return None

    @classmethod
    def has_member(cls, value: str) -> bool:
        """Whether the enum has a member case insensitively"""
        return any(value.casefold() == item.name.casefold() for item in cls)

    @classmethod
    def members(cls) -> Generator[Self, None, None]:
        """Yields the enum members"""
        for item in cls:
            yield item
