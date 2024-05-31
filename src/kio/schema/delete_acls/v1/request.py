"""
Generated from ``clients/src/main/resources/common/message/DeleteAclsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsFilter:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(31)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type_filter: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name_filter: str | None = field(metadata={"kafka_type": "string"})
    """The resource name."""
    pattern_type_filter: i8 = field(metadata={"kafka_type": "int8"}, default=i8(3))
    """The pattern type."""
    principal_filter: str | None = field(metadata={"kafka_type": "string"})
    """The principal filter, or null to accept all principals."""
    host_filter: str | None = field(metadata={"kafka_type": "string"})
    """The host filter, or null to accept all hosts."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAclsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(31)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    filters: tuple[DeleteAclsFilter, ...]
    """The filters to use when deleting ACLs."""
