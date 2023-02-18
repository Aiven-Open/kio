"""
Generated from AddOffsetsToTxnRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.entity import ProducerId
from kio.schema.entity import TransactionalId
from kio.schema.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class AddOffsetsToTxnRequest:
    __flexible__: ClassVar[bool] = False
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """Current producer id in use by the transactional id."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """Current epoch associated with the producer id."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
