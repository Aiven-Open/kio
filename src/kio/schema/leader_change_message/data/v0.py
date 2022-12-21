"""
Generated from LeaderChangeMessage.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class Voter:
    __flexible__: ClassVar[bool] = True
    voter_id: int = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderChangeMessage:
    __flexible__: ClassVar[bool] = True
    version: int = field(metadata={"kafka_type": "int16"})
    """The version of the leader change message"""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the newly elected leader"""
    voters: tuple[Voter, ...]
    """The set of voters in the quorum for this epoch"""
    granting_voters: tuple[Voter, ...]
    """The voters who voted for the leader at the time of election"""
