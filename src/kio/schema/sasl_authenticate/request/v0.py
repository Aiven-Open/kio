"""
Generated from SaslAuthenticateRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateRequest:
    __flexible__: ClassVar[bool] = False
    auth_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The SASL authentication bytes from the client, as defined by the SASL mechanism."""
