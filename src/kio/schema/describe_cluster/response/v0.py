"""
Generated from DescribeClusterResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClusterBroker:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    host: str = field(metadata={"kafka_type": "string"})
    """The broker hostname."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The broker port."""
    rack: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The rack of the broker, or null if it has not been assigned to a rack."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClusterResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no error"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    cluster_id: str = field(metadata={"kafka_type": "string"})
    """The cluster ID that responding broker belongs to."""
    controller_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(i32(-1))
    )
    """The ID of the controller broker."""
    brokers: tuple[DescribeClusterBroker, ...]
    """Each broker in the response."""
    cluster_authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this cluster."""
