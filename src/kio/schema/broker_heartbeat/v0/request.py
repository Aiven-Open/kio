"""
Generated from BrokerHeartbeatRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/BrokerHeartbeatRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.static.primitive import i16
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerHeartbeatRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(63)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The broker epoch."""
    current_metadata_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The highest metadata offset which the broker has reached."""
    want_fence: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker wants to be fenced, false otherwise."""
    want_shut_down: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker wants to be shut down, false otherwise."""
