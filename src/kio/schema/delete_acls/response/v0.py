"""
Generated from DeleteAclsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsMatchingAcl:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The deletion error code, or 0 if the deletion succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The deletion error message, or null if the deletion succeeded."""
    resource_type: int = field(metadata={"kafka_type": "int8"})
    """The ACL resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The ACL resource name."""
    principal: str = field(metadata={"kafka_type": "string"})
    """The ACL principal."""
    host: str = field(metadata={"kafka_type": "string"})
    """The ACL host."""
    operation: int = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: int = field(metadata={"kafka_type": "int8"})
    """The ACL permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsFilterResult:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if the filter succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if the filter succeeded."""
    matching_acls: tuple[DeleteAclsMatchingAcl, ...]
    """The ACLs which matched this filter."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    filter_results: tuple[DeleteAclsFilterResult, ...]
    """The results for each filter."""
