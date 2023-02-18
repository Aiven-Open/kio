"""
Generated from SnapshotFooterRecord.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotFooterRecord:
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot footer record"""
