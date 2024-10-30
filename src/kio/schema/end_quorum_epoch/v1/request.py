"""
Generated from ``clients/src/main/resources/common/message/EndQuorumEpochRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaInfo:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(54)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    candidate_id: BrokerId = field(metadata={"kafka_type": "int32"})
    candidate_directory_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(54)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The current leader ID that is resigning"""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current epoch"""
    preferred_candidates: tuple[ReplicaInfo, ...]
    """A sorted list of preferred candidates to start the election"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(54)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderEndpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(54)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the endpoint"""
    host: str = field(metadata={"kafka_type": "string"})
    """The node's hostname"""
    port: u16 = field(metadata={"kafka_type": "uint16"})
    """The node's port"""


@dataclass(frozen=True, slots=True, kw_only=True)
class EndQuorumEpochRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(54)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    topics: tuple[TopicData, ...]
    leader_endpoints: tuple[LeaderEndpoint, ...]
    """Endpoints for the leader"""
