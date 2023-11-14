"""
Generated from AllocateProducerIdsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AllocateProducerIdsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AllocateProducerIdsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(67)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top level response error code"""
    producer_id_start: ProducerId = field(metadata={"kafka_type": "int64"})
    """The first producer ID in this range, inclusive"""
    producer_id_len: i32 = field(metadata={"kafka_type": "int32"})
    """The number of producer IDs in this range"""
