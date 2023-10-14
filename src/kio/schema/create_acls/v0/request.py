"""
Generated from CreateAclsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/CreateAclsRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class AclCreation:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(30)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The type of the resource."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name for the ACL."""
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
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(30)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    creations: tuple[AclCreation, ...]
    """The ACLs that we want to create."""
