from abc import ABC
from json import loads
from typing import Any

import pydantic
from pydantic import ConfigDict, model_validator
from ulid import ULID


class BaseModel(pydantic.BaseModel, ABC):
    """Base class for all models in the project."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={ULID: str},
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
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
