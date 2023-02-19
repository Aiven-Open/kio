import enum
from dataclasses import Field
from dataclasses import is_dataclass
from types import EllipsisType
from types import NoneType
from types import UnionType
from typing import ClassVar
from typing import Protocol
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin

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
    entity = enum.auto()
    entity_tuple = enum.auto()


T = TypeVar("T")


def classify_field(field: Field[T]) -> tuple[FieldKind, type[T]]:
    type_origin = get_origin(field.type)

    if type_origin is not tuple:
        if is_dataclass(field.type):
            return FieldKind.entity, field.type
        else:
            return FieldKind.primitive, field.type

    type_args = get_args(field.type)

    match type_args:
        case (inner_type, EllipsisType()) if is_dataclass(inner_type):
            return FieldKind.entity_tuple, inner_type
        case (inner_type, EllipsisType()):
            return FieldKind.primitive_tuple, inner_type

    raise SchemaError(f"Field {field.name} has invalid tuple type args: {type_args}")
