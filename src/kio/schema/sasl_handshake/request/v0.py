"""
Generated from SaslHandshakeRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslHandshakeRequest:
    __flexible__: ClassVar[bool] = False
    mechanism: str = field(metadata={"kafka_type": "string"})
    """The SASL mechanism chosen by the client."""
