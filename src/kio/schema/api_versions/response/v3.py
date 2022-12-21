"""
Generated from ApiVersionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersion:
    __flexible__: ClassVar[bool] = True
    api_key: int = field(metadata={"kafka_type": "int16"})
    """The API index."""
    min_version: int = field(metadata={"kafka_type": "int16"})
    """The minimum supported version, inclusive."""
    max_version: int = field(metadata={"kafka_type": "int16"})
    """The maximum supported version, inclusive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SupportedFeatureKey:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the feature."""
    min_version: int = field(metadata={"kafka_type": "int16"})
    """The minimum supported version for the feature."""
    max_version: int = field(metadata={"kafka_type": "int16"})
    """The maximum supported version for the feature."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FinalizedFeatureKey:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the feature."""
    max_version_level: int = field(metadata={"kafka_type": "int16"})
    """The cluster-wide finalized max version level for the feature."""
    min_version_level: int = field(metadata={"kafka_type": "int16"})
    """The cluster-wide finalized min version level for the feature."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsResponse:
    __flexible__: ClassVar[bool] = True
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error code."""
    api_keys: tuple[ApiVersion, ...]
    """The APIs supported by the broker."""
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    supported_features: tuple[SupportedFeatureKey, ...]
    """Features supported by the broker."""
    finalized_features_epoch: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The monotonically increasing epoch for the finalized features information. Valid values are >= 0. A value of -1 is special and represents unknown epoch."""
    finalized_features: tuple[FinalizedFeatureKey, ...]
    """List of cluster-wide finalized features. The information is valid only if FinalizedFeaturesEpoch >= 0."""
