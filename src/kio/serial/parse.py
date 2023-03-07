from dataclasses import Field
from dataclasses import fields
from typing import TypeVar

from typing_extensions import assert_never

from kio.serial.decoders import Cursor
from kio.serial.decoders import Decoder
from kio.serial.decoders import compact_array_decoder
from kio.serial.decoders import decode_unsigned_varint

from . import decoders
from .introspect import Entity
from .introspect import FieldKind
from .introspect import classify_field
from .introspect import get_field_tag
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
        case ("float64", _, False):
            return decoders.decode_float64
        case ("string", True, False):
            return decoders.decode_compact_string
        case ("string", True, True):
            return decoders.decode_compact_string_nullable
        case ("string", False, False):
            return decoders.decode_legacy_string
        case ("string", False, True):
            return decoders.decode_nullable_legacy_string
        case ("bytes", True, False):
            return decoders.decode_compact_string_as_bytes
        case ("bytes", True, True):
            return decoders.decode_compact_string_as_bytes_nullable
        case ("bytes", False, False):
            return decoders.decode_legacy_bytes
        case ("bytes", False, True):
            return decoders.decode_nullable_legacy_bytes
        case ("records", _, True):
            return decoders.decode_nullable_legacy_bytes
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
        case FieldKind.entity:
            return entity_decoder(field_type)  # type: ignore[type-var]
        case FieldKind.entity_tuple:
            return compact_array_decoder(  # type: ignore[return-value]
                entity_decoder(field_type)  # type: ignore[type-var]
            )
        case no_match:
            assert_never(no_match)


E = TypeVar("E", bound=Entity)


def entity_decoder(entity_type: type[E]) -> Decoder[E]:
    def decode_entity() -> Cursor[E]:
        kwargs = {}
        tagged_fields: dict[int, Field] = {}

        for field in fields(entity_type):
            if (tag := get_field_tag(field)) is not None:
                tagged_fields[tag] = field
            else:
                kwargs[field.name] = yield get_field_decoder(entity_type, field)

        if not entity_type.__flexible__:
            # Assert we don't find tags for non-flexible models.
            assert not tagged_fields
            return entity_type(**kwargs)

        num_tagged_fields = yield decode_unsigned_varint

        for _ in range(num_tagged_fields):
            field_tag = yield decode_unsigned_varint
            yield decode_unsigned_varint  # field length
            field = tagged_fields[field_tag]
            kwargs[field.name] = yield get_field_decoder(entity_type, field)

        return entity_type(**kwargs)

    return decode_entity
