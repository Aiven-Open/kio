"""
Generated from InitProducerIdRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/InitProducerIdRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TransactionalId
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class InitProducerIdRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(22)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId | None = field(metadata={"kafka_type": "string"})
    """The transactional id, or null if the producer is not transactional."""
    transaction_timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The time in ms to wait before aborting idle transactions sent by this producer. This is only relevant if a TransactionalId has been defined."""
