"""
Generated from AddOffsetsToTxnResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class AddOffsetsToTxnResponse:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(25)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The response error code, or 0 if there was no error."""
