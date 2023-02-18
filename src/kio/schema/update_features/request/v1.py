"""
Generated from UpdateFeaturesRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureUpdateKey:
    __flexible__: ClassVar[bool] = True
    feature: str = field(metadata={"kafka_type": "string"})
    """The name of the finalized feature to be updated."""
    max_version_level: i16 = field(metadata={"kafka_type": "int16"})
    """The new maximum version level for the finalized feature. A value >= 1 is valid. A value < 1, is special, and can be used to request the deletion of the finalized feature."""
    upgrade_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(1))
    """Determine which type of upgrade will be performed: 1 will perform an upgrade only (default), 2 is safe downgrades only (lossless), 3 is unsafe downgrades (lossy)."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateFeaturesRequest:
    __flexible__: ClassVar[bool] = True
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """How long to wait in milliseconds before timing out the request."""
    feature_updates: tuple[FeatureUpdateKey, ...]
    """The list of updates to finalized features."""
    validate_only: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if we should validate the request, but not perform the upgrade or downgrade."""
