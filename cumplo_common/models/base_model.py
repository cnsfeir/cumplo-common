import enum
from abc import ABC
from collections.abc import Generator
from json import loads
from typing import Any, Self

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, model_validator
from ulid import ULID


class BaseModel(PydanticBaseModel, ABC):
    """Base class for all models in the project."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={ULID: str},
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        frozen=True,
    )

    def __hash__(self) -> int:
        return hash(self.model_dump_json(exclude={"id"}, exclude_none=True))

    def __str__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __repr__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()

    def json(self, *args: Any, **kwargs: Any) -> dict:  # type: ignore[override]
        """
        Return the model as a JSON parsed dict.

        Returns:
            dict:JSON parsed dict representation of the model

        """
        return loads(self.model_dump_json(*args, **kwargs, exclude_none=True))

    @classmethod
    def _remove_computed_fields(cls, core_schema: dict, values: list | dict) -> None:
        """Remove computed fields from the model schema."""
        schema = core_schema.get("schema", {}).get("schema", {})

        if schema.get("type") == "list" and schema.get("items_schema", {}).get("type") == "model":
            schema = schema.get("items_schema", {}).get("schema")
        else:
            values = [values]

        for field in schema.get("computed_fields", []):
            for element in values:
                element.pop(field.get("property_name"), None)

        for name, value in schema.get("fields", {}).items():
            for element in values:
                cls._remove_computed_fields(value, element.get(name))

    @model_validator(mode="before")
    @classmethod
    def _ignore_computed_fields(cls, values: dict) -> dict:
        """Ignores computed fields when validating the model."""
        if not (core_schema := cls.__dict__.get("__pydantic_core_schema__")):
            return values

        cls._remove_computed_fields(core_schema, values)
        return values


class StrEnum(enum.StrEnum):
    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        """Return the enum member case insensitively."""
        if isinstance(value, str):
            for member in cls:
                if member.casefold() == value.casefold():
                    return member
        return None

    @classmethod
    def has_member(cls, value: str) -> bool:
        """Whether the enum has a member case insensitively."""
        return any(value.casefold() == item.name.casefold() for item in cls)

    @classmethod
    def members(cls) -> Generator[Self, None, None]:
        """
        Yield the enum members.

        Yields:
            Self: The enum members.

        """
        yield from cls
