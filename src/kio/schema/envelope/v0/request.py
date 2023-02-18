"""
Generated from EnvelopeRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvelopeRequest:
    __flexible__: ClassVar[bool] = True
    request_data: bytes = field(metadata={"kafka_type": "bytes"})
    """The embedded request header and data."""
    request_principal: bytes | None = field(metadata={"kafka_type": "bytes"})
    """Value of the initial client principal when the request is redirected by a broker."""
    client_host_address: bytes = field(metadata={"kafka_type": "bytes"})
    """The original client's address in bytes."""
