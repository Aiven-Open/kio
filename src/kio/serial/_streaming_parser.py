from collections.abc import Generator
from dataclasses import Field
from dataclasses import fields
from typing import IO
from typing import TypeVar

from kio._utils import cache
from kio.static.constants import EntityType
from kio.static.protocol import Entity

from . import readers
from ._implicit_defaults import get_tagged_field_default
from ._introspect import get_field_tag
from ._parse import entity_reader
from ._parse import get_field_reader
from .readers import Reader
from .readers import read_compact_array_length
from .readers import read_legacy_array_length

H = TypeVar("H", bound=Entity)
S = TypeVar("S", bound=Entity)
T = TypeVar("T", bound=Entity)


def _gather_head_field_readers(
    entity_type: type[Entity],
) -> dict[Field, Reader[object]]:
    field_readers = {}
    for field in fields(entity_type):
        if get_field_tag(field) is not None:
            raise ValueError(
                "The head type cannot have tagged fields, as tags are serialized at the end of messages"
            )
        field_readers[field] = get_field_reader(
            entity_type=entity_type,
            field=field,
            is_request_header=False,
            is_tagged_field=False,
        )
    return field_readers


def _gather_tail_and_tagged_field_readers(
    entity_type: type[Entity],
) -> tuple[
    dict[Field, Reader[object]],
    dict[int, tuple[Field, Reader[object], object]],
]:
    tail_field_readers: dict[Field, Reader[object]] = {}
    tagged_field_readers: dict[int, tuple[Field, Reader[object], object]] = {}

    # Gather tail field readers.
    for field in fields(entity_type):
        tag = get_field_tag(field)
        field_reader = get_field_reader(
            entity_type=entity_type,
            field=field,
            is_request_header=False,
            is_tagged_field=tag is not None,
        )
        if tag is not None:
            tagged_field_readers[tag] = (
                field,
                field_reader,
                get_tagged_field_default(field),
            )
        else:
            tail_field_readers[field] = field_reader

    return tail_field_readers, tagged_field_readers


@cache
def streaming_entity_reader(
    head_type: type[H],
    streaming_type: type[S],
    tail_type: type[T],
) -> readers.Reader[Generator[H | S | T, None, None]]:
    assert head_type.__type__ is EntityType.response
    assert streaming_type.__type__ is EntityType.response
    assert tail_type.__type__ is EntityType.response
    assert (
        head_type.__flexible__ == streaming_type.__flexible__ == tail_type.__flexible__
    )

    read_length = (
        read_compact_array_length
        if streaming_type.__flexible__
        else read_legacy_array_length
    )
    read_streaming_entity = entity_reader(streaming_type)

    head_field_readers = _gather_head_field_readers(head_type)
    (
        tail_field_readers,
        tagged_field_readers,
    ) = _gather_tail_and_tagged_field_readers(tail_type)

    # Assert we don't find tags for non-flexible models.
    if tagged_field_readers and not tail_type.__flexible__:
        raise ValueError("Found tagged fields on a non-flexible model")

    def stream_entities(buffer: IO[bytes]) -> Generator[H | S | T, None, None]:
        # Read head.
        yield head_type(
            **{
                field.name: field_reader(buffer)
                for field, field_reader in head_field_readers.items()
            }
        )

        # Read the streaming type.
        for _ in range(read_length(buffer)):
            yield read_streaming_entity(buffer)

        # Read tail regular fields.
        tail_kwargs = {
            field.name: field_reader(buffer)
            for field, field_reader in tail_field_readers.items()
        }

        # For non-flexible entities we're done here.
        if not tail_type.__flexible__:
            yield tail_type(**tail_kwargs)
            return

        # Read tagged fields.
        tagged_field_values = {}
        num_tagged_fields = readers.read_unsigned_varint(buffer)
        for _ in range(num_tagged_fields):
            field_tag = readers.read_unsigned_varint(buffer)
            readers.read_unsigned_varint(buffer)  # field length
            field, field_reader, _ = tagged_field_readers[field_tag]
            tagged_field_values[field.name] = field_reader(buffer)

        # Resolve tagged field implicit defaults.
        for field, _, implicit_default in tagged_field_readers.values():
            tail_kwargs[field.name] = tagged_field_values.get(
                field.name, implicit_default
            )

        yield tail_type(**tail_kwargs)

    return stream_entities
