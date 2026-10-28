"""
Generated from ``clients/src/main/resources/common/message/AbortedTxn.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class AbortedTxn:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    producer_id: i64 = field(metadata={"kafka_type": "int64"})
    """The producer id associated with the aborted transaction"""
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The first offset in the aborted transaction"""
    last_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last offset in the aborted transaction"""
    last_stable_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last stable offset at the time the transaction was aborted"""
