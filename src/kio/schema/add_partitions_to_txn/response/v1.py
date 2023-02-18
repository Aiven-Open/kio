"""
Generated from AddPartitionsToTxnResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnPartitionResult:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition indexes."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The response error code."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopicResult:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    results: tuple[AddPartitionsToTxnPartitionResult, ...]
    """The results for each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[AddPartitionsToTxnTopicResult, ...]
    """The results for each topic."""
