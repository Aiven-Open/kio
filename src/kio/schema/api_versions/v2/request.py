"""
Generated from ApiVersionsRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ApiVersionsRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsRequest:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
