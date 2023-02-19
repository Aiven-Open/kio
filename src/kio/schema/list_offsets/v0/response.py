"""
Generated from ListOffsetsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartitionResponse:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no error."""
    old_style_offsets: tuple[i64, ...] = field(
        metadata={"kafka_type": "int64"}, default=()
    )
    """The result offsets."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopicResponse:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ListOffsetsPartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsResponse:
    __flexible__: ClassVar[bool] = False
    topics: tuple[ListOffsetsTopicResponse, ...]
    """Each topic in the response."""