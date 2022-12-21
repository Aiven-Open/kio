"""
Generated from SaslHandshakeResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslHandshakeResponse:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    mechanisms: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    """The mechanisms enabled in the server."""
