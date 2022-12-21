"""
Generated from DeleteAclsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsFilter:
    __flexible__: ClassVar[bool] = True
    resource_type_filter: int = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name_filter: str | None = field(metadata={"kafka_type": "string"})
    """The resource name."""
    pattern_type_filter: int = field(metadata={"kafka_type": "int8"}, default=3)
    """The pattern type."""
    principal_filter: str | None = field(metadata={"kafka_type": "string"})
    """The principal filter, or null to accept all principals."""
    host_filter: str | None = field(metadata={"kafka_type": "string"})
    """The host filter, or null to accept all hosts."""
    operation: int = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: int = field(metadata={"kafka_type": "int8"})
    """The permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsRequest:
    __flexible__: ClassVar[bool] = True
    filters: tuple[DeleteAclsFilter, ...]
    """The filters to use when deleting ACLs."""
