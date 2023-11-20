"""
Generated from ResponseHeader.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ResponseHeader.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ResponseHeader(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this response."""
