"""
Generated from ``clients/src/main/resources/common/message/DescribeUserScramCredentialsResponse.json``.
"""

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
class CredentialInfo:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    mechanism: i8 = field(metadata={"kafka_type": "int8"})
    """The SCRAM mechanism."""
    iterations: i32 = field(metadata={"kafka_type": "int32"})
    """The number of iterations used in the SCRAM credential."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The user-level error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The user-level error message, if any."""
    credential_infos: tuple[CredentialInfo, ...]
    """The mechanism and related information associated with the user's SCRAM credentials."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The message-level error code, 0 except for user authorization or infrastructure issues."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The message-level error message, if any."""
    results: tuple[DescribeUserScramCredentialsResult, ...]
    """The results for descriptions, one per user."""
