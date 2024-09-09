"""
Generated from ``clients/src/main/resources/common/message/GetTelemetrySubscriptionsResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTelemetrySubscriptionsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(71)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    client_instance_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """Assigned client instance id if ClientInstanceId was 0 in the request, else 0."""
    subscription_id: i32 = field(metadata={"kafka_type": "int32"})
    """Unique identifier for the current subscription set for this client instance."""
    accepted_compression_types: tuple[i8, ...] = field(
        metadata={"kafka_type": "int8"}, default=()
    )
    """Compression types that broker accepts for the PushTelemetryRequest."""
    push_interval: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Configured push interval, which is the lowest configured interval in the current subscription set."""
    telemetry_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes of binary data the broker accepts in PushTelemetryRequest."""
    delta_temporality: bool = field(metadata={"kafka_type": "bool"})
    """Flag to indicate monotonic/counter metrics are to be emitted as deltas or cumulative values"""
    requested_metrics: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Requested metrics prefix string match. Empty array: No metrics subscribed, Array[0] empty string: All metrics subscribed."""
