"""
Generated from BrokerHeartbeatRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerHeartbeatRequest:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    broker_epoch: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The broker epoch."""
    current_metadata_offset: int = field(metadata={"kafka_type": "int64"})
    """The highest metadata offset which the broker has reached."""
    want_fence: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker wants to be fenced, false otherwise."""
    want_shut_down: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker wants to be shut down, false otherwise."""
