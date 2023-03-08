"""
Generated from AlterUserScramCredentialsResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v1.header import ResponseHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, if any."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[AlterUserScramCredentialsResult, ...]
    """The results for deletions and alterations, one per affected user."""
