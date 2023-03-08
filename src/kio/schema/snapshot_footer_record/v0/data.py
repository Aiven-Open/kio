"""
Generated from SnapshotFooterRecord.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotFooterRecord:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the snapshot footer record"""
