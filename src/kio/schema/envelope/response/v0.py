"""
Generated from EnvelopeResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvelopeResponse:
    __flexible__: ClassVar[bool] = True
    response_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    """The embedded response header and data."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
