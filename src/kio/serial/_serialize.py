import io

from dataclasses import Field
from dataclasses import fields
from typing import Literal
from typing import TypeVar
from typing import assert_never
from typing import overload

from kio._utils import cache
from kio.static.protocol import Entity

from . import writers
from ._introspect import EntityField
from ._introspect import EntityTupleField
from ._introspect import PrimitiveField
from ._introspect import PrimitiveTupleField
from ._introspect import classify_field
from ._introspect import get_field_tag
from ._introspect import get_schema_field_type
from ._introspect import is_optional
from ._shared import NullableEntityMarker
from .writers import Writable
from .writers import Writer
from .writers import compact_array_writer
from .writers import legacy_array_writer
from .writers import write_int8
from .writers import write_tagged_field
from .writers import write_unsigned_varint


def get_writer(
    kafka_type: str,
    flexible: bool,
    optional: bool,
) -> Writer:
    match (kafka_type, flexible, optional):
        case ("int8", _, False):
            return writers.write_int8
        case ("int16", _, False):
            return writers.write_int16
        case ("int32", _, False):
            return writers.write_int32
        case ("int64", _, False):
            return writers.write_int64
        case ("uint8", _, False):
            return writers.write_uint8
        case ("uint16", _, False):
            return writers.write_uint16
        case ("uint32", _, False):
            return writers.write_uint32
        case ("uint64", _, False):
            return writers.write_uint64
        case ("float64", _, False):
            return writers.write_float64
        case ("string", True, False):
            return writers.write_compact_string
        case ("string", True, True):
            return writers.write_nullable_compact_string
        case ("string", False, False):
            return writers.write_legacy_string
        case ("string", False, True):
            return writers.write_nullable_legacy_string
        case ("bytes" | "records", True, False):
            return writers.write_compact_string
        case ("bytes" | "records", True, True):
            return writers.write_nullable_compact_string
        case ("bytes" | "records", False, False):
            return writers.write_legacy_bytes
        case ("bytes" | "records", False, True):
            return writers.write_nullable_legacy_bytes
        case ("uuid", _, _):
            return writers.write_uuid
        case ("bool", _, False):
            return writers.write_boolean
        case ("error_code", _, False):
            return writers.write_error_code
        case ("timedelta_i32", _, False):
            return writers.write_timedelta_i32
        case ("timedelta_i64", _, False):
            return writers.write_timedelta_i64
        case ("datetime_i64", _, False):
            return writers.write_datetime_i64
        case ("datetime_i64", _, True):
            return writers.write_nullable_datetime_i64

    raise NotImplementedError(
        f"Failed identifying writer for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_writer(
    field: Field[T],
    flexible: bool,
    is_request_header: bool,
    is_tag: bool,
) -> Writer[T]:
    # RequestHeader.client_id is special-cased by Apache Kafka® to always use the legacy
    # string format.
    # https://github.com/apache/kafka/blob/trunk/clients/src/main/resources/common/message/RequestHeader.json#L34-L38
    # It's odd that this choice is made, instead of addressing this only for the
    # ApiVersions request, because it's response is already special-cased.
    # https://github.com/apache/kafka/blob/trunk/generator/src/main/java/org/apache/kafka/message/ApiMessageTypeGenerator.java#L341
    if is_request_header and field.name == "client_id":
        return writers.write_nullable_legacy_string  # type: ignore[return-value]

    # Optionality needs to be special cased for tagged fields, because they are optional
    # by definition. This optionality is implemented in a different way from normal
    # fields, it's implemented by the presence or absence by the tag itself. Hence, we
    # can have optional fields with in-transit value types that cannot represent None.
    # To be able to match an optional tagged field to a writer that cannot accept None,
    # we hard-code all tagged fields as not optional here.
    optional = False if is_tag else is_optional(field)
    field_class = classify_field(field)

    match field_class:
        case PrimitiveField() | PrimitiveTupleField():
            inner_type_writer = get_writer(
                kafka_type=get_schema_field_type(field),
                flexible=flexible,
                optional=optional,
            )
        case EntityField(field_type):
            inner_type_writer = (
                entity_writer(field_type, nullable=True)
                if optional
                else entity_writer(field_type, nullable=False)
            )
        case EntityTupleField(field_type):
            inner_type_writer = entity_writer(field_type)
        case no_match:
            assert_never(no_match)

    if field_class.is_array:
        array_writer = compact_array_writer if flexible else legacy_array_writer
        # mypy fails to bind T to Sequence[object] here.
        return array_writer(inner_type_writer)  # type: ignore[return-value]

    return inner_type_writer


E = TypeVar("E", bound=Entity)


def _wrap_nullable(write_entity: Writer[E]) -> Writer[E | None]:
    # This is undocumented behavior, formalized in KIP-893.
    # https://cwiki.apache.org/confluence/display/KAFKA/KIP-893%3A+The+Kafka+protocol+should+support+nullable+structs
    def write_nullable(buffer: Writable, entity: E | None) -> None:
        if entity is None:
            write_int8(buffer, NullableEntityMarker.null.value)
            return
        write_int8(buffer, NullableEntityMarker.not_null.value)
        write_entity(buffer, entity)

    return write_nullable


@overload
def entity_writer(
    entity_type: type[E],
    nullable: Literal[False] = ...,
) -> Writer[E]: ...
@overload
def entity_writer(
    entity_type: type[E],
    nullable: Literal[True],
) -> Writer[E | None]: ...
@cache
def entity_writer(entity_type: type[E], nullable: bool = False) -> Writer[E | None]:
    field_writers = {}
    tagged_field_writers = {}
    is_request_header = entity_type.__name__ == "RequestHeader"

    for field in fields(entity_type):
        tag = get_field_tag(field)
        field_writer = get_field_writer(
            field,
            flexible=entity_type.__flexible__,
            is_request_header=is_request_header,
            is_tag=tag is not None,
        )
        if tag is not None:
            tagged_field_writers[tag] = field, field_writer
        else:
            field_writers[field] = field_writer

    # Assert we don't find tags for non-flexible models.
    if tagged_field_writers and not entity_type.__flexible__:
        raise ValueError("Found tagged fields on a non-flexible model")

    # Sort tagged fields by key, maintaining this order when writing tagged fields is
    # important to fulfill the spec.
    tagged_field_writers = {
        key: tagged_field_writers[key] for key in sorted(tagged_field_writers.keys())
    }

    def write_entity(buffer: Writable, entity: E) -> None:
        # Loop over all fields of the entity, serializing its values to the buffer.
        for field, field_writer in field_writers.items():
            field_value = getattr(entity, field.name)
            field_writer(buffer, field_value)

        # For non-flexible entities we're done here.
        if not entity_type.__flexible__:
            return

        # Write tagged fields to a temporary buffer, in order to be able to count the
        # number of tags that are being written.
        num_tagged_fields = 0
        with io.BytesIO() as tag_buffer:
            # Serialize tagged fields. Note that order is important to fulfill spec.
            for tag, (field, field_writer) in tagged_field_writers.items():
                field_value = getattr(entity, field.name)

                # Skip default-valued fields.
                if field_value == field.default:
                    continue

                # Write the tag to the buffer and increase counter.
                write_tagged_field(
                    buffer=tag_buffer,
                    tag=tag,
                    writer=field_writer,
                    value=field_value,
                )
                num_tagged_fields += 1

            # Write number of tagged fields followed by the serialized tags.
            write_unsigned_varint(buffer, num_tagged_fields)
            buffer.write(tag_buffer.getvalue())

    return _wrap_nullable(write_entity) if nullable else write_entity  # type: ignore[return-value]
