"""
Generated from CreateDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableRenewers:
    __flexible__: ClassVar[bool] = False
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The type of the Kafka principal."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The name of the Kafka principal."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateDelegationTokenRequest:
    __flexible__: ClassVar[bool] = False
    renewers: tuple[CreatableRenewers, ...]
    """A list of those who are allowed to renew this token before it expires."""
    max_lifetime_ms: int = field(metadata={"kafka_type": "int64"})
    """The maximum lifetime of the token in milliseconds, or -1 to use the server side default."""
