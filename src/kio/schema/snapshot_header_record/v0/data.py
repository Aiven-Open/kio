"""
Generated from SnapshotHeaderRecord.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/SnapshotHeaderRecord.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.primitive import i16
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotHeaderRecord:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot header record"""
    last_contained_log_timestamp: i64 = field(metadata={"kafka_type": "int64"})
    """The append time of the last record from the log contained in this snapshot"""
