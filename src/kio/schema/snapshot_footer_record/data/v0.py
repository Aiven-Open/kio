"""
Generated from SnapshotFooterRecord.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotFooterRecord:
    __flexible__: ClassVar[bool] = True
    version: int = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot footer record"""
