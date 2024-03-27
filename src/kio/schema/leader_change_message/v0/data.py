"""
Generated from ``clients/src/main/resources/common/message/LeaderChangeMessage.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class Voter:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    voter_id: i32 = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderChangeMessage:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the leader change message"""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the newly elected leader"""
    voters: tuple[Voter, ...]
    """The set of voters in the quorum for this epoch"""
    granting_voters: tuple[Voter, ...]
    """The voters who voted for the leader at the time of election"""
