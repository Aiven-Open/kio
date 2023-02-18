"""
Generated from ApiVersionsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsRequest:
    __flexible__: ClassVar[bool] = True
    client_software_name: str = field(metadata={"kafka_type": "string"})
    """The name of the client."""
    client_software_version: str = field(metadata={"kafka_type": "string"})
    """The version of the client."""
