"""
Generated from InitProducerIdRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdRequest:
    __flexible__: ClassVar[bool] = True
    transactional_id: TransactionalId | None = field(metadata={"kafka_type": "string"})
    """The transactional id, or null if the producer is not transactional."""
    transaction_timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The time in ms to wait before aborting idle transactions sent by this producer. This is only relevant if a TransactionalId has been defined."""
    producer_id: ProducerId = field(
        metadata={"kafka_type": "int64"}, default=ProducerId(-1)
    )
    """The producer id. This is used to disambiguate requests if a transactional id is reused following its expiration."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"}, default=i16(-1))
    """The producer's current epoch. This will be checked against the producer epoch on the broker, and the request will return an error if they do not match."""
