"""
Generated from JoinGroupRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupRequestProtocol:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The protocol name."""
    metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The protocol metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupRequest:
    __flexible__: ClassVar[bool] = True
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    session_timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The coordinator considers the consumer dead if it receives no heartbeat after this timeout in milliseconds."""
    rebalance_timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The maximum time in milliseconds that the coordinator will wait for each member to rejoin when rebalancing the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member id assigned by the group coordinator."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The unique name the for class of protocols implemented by the group we want to join."""
    protocols: tuple[JoinGroupRequestProtocol, ...]
    """The list of protocols that the member supports."""
    reason: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The reason why the member (re-)joins the group."""
