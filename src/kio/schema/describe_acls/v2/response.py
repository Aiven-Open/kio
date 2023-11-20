"""
Generated from DescribeAclsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeAclsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AclDescription:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(29)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    principal: str = field(metadata={"kafka_type": "string"})
    """The ACL principal."""
    host: str = field(metadata={"kafka_type": "string"})
    """The ACL host."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResource:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(29)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    pattern_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(3))
    """The resource pattern type."""
    acls: tuple[AclDescription, ...]
    """The ACLs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(29)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    resources: tuple[DescribeAclsResource, ...]
    """Each Resource that is referenced in an ACL."""
