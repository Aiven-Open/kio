"""
Generated from FindCoordinatorResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorResponse:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    node_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The node id."""
    host: str = field(metadata={"kafka_type": "string"})
    """The host name."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The port."""
