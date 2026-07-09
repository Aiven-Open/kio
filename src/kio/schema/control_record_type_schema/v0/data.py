"""
Generated from ``clients/src/main/resources/common/message/ControlRecordTypeSchema.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ControlRecordTypeSchema:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    type_: i16 = field(metadata={"kafka_type": "int16"})
    """The type of the control record, such as commit or abort"""
