"""
Generated from SaslAuthenticateResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateResponse:
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    auth_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The SASL authentication bytes from the server, as defined by the SASL mechanism."""
    session_lifetime_ms: i64 = field(metadata={"kafka_type": "int64"}, default=i64(0))
    """The SASL authentication bytes from the server, as defined by the SASL mechanism."""
