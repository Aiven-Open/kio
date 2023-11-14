"""
Generated from DescribeClusterRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeClusterRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClusterRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(60)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    include_cluster_authorized_operations: bool = field(metadata={"kafka_type": "bool"})
    """Whether to include cluster authorized operations."""
