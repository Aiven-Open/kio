"""
Generated from SnapshotFooterRecord.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SnapshotFooterRecord.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotFooterRecord(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot footer record"""
