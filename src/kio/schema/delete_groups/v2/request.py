"""
Generated from ``clients/src/main/resources/common/message/DeleteGroupsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteGroupsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(42)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    groups_names: tuple[GroupId, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The group names to delete."""
