"""
Generated from ``clients/src/main/resources/common/message/DescribeClusterRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClusterRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(60)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    include_cluster_authorized_operations: bool = field(metadata={"kafka_type": "bool"})
    """Whether to include cluster authorized operations."""
    endpoint_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(1))
    """The endpoint type to describe. 1=brokers, 2=controllers."""
