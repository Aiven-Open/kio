"""
Generated from AlterUserScramCredentialsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResult:
    __flexible__: ClassVar[bool] = True
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, if any."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[AlterUserScramCredentialsResult, ...]
    """The results for deletions and alterations, one per affected user."""
