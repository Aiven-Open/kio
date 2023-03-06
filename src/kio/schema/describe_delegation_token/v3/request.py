"""
Generated from DescribeDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.request_header.v2.header import RequestHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenOwner:
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
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(41)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    owners: tuple[DescribeDelegationTokenOwner, ...]
    """Each owner that we want to describe delegation tokens for, or null to describe all tokens."""
