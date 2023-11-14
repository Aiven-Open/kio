"""
Generated from RequestHeader.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/RequestHeader.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestHeader(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    request_api_key: i16 = field(metadata={"kafka_type": "int16"})
    """The API key of this request."""
    request_api_version: i16 = field(metadata={"kafka_type": "int16"})
    """The API version of this request."""
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this request."""
    client_id: str | None = field(metadata={"kafka_type": "string"})
    """The client ID string."""
