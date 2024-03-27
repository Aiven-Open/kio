"""
Generated from ``clients/src/main/resources/common/message/CreateAclsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class AclCreation:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(30)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The type of the resource."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name for the ACL."""
    resource_pattern_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(3))
    """The pattern type for the ACL."""
    principal: str = field(metadata={"kafka_type": "string"})
    """The principal for the ACL."""
    host: str = field(metadata={"kafka_type": "string"})
    """The host for the ACL."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The operation type for the ACL (read, write, etc.)."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The permission type for the ACL (allow, deny, etc.)."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateAclsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(30)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    creations: tuple[AclCreation, ...]
    """The ACLs that we want to create."""
