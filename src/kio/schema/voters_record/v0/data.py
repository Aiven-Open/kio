"""
Generated from ``clients/src/main/resources/common/message/VotersRecord.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class Endpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
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
    min_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported KRaft protocol version"""
    max_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported KRaft protocol version"""


@dataclass(frozen=True, slots=True, kw_only=True)
class Voter:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    voter_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The replica id of the voter in the topic partition"""
    voter_directory_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The directory id of the voter in the topic partition"""
    endpoints: tuple[Endpoint, ...]
    """The endpoint that can be used to communicate with the voter"""
    k_raft_version_feature: KRaftVersionFeature
    """The range of versions of the protocol that the replica supports"""


@dataclass(frozen=True, slots=True, kw_only=True)
class VotersRecord:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the voters record"""
    voters: tuple[Voter, ...]
