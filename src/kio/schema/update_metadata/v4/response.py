"""
Generated from UpdateMetadataResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.response_header.v0.header import ResponseHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataResponse:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
