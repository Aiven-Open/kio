"""
Generated from ``clients/src/main/resources/common/message/EnvelopeRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvelopeRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(58)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    request_data: bytes = field(metadata={"kafka_type": "bytes"})
    """The embedded request header and data."""
    request_principal: bytes | None = field(metadata={"kafka_type": "bytes"})
    """Value of the initial client principal when the request is redirected by a broker."""
    client_host_address: bytes = field(metadata={"kafka_type": "bytes"})
    """The original client's address in bytes."""
