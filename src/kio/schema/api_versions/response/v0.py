"""
Generated from ApiVersionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersion:
    __flexible__: ClassVar[bool] = False
    api_key: int = field(metadata={"kafka_type": "int16"})
    """The API index."""
    min_version: int = field(metadata={"kafka_type": "int16"})
    """The minimum supported version, inclusive."""
    max_version: int = field(metadata={"kafka_type": "int16"})
    """The maximum supported version, inclusive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsResponse:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error code."""
    api_keys: tuple[ApiVersion, ...]
    """The APIs supported by the broker."""
