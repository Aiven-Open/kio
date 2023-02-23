"""
Generated from UpdateMetadataResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataResponse:
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
