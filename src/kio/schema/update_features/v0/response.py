"""
Generated from UpdateFeaturesResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdatableFeatureResult:
    __flexible__: ClassVar[bool] = True
    feature: str = field(metadata={"kafka_type": "string"})
    """The name of the finalized feature."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The feature update error code or `0` if the feature update succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The feature update error, or `null` if the feature update succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateFeaturesResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or `0` if there was no top-level error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The top-level error message, or `null` if there was no top-level error."""
    results: tuple[UpdatableFeatureResult, ...]
    """Results for each feature update."""
