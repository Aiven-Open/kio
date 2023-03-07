"""
Generated from InitProducerIdRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(22)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId | None = field(metadata={"kafka_type": "string"})
    """The transactional id, or null if the producer is not transactional."""
    transaction_timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The time in ms to wait before aborting idle transactions sent by this producer. This is only relevant if a TransactionalId has been defined."""
