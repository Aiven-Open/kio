"""
Generated from DescribeDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenOwner:
    __flexible__: ClassVar[bool] = True
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The owner principal type."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The owner principal name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenRequest:
    __flexible__: ClassVar[bool] = True
    owners: tuple[DescribeDelegationTokenOwner, ...]
    """Each owner that we want to describe delegation tokens for, or null to describe all tokens."""
