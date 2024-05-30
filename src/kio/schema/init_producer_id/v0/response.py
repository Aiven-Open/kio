"""
Generated from ``clients/src/main/resources/common/message/InitProducerIdResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(22)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    producer_id: ProducerId = field(
        metadata={"kafka_type": "int64"}, default=ProducerId(-1)
    )
    """The current producer id."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer id."""
