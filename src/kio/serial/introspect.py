from dataclasses import Field, is_dataclass
from types import NoneType, EllipsisType
from types import UnionType
from typing import ClassVar, TypeVar
from typing import Protocol
from typing import Union
from typing import get_args
from typing import get_origin
import enum

from .errors import SchemaError


class Entity(Protocol):
    __flexible__: ClassVar[bool]


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
    if get_origin(field.type) not in [UnionType, Union]:
        return False
    return NoneType in get_args(field.type)


class FieldKind(enum.Enum):
    primitive = enum.auto()
    primitive_tuple = enum.auto()
    entity_tuple = enum.auto()


T = TypeVar("T")


def classify_field(field: Field[T]) -> tuple[FieldKind, T]:
    type_origin = get_origin(field.type)

    if type_origin is not tuple:
        # Fixme: Should support non-tuple nested entities!!
        return FieldKind.primitive, field.type

    type_args = get_args(field.type)

    match type_args:
        case (inner_type, EllipsisType()) if is_dataclass(inner_type):
            return FieldKind.entity_tuple, inner_type
        case (inner_type, EllipsisType()):
            return FieldKind.primitive_tuple, inner_type

    raise SchemaError(f"Field {field.name} has invalid tuple type args: {type_args}")
