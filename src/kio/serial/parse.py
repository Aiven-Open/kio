from dataclasses import Field
from dataclasses import fields
from dataclasses import is_dataclass
from types import EllipsisType
from typing import TypeVar
from typing import get_args
from typing import get_origin

from typing_extensions import assert_never

from kio.serial.decoders import Cursor
from kio.serial.decoders import Decoder
from kio.serial.decoders import compact_array_decoder
from kio.serial.decoders import skip_tagged_fields

from . import decoders
from .errors import SchemaError
from .introspect import Entity, classify_field, FieldKind
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
            return decoders.decode_legacy_string
        case ("string", False, True):
            return decoders.decode_nullable_legacy_string
        case ("uuid", _, False):
            return decoders.decode_uuid
        case ("bool", _, False):
            return decoders.decode_boolean

    raise NotImplementedError(
        f"Failed identifying decoder for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_decoder(entity_type: type[Entity], field: Field[T]) -> Decoder[T]:
    field_kind, field_type = classify_field(field)

    match field_kind:
        case FieldKind.primitive:
            return get_decoder(
                kafka_type=get_schema_field_type(field),
                flexible=entity_type.__flexible__,
                optional=is_optional(field),
            )
        case FieldKind.primitive_tuple:
            return compact_array_decoder(  # type: ignore[return-value]
                get_decoder(
                    kafka_type=get_schema_field_type(field),
                    flexible=entity_type.__flexible__,
                    optional=is_optional(field),
                )
            )
        case FieldKind.entity_tuple:
            return compact_array_decoder(  # type: ignore[return-value]
                entity_decoder(field_type)
            )
        case no_match:
            assert_never(no_match)


E = TypeVar("E", bound=Entity)


def entity_decoder(entity_type: type[E]) -> Decoder[E]:
    def decode_entity() -> Cursor[E]:
        kwargs = {}
        for field in fields(entity_type):
            kwargs[field.name] = yield get_field_decoder(entity_type, field)
        yield skip_tagged_fields
        return entity_type(**kwargs)

    return decode_entity
