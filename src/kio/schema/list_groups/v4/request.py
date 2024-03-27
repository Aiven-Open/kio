"""
Generated from ``clients/src/main/resources/common/message/ListGroupsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    states_filter: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The states of the groups we want to list. If empty all groups are returned with their state."""
