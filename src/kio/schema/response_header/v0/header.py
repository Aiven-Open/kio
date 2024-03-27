"""
Generated from ``clients/src/main/resources/common/message/ResponseHeader.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ResponseHeader:
    __type__: ClassVar = EntityType.header
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this response."""
