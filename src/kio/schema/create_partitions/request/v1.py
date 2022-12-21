"""
Generated from CreatePartitionsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsAssignment:
    __flexible__: ClassVar[bool] = False
    broker_ids: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The assigned broker IDs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    count: int = field(metadata={"kafka_type": "int32"})
    """The new partition count."""
    assignments: tuple[CreatePartitionsAssignment, ...]
    """The new partition assignments."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsRequest:
    __flexible__: ClassVar[bool] = False
    topics: tuple[CreatePartitionsTopic, ...]
    """Each topic that we want to create new partitions inside."""
    timeout_ms: int = field(metadata={"kafka_type": "int32"})
    """The time in ms to wait for the partitions to be created."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """If true, then validate the request, but don't actually increase the number of partitions."""
