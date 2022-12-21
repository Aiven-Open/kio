"""
Generated from SnapshotHeaderRecord.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotHeaderRecord:
    __flexible__: ClassVar[bool] = True
    version: int = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot header record"""
    last_contained_log_timestamp: int = field(metadata={"kafka_type": "int64"})
    """The append time of the last record from the log contained in this snapshot"""
