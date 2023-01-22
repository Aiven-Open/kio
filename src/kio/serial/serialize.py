from dataclasses import Field
from dataclasses import fields
from typing import TypeVar

from typing_extensions import assert_never

from kio.serial import encoders
from kio.serial.encoders import Writable
from kio.serial.encoders import Writer
from kio.serial.encoders import compact_array_writer
from kio.serial.encoders import write_empty_tagged_fields
from kio.serial.introspect import Entity
from kio.serial.introspect import FieldKind
from kio.serial.introspect import classify_field
from kio.serial.introspect import get_schema_field_type
from kio.serial.introspect import is_optional


def get_writer(
    kafka_type: str,
    flexible: bool,
    optional: bool,
) -> Writer:
    match (kafka_type, flexible, optional):
        case ("int8", _, False):
            return encoders.write_int8
        case ("int16", _, False):
            return encoders.write_int16
        case ("int32", _, False):
            return encoders.write_int32
        case ("int64", _, False):
            return encoders.write_int64
        case ("uint8", _, False):
            return encoders.write_uint8
        case ("uint16", _, False):
            return encoders.write_uint16
        case ("uint32", _, False):
            return encoders.write_uint32
        case ("uint64", _, False):
            return encoders.write_uint64
        case ("string", True, False):
            return encoders.write_compact_string
        case ("string", True, True):
            return encoders.write_nullable_compact_string
        case ("string", False, False):
            return encoders.write_legacy_string
        case ("string", False, True):
            return encoders.write_nullable_legacy_string
        case ("uuid", _, False):
            return encoders.write_uuid
        case ("bool", _, False):
            return encoders.write_boolean

    raise NotImplementedError(
        f"Failed identifying decoder for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_writer(field: Field[T], flexible: bool) -> Writer[T]:
    field_kind, field_type = classify_field(field)

    match field_kind:
        case FieldKind.primitive:
            return get_writer(
                kafka_type=get_schema_field_type(field),
                flexible=flexible,
                optional=is_optional(field),
            )
        case FieldKind.primitive_tuple:
            return compact_array_writer(  # type: ignore[return-value]
                get_writer(
                    kafka_type=get_schema_field_type(field),
                    flexible=flexible,
                    optional=is_optional(field),
                )
            )
        case FieldKind.entity_tuple:
            return compact_array_writer(  # type: ignore[return-value]
                entity_writer(field_type)  # type: ignore[type-var]
            )
        case no_match:
            assert_never(no_match)


E = TypeVar("E", bound=Entity)


def entity_writer(entity_type: type[E]) -> Writer[E]:
    flexible = entity_type.__flexible__

    def write_entity(buffer: Writable, entity: E) -> None:
        for field in fields(entity):
            field_writer = get_field_writer(field, flexible=flexible)
            field_writer(buffer, getattr(entity, field.name))
        write_empty_tagged_fields(buffer)

    return write_entity
