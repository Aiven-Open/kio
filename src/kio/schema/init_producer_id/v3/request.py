"""
Generated from ``clients/src/main/resources/common/message/InitProducerIdRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(22)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId | None = field(metadata={"kafka_type": "string"})
    """The transactional id, or null if the producer is not transactional."""
    transaction_timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The time in ms to wait before aborting idle transactions sent by this producer. This is only relevant if a TransactionalId has been defined."""
    producer_id: ProducerId = field(
        metadata={"kafka_type": "int64"}, default=ProducerId(-1)
    )
    """The producer id. This is used to disambiguate requests if a transactional id is reused following its expiration."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"}, default=i16(-1))
    """The producer's current epoch. This will be checked against the producer epoch on the broker, and the request will return an error if they do not match."""
