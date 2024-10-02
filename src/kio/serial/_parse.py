from dataclasses import Field
from dataclasses import fields
from typing import IO
from typing import Literal
from typing import TypeVar
from typing import assert_never
from typing import overload

from kio._utils import cache
from kio.static.protocol import Entity

from . import readers
from ._introspect import EntityField
from ._introspect import EntityTupleField
from ._introspect import PrimitiveField
from ._introspect import PrimitiveTupleField
from ._introspect import classify_field
from ._introspect import get_field_tag
from ._introspect import get_schema_field_type
from ._introspect import is_optional
from ._shared import NullableEntityMarker
from .readers import read_int8


def get_reader(
    kafka_type: str,
    flexible: bool,
    optional: bool,
) -> readers.Reader:
    match (kafka_type, flexible, optional):
        case ("int8", _, False):
            return readers.read_int8
        case ("int16", _, False):
            return readers.read_int16
        case ("int32", _, False):
            return readers.read_int32
        case ("int64", _, False):
            return readers.read_int64
        case ("uint8", _, False):
            return readers.read_uint8
        case ("uint16", _, False):
            return readers.read_uint16
        case ("uint32", _, False):
            return readers.read_uint32
        case ("uint64", _, False):
            return readers.read_uint64
        case ("float64", _, False):
            return readers.read_float64
        case ("string", True, False):
            return readers.read_compact_string
        case ("string", True, True):
            return readers.read_compact_string_nullable
        case ("string", False, False):
            return readers.read_legacy_string
        case ("string", False, True):
            return readers.read_nullable_legacy_string
        case ("bytes" | "records", True, False):
            return readers.read_compact_string_as_bytes
        case ("bytes" | "records", True, True):
            return readers.read_compact_string_as_bytes_nullable
        case ("bytes" | "records", False, False):
            return readers.read_legacy_bytes
        case ("bytes" | "records", False, True):
            return readers.read_nullable_legacy_bytes
        case ("uuid", _, True):
            return readers.read_uuid
        case ("bool", _, False):
            return readers.read_boolean
        case ("error_code", _, False):
            return readers.read_error_code
        case ("timedelta_i32", _, False):
            return readers.read_timedelta_i32
        case ("timedelta_i64", _, False):
            return readers.read_timedelta_i64
        case ("datetime_i64", _, False):
            return readers.read_datetime_i64
        case ("datetime_i64", _, True):
            return readers.read_nullable_datetime_i64

    raise NotImplementedError(
        f"Failed identifying reader for {kafka_type!r} field {flexible=} {optional=}"
    )


T = TypeVar("T")


def get_field_reader(
    entity_type: type[Entity],
    field: Field[T],
    is_request_header: bool,
    is_tagged_field: bool,
) -> readers.Reader[T]:
    # RequestHeader.client_id is special-cased by Apache Kafka® to always use the legacy
    # string format.
    # https://github.com/apache/kafka/blob/trunk/clients/src/main/resources/common/message/RequestHeader.json#L34-L38
    if is_request_header and field.name == "client_id":
        return readers.read_nullable_legacy_string  # type: ignore[return-value]

    flexible = entity_type.__flexible__
    field_class = classify_field(field)

    match field_class:
        case PrimitiveField():
            inner_type_reader = get_reader(
                kafka_type=get_schema_field_type(field),
                flexible=flexible,
                optional=is_optional(field) and not is_tagged_field,
            )
        case PrimitiveTupleField():
            inner_type_reader = get_reader(
                kafka_type=get_schema_field_type(field),
                flexible=flexible,
                optional=is_optional(field),
            )
        case EntityField(field_type):
            inner_type_reader = (
                entity_reader(field_type, nullable=True)
                if is_optional(field)
                else entity_reader(field_type, nullable=False)
            )
        case EntityTupleField(field_type):
            inner_type_reader = entity_reader(field_type)
        case no_match:
            assert_never(no_match)

    if field_class.is_array:
        array_reader = (
            readers.compact_array_reader if flexible else readers.legacy_array_reader
        )
        # mypy fails to bind T to Sequence[object] here.
        return array_reader(inner_type_reader)  # type: ignore[return-value]

    return inner_type_reader


E = TypeVar("E", bound=Entity)


@overload
def entity_reader(
    entity_type: type[E],
    nullable: Literal[False] = ...,
) -> readers.Reader[E]: ...
@overload
def entity_reader(
    entity_type: type[E],
    nullable: Literal[True],
) -> readers.Reader[E | None]: ...
@cache
def entity_reader(
    entity_type: type[E],
    nullable: bool = False,
) -> readers.Reader[E | None]:
    field_readers = {}
    tagged_field_readers = {}
    is_request_header = entity_type.__name__ == "RequestHeader"

    for field in fields(entity_type):
        tag = get_field_tag(field)
        field_reader = get_field_reader(
            entity_type=entity_type,
            field=field,
            is_request_header=is_request_header,
            is_tagged_field=tag is not None,
        )
        if tag is not None:
            tagged_field_readers[tag] = field, field_reader
        else:
            field_readers[field] = field_reader

    # Assert we don't find tags for non-flexible models.
    if tagged_field_readers and not entity_type.__flexible__:
        raise ValueError("Found tagged fields on a non-flexible model")

    def read_entity(buffer: IO[bytes]) -> E:
        # Read regular fields.
        kwargs = {
            field.name: field_reader(buffer)
            for field, field_reader in field_readers.items()
        }

        # For non-flexible entities we're done here.
        if not entity_type.__flexible__:
            return entity_type(**kwargs)

        # Read tagged fields.
        num_tagged_fields = readers.read_unsigned_varint(buffer)
        for _ in range(num_tagged_fields):
            field_tag = readers.read_unsigned_varint(buffer)
            readers.read_unsigned_varint(buffer)  # field length
            field, field_reader = tagged_field_readers[field_tag]
            kwargs[field.name] = field_reader(buffer)

        return entity_type(**kwargs)

    if not nullable:
        return read_entity

    # This is undocumented behavior, formalized in KIP-893.
    # https://cwiki.apache.org/confluence/display/KAFKA/KIP-893%3A+The+Kafka+protocol+should+support+nullable+structs
    def read_nullable_entity(buffer: IO[bytes]) -> E | None:
        marker = NullableEntityMarker(read_int8(buffer))
        return None if marker is NullableEntityMarker.null else read_entity(buffer)

    return read_nullable_entity
