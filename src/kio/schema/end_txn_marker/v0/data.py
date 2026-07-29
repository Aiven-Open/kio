"""
Generated from ``clients/src/main/resources/common/message/EndTxnMarker.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class EndTxnMarker:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    coordinator_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The coordinator epoch when appending the record"""
