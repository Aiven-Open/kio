"""
Generated from ResponseHeader.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ResponseHeader:
    __flexible__: ClassVar[bool] = True
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this response."""
