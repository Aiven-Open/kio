"""
Generated from InitProducerIdRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdRequest:
    __flexible__: ClassVar[bool] = True
    transactional_id: TransactionalId | None = field(metadata={"kafka_type": "string"})
    """The transactional id, or null if the producer is not transactional."""
    transaction_timeout_ms: int = field(metadata={"kafka_type": "int32"})
    """The time in ms to wait before aborting idle transactions sent by this producer. This is only relevant if a TransactionalId has been defined."""
