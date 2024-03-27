"""
Generated from ``clients/src/main/resources/common/message/DescribeGroupsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeGroupsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(15)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    groups: tuple[GroupId, ...] = field(metadata={"kafka_type": "string"}, default=())
    """The names of the groups to describe"""
