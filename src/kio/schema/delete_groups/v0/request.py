"""
Generated from DeleteGroupsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteGroupsRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(42)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    groups_names: tuple[GroupId, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The group names to delete."""
