"""
Generated from ``clients/src/main/resources/common/message/DefaultPrincipalData.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DefaultPrincipalData:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    type_: str = field(metadata={"kafka_type": "string"})
    """The principal type"""
    name: str = field(metadata={"kafka_type": "string"})
    """The principal name"""
    token_authenticated: bool = field(metadata={"kafka_type": "bool"})
    """Whether the principal was authenticated by a delegation token on the forwarding broker."""
