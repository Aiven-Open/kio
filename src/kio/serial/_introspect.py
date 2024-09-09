from dataclasses import Field
from dataclasses import dataclass
from dataclasses import is_dataclass
from types import EllipsisType
from types import NoneType
from types import UnionType
from typing import ClassVar
from typing import TypeAlias
from typing import TypeVar
from typing import Union
from typing import final
from typing import get_args
from typing import get_origin

from kio.static.protocol import Entity

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


@final
@dataclass(frozen=True, slots=True)
class PrimitiveField:
    is_array: ClassVar = False
    type_: type


@final
@dataclass(frozen=True, slots=True)
class PrimitiveTupleField:
    is_array: ClassVar = True
    type_: type


@final
@dataclass(frozen=True, slots=True)
class EntityField:
    is_array: ClassVar = False
    type_: type[Entity]


@final
@dataclass(frozen=True, slots=True)
class EntityTupleField:
    is_array: ClassVar = True
    type_: type[Entity]


FieldClass: TypeAlias = (
    PrimitiveField | PrimitiveTupleField | EntityField | EntityTupleField
)


T = TypeVar("T")


def classify_field(field: Field[T]) -> FieldClass:
    return _classify_field(field.type, field.name)


def _classify_field(field_type: type[T], field_name: str) -> FieldClass:
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
            EntityField(field_type)  # type: ignore[arg-type]
            if is_dataclass(field_type)
            else PrimitiveField(field_type)
        )

    type_args = get_args(field_type)

    match type_args:
        case (inner_type, EllipsisType()) if is_dataclass(inner_type):
            return EntityTupleField(inner_type)
        case (inner_type, EllipsisType()):
            return PrimitiveTupleField(inner_type)

    raise SchemaError(f"Field {field_name} has invalid tuple type args: {type_args}")


def get_field_tag(field: Field) -> int | None:
    try:
        return int(field.metadata["tag"])
    except KeyError:
        return None
