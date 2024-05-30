"""
Generated from ``clients/src/main/resources/common/message/ListGroupsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ListedGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The group protocol type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    groups: tuple[ListedGroup, ...]
    """Each group in the response."""
