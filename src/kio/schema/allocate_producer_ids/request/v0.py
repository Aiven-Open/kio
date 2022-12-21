"""
Generated from AllocateProducerIdsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class AllocateProducerIdsRequest:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The epoch of the requesting broker"""
