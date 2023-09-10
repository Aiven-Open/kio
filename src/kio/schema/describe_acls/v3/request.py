"""
Generated from DescribeAclsRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/DescribeAclsRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsRequest:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(29)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type_filter: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name_filter: str | None = field(metadata={"kafka_type": "string"})
    """The resource name, or null to match any resource name."""
    pattern_type_filter: i8 = field(metadata={"kafka_type": "int8"}, default=i8(3))
    """The resource pattern to match."""
    principal_filter: str | None = field(metadata={"kafka_type": "string"})
    """The principal to match, or null to match any principal."""
    host_filter: str | None = field(metadata={"kafka_type": "string"})
    """The host to match, or null to match any host."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The operation to match."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The permission type to match."""
