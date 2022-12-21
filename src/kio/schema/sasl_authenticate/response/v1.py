"""
Generated from SaslAuthenticateResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateResponse:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    auth_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The SASL authentication bytes from the server, as defined by the SASL mechanism."""
    session_lifetime_ms: int = field(metadata={"kafka_type": "int64"}, default=0)
    """The SASL authentication bytes from the server, as defined by the SASL mechanism."""
