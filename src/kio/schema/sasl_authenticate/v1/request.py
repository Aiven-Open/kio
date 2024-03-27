"""
Generated from ``clients/src/main/resources/common/message/SaslAuthenticateRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(36)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    auth_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The SASL authentication bytes from the client, as defined by the SASL mechanism."""
