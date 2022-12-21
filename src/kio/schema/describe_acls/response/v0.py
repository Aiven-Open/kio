"""
Generated from DescribeAclsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class AclDescription:
    __flexible__: ClassVar[bool] = False
    principal: str = field(metadata={"kafka_type": "string"})
    """The ACL principal."""
    host: str = field(metadata={"kafka_type": "string"})
    """The ACL host."""
    operation: int = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: int = field(metadata={"kafka_type": "int8"})
    """The ACL permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResource:
    __flexible__: ClassVar[bool] = False
    resource_type: int = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    acls: tuple[AclDescription, ...]
    """The ACLs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    resources: tuple[DescribeAclsResource, ...]
    """Each Resource that is referenced in an ACL."""
