"""
Generated from ``clients/src/main/resources/common/message/PushTelemetryRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class PushTelemetryRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(72)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    client_instance_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """Unique id for this client instance."""
    subscription_id: i32 = field(metadata={"kafka_type": "int32"})
    """Unique identifier for the current subscription."""
    terminating: bool = field(metadata={"kafka_type": "bool"})
    """Client is terminating the connection."""
    compression_type: i8 = field(metadata={"kafka_type": "int8"})
    """Compression codec used to compress the metrics."""
    metrics: bytes = field(metadata={"kafka_type": "bytes"})
    """Metrics encoded in OpenTelemetry MetricsData v1 protobuf format."""
