"""
Generated from ``clients/src/main/resources/common/message/DescribeClusterResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClusterBroker:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(60)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
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
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(60)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code, or 0 if there was no error"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    endpoint_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(1))
    """The endpoint type that was described. 1=brokers, 2=controllers."""
    cluster_id: str = field(metadata={"kafka_type": "string"})
    """The cluster ID that responding broker belongs to."""
    controller_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(-1)
    )
    """The ID of the controller broker."""
    brokers: tuple[DescribeClusterBroker, ...]
    """Each broker in the response."""
    cluster_authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this cluster."""
