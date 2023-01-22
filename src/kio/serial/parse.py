from dataclasses import Field
from dataclasses import fields
from dataclasses import is_dataclass
from types import EllipsisType
from typing import TypeVar
from typing import get_args
from typing import get_origin

from kio.serial.decoders import Cursor
from kio.serial.decoders import Decoder
from kio.serial.decoders import compact_array_decoder
from kio.serial.decoders import skip_tagged_fields

from . import decoders
from .errors import SchemaError
from .introspect import Entity
from .introspect import get_schema_field_type
from .introspect import is_optional


def get_decoder(
    kafka_type: str,
    flexible: bool,
    optional: bool,
) -> decoders.Decoder:
    match (kafka_type, flexible, optional):
        case ("int8", _, False):
            return decoders.decode_int8
        case ("int16", _, False):
            return decoders.decode_int16
        case ("int32", _, False):
            return decoders.decode_int32
        case ("int64", _, False):
            return decoders.decode_int64
        case ("uint8", _, False):
            return decoders.decode_uint8
        case ("uint16", _, False):
            return decoders.decode_uint16
        case ("uint32", _, False):
            return decoders.decode_uint32
        case ("uint64", _, False):
            return decoders.decode_uint64
        case ("string", True, False):
            return decoders.decode_compact_string
        case ("string", True, True):
            return decoders.decode_compact_string_nullable
        case ("string", False, False):
            return decoders.decode_string
        case ("string", False, True):
            return decoders.decode_string_nullable
        case ("uuid", _, False):
            return decoders.decode_uuid
        case ("bool", _, False):
            return decoders.decode_boolean

    raise NotImplementedError(
        f"Failed identifying decoder for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_decoder(entity_type: type[Entity], field: Field[T]) -> Decoder[T]:
    type_origin = get_origin(field.type)

    if type_origin is not tuple:
        # Field is a simple primitive field.
        return get_decoder(
            kafka_type=get_schema_field_type(field),
            flexible=entity_type.__flexible__,
            optional=is_optional(field),
        )

    type_args = get_args(field.type)

    match type_args:
        # Field is a homogenous tuple of a nested entity.
        case (inner_type, EllipsisType()) if is_dataclass(inner_type):
            return compact_array_decoder(entity_decoder(inner_type))  # type: ignore[return-value]
        # Field is a homogenous tuple of primitives.
        case (_, EllipsisType()):
            return compact_array_decoder(  # type: ignore[return-value]
                get_decoder(
                    kafka_type=get_schema_field_type(field),
                    flexible=entity_type.__flexible__,
                    optional=is_optional(field),
                )
            )

    raise SchemaError(f"Field {field.name} has invalid tuple type args: {type_args}")


E = TypeVar("E", bound=Entity)


def entity_decoder(entity_type: type[E]) -> Decoder[E]:
    def decode_entity() -> Cursor[E]:
        kwargs = {}
        for field in fields(entity_type):
            kwargs[field.name] = yield get_field_decoder(entity_type, field)
        yield skip_tagged_fields
        return entity_type(**kwargs)

    return decode_entity
