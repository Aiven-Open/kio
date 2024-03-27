"""
Generated from ``clients/src/main/resources/common/message/DescribeDelegationTokenRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenOwner:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(41)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The owner principal type."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The owner principal name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(41)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    owners: tuple[DescribeDelegationTokenOwner, ...] | None
    """Each owner that we want to describe delegation tokens for, or null to describe all tokens."""
