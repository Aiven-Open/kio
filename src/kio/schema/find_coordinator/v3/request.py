"""
Generated from FindCoordinatorRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.request_header.v2.header import RequestHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorRequest:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(10)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    key: str = field(metadata={"kafka_type": "string"})
    """The coordinator key."""
    key_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """The coordinator key type. (Group, transaction, etc.)"""
