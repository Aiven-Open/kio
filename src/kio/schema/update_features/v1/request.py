"""
Generated from ``clients/src/main/resources/common/message/UpdateFeaturesRequest.json``.
"""

import datetime

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureUpdateKey:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(57)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    feature: str = field(metadata={"kafka_type": "string"})
    """The name of the finalized feature to be updated."""
    max_version_level: i16 = field(metadata={"kafka_type": "int16"})
    """The new maximum version level for the finalized feature. A value >= 1 is valid. A value < 1, is special, and can be used to request the deletion of the finalized feature."""
    upgrade_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(1))
    """Determine which type of upgrade will be performed: 1 will perform an upgrade only (default), 2 is safe downgrades only (lossless), 3 is unsafe downgrades (lossy)."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateFeaturesRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(57)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=60000)),
    )
    """How long to wait in milliseconds before timing out the request."""
    feature_updates: tuple[FeatureUpdateKey, ...]
    """The list of updates to finalized features."""
    validate_only: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if we should validate the request, but not perform the upgrade or downgrade."""
