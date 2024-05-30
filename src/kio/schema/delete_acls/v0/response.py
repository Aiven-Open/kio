"""
Generated from ``clients/src/main/resources/common/message/DeleteAclsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsMatchingAcl:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(31)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The deletion error code, or 0 if the deletion succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The deletion error message, or null if the deletion succeeded."""
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The ACL resource name."""
    principal: str = field(metadata={"kafka_type": "string"})
    """The ACL principal."""
    host: str = field(metadata={"kafka_type": "string"})
    """The ACL host."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsFilterResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(31)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if the filter succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if the filter succeeded."""
    matching_acls: tuple[DeleteAclsMatchingAcl, ...]
    """The ACLs which matched this filter."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(31)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    filter_results: tuple[DeleteAclsFilterResult, ...]
    """The results for each filter."""
