"""
Generated from ListGroupsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListGroupsRequest.json
"""

from dataclasses import dataclass
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
