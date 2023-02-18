"""
Generated from ElectLeadersResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResult:
    __flexible__: ClassVar[bool] = True
    partition_id: i32 = field(metadata={"kafka_type": "int32"})
    """The partition id"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The result error, or zero if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The result message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaElectionResult:
    __flexible__: ClassVar[bool] = True
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_result: tuple[PartitionResult, ...]
    """The results for each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectLeadersResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level response error code."""
    replica_election_results: tuple[ReplicaElectionResult, ...]
    """The election results, or an empty array if the requester did not have permission and the request asks for all partitions."""
