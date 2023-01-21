import io
from dataclasses import fields
from dataclasses import is_dataclass
from types import EllipsisType
from typing import ClassVar
from typing import Protocol
from typing import TypeVar
from typing import get_args
from typing import get_origin

from kio.serial.decoders import Decoder
from kio.serial.decoders import decode_compact_array_length
from kio.serial.decoders import decode_unsigned_varint
from kio.serial.decoders import read_sync

from . import decoders
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


class Entity(Protocol):
    __flexible__: ClassVar[bool]


# FIXME: Don't do this.
def skip_tagged_fields(buffer: io.BytesIO) -> None:
    # The tagged field structure is described in
    # https://cwiki.apache.org/confluence/display/KAFKA/KIP-482%3A+The+Kafka+Protocol+should+Support+Optional+Tagged+Fields
    for _ in range(read_sync(buffer, decode_unsigned_varint)):
        read_sync(buffer, decode_unsigned_varint)  # tag
        value_len = read_sync(buffer, decode_unsigned_varint)
        buffer.seek(buffer.tell() + value_len)


E = TypeVar("E", bound=Entity)


def read_compact_entity_array(
    buffer: io.BytesIO,
    entity_type: type[E],
) -> tuple[E, ...]:
    length = read_sync(buffer, decode_compact_array_length)
    return tuple(parse_entity(buffer, entity_type) for _ in range(length))


T = TypeVar("T")


def read_compact_array(buffer: io.BytesIO, decoder: Decoder[T]) -> tuple[T, ...]:
    length = read_sync(buffer, decode_compact_array_length)
    return tuple(read_sync(buffer, decoder) for _ in range(length))


def parse_entity(buffer: io.BytesIO, entity_type: type[E]) -> E:
    kwargs = {}
    for field in fields(entity_type):
        if get_origin(field.type) is tuple:
            match get_args(field.type):
                case (inner_type, EllipsisType()) if is_dataclass(inner_type):
                    kwargs[field.name] = read_compact_entity_array(buffer, inner_type)
                case (_, EllipsisType()):
                    kafka_type = get_schema_field_type(field)
                    decoder = get_decoder(
                        kafka_type=kafka_type,
                        flexible=entity_type.__flexible__,
                        optional=is_optional(field),
                    )
                    kwargs[field.name] = read_compact_array(buffer, decoder)
                case _:
                    raise NotImplementedError
        else:
            kafka_type = get_schema_field_type(field)
            decoder = get_decoder(
                kafka_type=kafka_type,
                flexible=entity_type.__flexible__,
                optional=is_optional(field),
            )
            print(f"reading {field.name} of {entity_type.__qualname__}")
            kwargs[field.name] = read_sync(buffer, decoder)
            print(f" -> value={kwargs[field.name]}")

    skip_tagged_fields(buffer)

    return entity_type(**kwargs)
