"""
Generated from ``clients/src/main/resources/common/message/GetTelemetrySubscriptionsRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTelemetrySubscriptionsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(71)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    client_instance_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """Unique id for this client instance, must be set to 0 on the first request."""
