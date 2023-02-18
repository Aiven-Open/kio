"""
Generated from AllocateProducerIdsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.types import ProducerId


@dataclass(frozen=True, slots=True, kw_only=True)
class AllocateProducerIdsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level response error code"""
    producer_id_start: ProducerId = field(metadata={"kafka_type": "int64"})
    """The first producer ID in this range, inclusive"""
    producer_id_len: i32 = field(metadata={"kafka_type": "int32"})
    """The number of producer IDs in this range"""
