"""
Generated from WriteTxnMarkersResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerPartitionResult:
    __flexible__: ClassVar[bool] = False
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerTopicResult:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[WritableTxnMarkerPartitionResult, ...]
    """The results by partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerResult:
    __flexible__: ClassVar[bool] = False
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The current producer ID in use by the transactional ID."""
    topics: tuple[WritableTxnMarkerTopicResult, ...]
    """The results by topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WriteTxnMarkersResponse:
    __flexible__: ClassVar[bool] = False
    markers: tuple[WritableTxnMarkerResult, ...]
    """The results for writing makers."""
