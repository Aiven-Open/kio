"""
Generated from ``clients/src/main/resources/common/message/CreatePartitionsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsAssignment:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(37)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_ids: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The assigned broker IDs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(37)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    count: i32 = field(metadata={"kafka_type": "int32"})
    """The new partition count."""
    assignments: tuple[CreatePartitionsAssignment, ...] | None
    """The new partition assignments."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(37)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[CreatePartitionsTopic, ...]
    """Each topic that we want to create new partitions inside."""
    timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The time in ms to wait for the partitions to be created."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """If true, then validate the request, but don't actually increase the number of partitions."""
