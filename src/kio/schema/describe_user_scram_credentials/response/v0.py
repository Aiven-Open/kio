"""
Generated from DescribeUserScramCredentialsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class CredentialInfo:
    __flexible__: ClassVar[bool] = True
    mechanism: int = field(metadata={"kafka_type": "int8"})
    """The SCRAM mechanism."""
    iterations: int = field(metadata={"kafka_type": "int32"})
    """The number of iterations used in the SCRAM credential."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResult:
    __flexible__: ClassVar[bool] = True
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The user-level error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The user-level error message, if any."""
    credential_infos: tuple[CredentialInfo, ...]
    """The mechanism and related information associated with the user's SCRAM credentials."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The message-level error code, 0 except for user authorization or infrastructure issues."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The message-level error message, if any."""
    results: tuple[DescribeUserScramCredentialsResult, ...]
    """The results for descriptions, one per user."""
