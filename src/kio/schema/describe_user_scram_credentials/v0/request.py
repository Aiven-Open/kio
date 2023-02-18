"""
Generated from DescribeUserScramCredentialsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class UserName:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The user name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsRequest:
    __flexible__: ClassVar[bool] = True
    users: tuple[UserName, ...]
    """The users to describe, or null/empty to describe all users."""
