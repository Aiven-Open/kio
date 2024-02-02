import enum

from dataclasses import Field
from dataclasses import is_dataclass
from types import EllipsisType
from types import NoneType
from types import UnionType
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin

from .errors import SchemaError


def get_schema_field_type(field: Field) -> str:
    try:
        value = field.metadata["kafka_type"]
    except KeyError as exception:
        raise SchemaError(
            f"Missing `kafka_type` in metadata for {field=}"
        ) from exception
    if not isinstance(value, str):
        raise SchemaError(f"`kafka_type` must be of type str, found {type(value)}")
    return value


def is_optional(field: Field) -> bool:
    if get_origin(field.type) is tuple:
        type_args = get_args(field.type)
        match type_args:
            case (inner_type, EllipsisType()):
                inner_type = inner_type
            case _:
                raise SchemaError(
                    f"Field {field.name} has invalid tuple type args: {type_args}"
                )
    else:
        inner_type = field.type

    if get_origin(inner_type) not in [UnionType, Union]:
        return False
    return NoneType in get_args(inner_type)


class FieldKind(enum.Enum):
    primitive = enum.auto()
    primitive_tuple = enum.auto()
    entity = enum.auto()
    entity_tuple = enum.auto()


T = TypeVar("T")


def classify_field(field: Field[T]) -> tuple[FieldKind, type[T]]:
    return _classify_field(field.type, field.name)


def _classify_field(field_type: type[T], field_name: str) -> tuple[FieldKind, type[T]]:
    type_origin = get_origin(field_type)

    if type_origin is UnionType:
        try:
            a, b = get_args(field_type)
        except ValueError:
            raise SchemaError(
                f"Field {field_name} has unsupported union type: {field_type}"
            ) from None

        if a is NoneType:
            inner_type = b
        elif b is NoneType:
            inner_type = a
        else:
            raise SchemaError("Only union with None is supported")

        return _classify_field(inner_type, f"{field_name}.nested")

    if type_origin is not tuple:
        return (
            (FieldKind.entity, field_type)  # type: ignore[return-value]
            if is_dataclass(field_type)
            else (FieldKind.primitive, field_type)
        )

    type_args = get_args(field_type)

    match type_args:
        case (inner_type, EllipsisType()) if is_dataclass(inner_type):
            return FieldKind.entity_tuple, inner_type
        case (inner_type, EllipsisType()):
            return FieldKind.primitive_tuple, inner_type

    raise SchemaError(f"Field {field_name} has invalid tuple type args: {type_args}")


def get_field_tag(field: Field) -> int | None:
    try:
        return int(field.metadata["tag"])
    except KeyError:
        return None
