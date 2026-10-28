"""
Generated from ``clients/src/main/resources/common/message/ApiVersionsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    client_software_name: str = field(metadata={"kafka_type": "string"})
    """The name of the client."""
    client_software_version: str = field(metadata={"kafka_type": "string"})
    """The version of the client."""
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The cluster ID the client intends to connect to. Provide both ClusterId and NodeId, if known."""
    node_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The node ID the client intends to connect to. Provide both ClusterId and NodeId, if known."""
