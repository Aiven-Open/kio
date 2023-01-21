import io
from dataclasses import fields, is_dataclass
from typing import TypeVar, Protocol, ClassVar

from kio.serial.decoders import read_sync
from . import decoders
from .introspect import get_schema_field_type, is_optional


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

    raise NotImplementedError(
        f"Failed identifying decoder for {kafka_type!r} field {flexible=} {optional=}"
    )


class Entity(Protocol):
    __flexible__: ClassVar[bool]


E = TypeVar("E", bound=Entity)


def parse(buffer: io.BytesIO, entity_type: type[E]) -> E:
    kwargs = {}
    for field in fields(entity_type):
        if is_dataclass(field.type):
            kwargs[field.name] = parse(buffer, field.type)
        else:
            kafka_type = get_schema_field_type(field)
            decoder = get_decoder(
                kafka_type=kafka_type,
                flexible=entity_type.__flexible__,
                optional=is_optional(field),
            )
            kwargs[field.name] = read_sync(buffer, decoder)
    return entity_type(**kwargs)
