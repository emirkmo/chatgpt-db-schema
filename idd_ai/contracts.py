from typing import TypedDict, Any, Protocol, cast
from pydantic.dataclasses import dataclass
from pydantic import Field, create_model
from pydantic.main import ModelMetaclass
from functools import reduce


class ColumnSpecification(TypedDict):
    type: str
    description: str


class Contract(TypedDict):
    table: str
    table_description: str
    columns: dict[str, ColumnSpecification]


@dataclass
class TemplateTable:
    col1_name: str = Field(description="col1 description text.", default="")
    col2_name: str = Field(description="col2 description.", default="")

    # Raise error if someone tries to instantiate the template..
    def __post_init__(self):
        raise NotImplementedError("This is just a template for reference!")


def to_snake_case(str) -> str:
    """Convert CamelCase to snake_case (well actually `camel_case`)."""
    return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, str).lower()


class PydanticSchema(Protocol):
    __pydantic_model__: ModelMetaclass


class HasPydanticSchema(Protocol):
    """Interface for pydantic schema"""

    @staticmethod
    def schema(
        *,
        by_alias: bool = True,
        ref_template: "unicode" = "default_from_pydantic",  # type: ignore # noqa F821
    ) -> dict[str, Any]:
        ...


KNOWN_TYPES = {
    "int": int,
    "integer": int,
    "float": float,
    "number": float,
    "str": str,
    "string": str,
}

PYDANTIC_TYPES = {
    int: "integer",
    float: "float",
    str: "string",
}


def type_convert(type_str: str) -> str:
    if type_str in KNOWN_TYPES:
        return PYDANTIC_TYPES[KNOWN_TYPES[type_str]]
    return type_str


def dynamically_create_pydantic_model(
    table_name: str, fields: list[tuple[str, type | str, str]]
) -> HasPydanticSchema:
    """Create a pydantic model table from dynamically input fields."""
    return create_model(
        table_name,
        **{
            name: (KNOWN_TYPES[typ], Field(description=desc))
            for (name, typ, desc) in fields
            if isinstance(typ, str)
        },
    )


def make_contract(
    table: HasPydanticSchema, description: str = "This is a table with data."
) -> Contract:
    schema = table.schema()

    table_name = {
        "table": to_snake_case(schema["title"]),
        "table_description": description,
    }

    columns: dict[str, dict[str, str]] = {
        field_name: {
            "type": type_convert(typ_format),
            "description": properties["description"],
        }
        for field_name, properties in schema["properties"].items()
        if (typ_format := properties.get("format", properties["type"])) is not None
    }

    return cast(Contract, table_name | {"columns": columns})


def pydantic_model_from_contract(contract: Contract) -> HasPydanticSchema:
    fields = [
        (colname, properties["type"], properties["description"])
        for colname, properties in contract["columns"].items()
    ]

    return dynamically_create_pydantic_model(
        contract["table"],
        fields,  # type: ignore
    )
