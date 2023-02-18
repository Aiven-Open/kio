"""
Generated from DefaultPrincipalData.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DefaultPrincipalData:
    __flexible__: ClassVar[bool] = True
    type: str = field(metadata={"kafka_type": "string"})
    """The principal type"""
    name: str = field(metadata={"kafka_type": "string"})
    """The principal name"""
    token_authenticated: bool = field(metadata={"kafka_type": "bool"})
    """Whether the principal was authenticated by a delegation token on the forwarding broker."""
