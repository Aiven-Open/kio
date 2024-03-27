"""
Generated from ``clients/src/main/resources/common/message/ListClientMetricsResourcesRequest.json``.
"""

from dataclasses import dataclass
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ListClientMetricsResourcesRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(74)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
