"""
Generated from ``clients/src/main/resources/common/message/ApiVersionsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersion:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    api_key: i16 = field(metadata={"kafka_type": "int16"})
    """The API index."""
    min_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported version, inclusive."""
    max_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported version, inclusive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SupportedFeatureKey:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the feature."""
    min_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported version for the feature."""
    max_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported version for the feature."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FinalizedFeatureKey:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the feature."""
    max_version_level: i16 = field(metadata={"kafka_type": "int16"})
    """The cluster-wide finalized max version level for the feature."""
    min_version_level: i16 = field(metadata={"kafka_type": "int16"})
    """The cluster-wide finalized min version level for the feature."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code."""
    api_keys: tuple[ApiVersion, ...]
    """The APIs supported by the broker."""
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    supported_features: tuple[SupportedFeatureKey, ...] = field(
        metadata={"tag": 0}, default=()
    )
    """Features supported by the broker."""
    finalized_features_epoch: i64 = field(
        metadata={"kafka_type": "int64", "tag": 1}, default=i64(-1)
    )
    """The monotonically increasing epoch for the finalized features information. Valid values are >= 0. A value of -1 is special and represents unknown epoch."""
    finalized_features: tuple[FinalizedFeatureKey, ...] = field(
        metadata={"tag": 2}, default=()
    )
    """List of cluster-wide finalized features. The information is valid only if FinalizedFeaturesEpoch >= 0."""
    zk_migration_ready: bool = field(
        metadata={"kafka_type": "bool", "tag": 3}, default=False
    )
    """Set by a KRaft controller if the required configurations for ZK migration are present"""
