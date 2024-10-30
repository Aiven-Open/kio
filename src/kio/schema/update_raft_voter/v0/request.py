"""
Generated from ``clients/src/main/resources/common/message/UpdateRaftVoterRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class Listener:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(82)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the endpoint"""
    host: str = field(metadata={"kafka_type": "string"})
    """The hostname"""
    port: u16 = field(metadata={"kafka_type": "uint16"})
    """The port"""


@dataclass(frozen=True, slots=True, kw_only=True)
class KRaftVersionFeature:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(82)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    min_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported KRaft protocol version"""
    max_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported KRaft protocol version"""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateRaftVoterRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(82)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    cluster_id: str | None = field(metadata={"kafka_type": "string"})
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current leader epoch of the partition, -1 for unknown leader epoch"""
    voter_id: i32 = field(metadata={"kafka_type": "int32"})
    """The replica id of the voter getting updated in the topic partition"""
    voter_directory_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The directory id of the voter getting updated in the topic partition"""
    listeners: tuple[Listener, ...]
    """The endpoint that can be used to communicate with the leader"""
    k_raft_version_feature: KRaftVersionFeature
    """The range of versions of the protocol that the replica supports"""
