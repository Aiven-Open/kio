"""
Generated from ``clients/src/main/resources/common/message/DescribeUserScramCredentialsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class UserName:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The user name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    users: tuple[UserName, ...] | None
    """The users to describe, or null/empty to describe all users."""
