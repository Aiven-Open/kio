from dataclasses import Field
from dataclasses import fields
from typing import TypeVar

from typing_extensions import assert_never

from kio.schema.protocol import Entity

from . import encoders
from .encoders import Writable
from .encoders import Writer
from .encoders import compact_array_writer
from .encoders import legacy_array_writer
from .encoders import write_tagged_field
from .encoders import write_unsigned_varint
from .introspect import FieldKind
from .introspect import classify_field
from .introspect import get_field_tag
from .introspect import get_schema_field_type
from .introspect import is_optional


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
        case ("float64", _, False):
            return encoders.write_float64
        case ("string", True, False):
            return encoders.write_compact_string
        case ("string", True, True):
            return encoders.write_nullable_compact_string
        case ("string", False, False):
            return encoders.write_legacy_string
        case ("string", False, True):
            return encoders.write_nullable_legacy_string
        case ("bytes", True, False):
            return encoders.write_compact_string
        case ("bytes", True, True):
            return encoders.write_nullable_compact_string
        case ("bytes", False, False):
            return encoders.write_legacy_string
        case ("bytes", False, True):
            return encoders.write_nullable_legacy_string
        case ("records", _, True):
            return encoders.write_nullable_legacy_string
        case ("uuid", _, False):
            return encoders.write_uuid
        case ("bool", _, False):
            return encoders.write_boolean

    raise NotImplementedError(
        f"Failed identifying encoder for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_writer(
    field: Field[T],
    flexible: bool,
    is_request_header: bool,
) -> Writer[T]:
    # RequestHeader.client_id is special-cased by Kafka to always use the legacy string
    # format.
    # https://github.com/apache/kafka/blob/trunk/clients/src/main/resources/common/message/RequestHeader.json#L34-L38
    # It's odd that this choice is made, instead of addressing this only for the
    # ApiVersions request, because it's response is already special-cased.
    # https://github.com/apache/kafka/blob/trunk/generator/src/main/java/org/apache/kafka/message/ApiMessageTypeGenerator.java#L341
    if is_request_header and field.name == "client_id":
        return encoders.write_nullable_legacy_string  # type: ignore[return-value]

    field_kind, field_type = classify_field(field)
    array_writer = compact_array_writer if flexible else legacy_array_writer

    match field_kind:
        case FieldKind.primitive:
            return get_writer(
                kafka_type=get_schema_field_type(field),
                flexible=flexible,
                optional=is_optional(field),
            )
        case FieldKind.primitive_tuple:
            return array_writer(  # type: ignore[return-value]
                get_writer(
                    kafka_type=get_schema_field_type(field),
                    flexible=flexible,
                    optional=is_optional(field),
                )
            )
        case FieldKind.entity:
            return entity_writer(field_type)  # type: ignore[type-var]
        case FieldKind.entity_tuple:
            return array_writer(  # type: ignore[return-value]
                entity_writer(field_type)  # type: ignore[type-var]
            )
        case no_match:
            assert_never(no_match)


def _fqn(type_: type) -> str:
    return f"{type_.__module__}.{type_.__qualname__}"


E = TypeVar("E", bound=Entity)


def entity_writer(entity_type: type[E]) -> Writer[E]:
    def write_entity(buffer: Writable, entity: E) -> None:
        is_request_header = entity_type.__name__ == "RequestHeader"
        tag_writers = {}

        # Loop over all fields of the entity, serializing its values to the buffer and
        # keeping track of tagged fields.

        for field in fields(entity):
            field_writer = get_field_writer(
                field,
                flexible=entity.__flexible__,
                is_request_header=is_request_header,
            )
            field_value = getattr(entity, field.name)

            # Record non-default valued tagged fields and defer serialization.
            if (tag := get_field_tag(field)) is not None:
                if field_value != field.default:
                    tag_writers[tag] = (field_writer, field_value)
                continue

            field_writer(buffer, field_value)

        # For non-flexible entities we're done here.
        if not entity_type.__flexible__:
            # Assert we don't find tags for non-flexible models.
            assert not tag_writers
            return

        # Write number of tagged fields.
        write_unsigned_varint(buffer, len(tag_writers))

        # Serialize tagged fields. Order is important to fulfill spec.
        for field_tag in sorted(tag_writers.keys()):
            field_writer, value = tag_writers[field_tag]
            write_tagged_field(
                buffer=buffer,
                tag=field_tag,
                writer=field_writer,
                value=value,
            )

    return write_entity
