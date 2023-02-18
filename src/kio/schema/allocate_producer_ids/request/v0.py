"""
Generated from AllocateProducerIdsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i64
from kio.schema.types import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class AllocateProducerIdsRequest:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The epoch of the requesting broker"""
