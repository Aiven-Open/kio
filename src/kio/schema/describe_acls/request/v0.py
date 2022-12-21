"""
Generated from DescribeAclsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsRequest:
    __flexible__: ClassVar[bool] = False
    resource_type_filter: int = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name_filter: str | None = field(metadata={"kafka_type": "string"})
    """The resource name, or null to match any resource name."""
    principal_filter: str | None = field(metadata={"kafka_type": "string"})
    """The principal to match, or null to match any principal."""
    host_filter: str | None = field(metadata={"kafka_type": "string"})
    """The host to match, or null to match any host."""
    operation: int = field(metadata={"kafka_type": "int8"})
    """The operation to match."""
    permission_type: int = field(metadata={"kafka_type": "int8"})
    """The permission type to match."""
