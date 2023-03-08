"""
Generated from ResponseHeader.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ResponseHeader:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this response."""
