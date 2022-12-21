"""
Generated from EndTxnRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class EndTxnRequest:
    __flexible__: ClassVar[bool] = False
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The ID of the transaction to end."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The producer ID."""
    producer_epoch: int = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer."""
    committed: bool = field(metadata={"kafka_type": "bool"})
    """True if the transaction was committed, false if it was aborted."""
