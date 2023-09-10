"""
Generated from ListGroupsRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ListGroupsRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsRequest:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    states_filter: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The states of the groups we want to list. If empty all groups are returned with their state."""
