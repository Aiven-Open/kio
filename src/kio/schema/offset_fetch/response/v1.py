"""
Generated from OffsetFetchResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponsePartition:
    __flexible__: ClassVar[bool] = False
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    committed_offset: int = field(metadata={"kafka_type": "int64"})
    """The committed message offset."""
    metadata: str | None = field(metadata={"kafka_type": "string"})
    """The partition metadata."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponseTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetFetchResponsePartition, ...]
    """The responses per partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponse:
    __flexible__: ClassVar[bool] = False
    topics: tuple[OffsetFetchResponseTopic, ...]
    """The responses per topic."""
