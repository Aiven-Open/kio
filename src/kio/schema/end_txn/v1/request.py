"""
Generated from ``clients/src/main/resources/common/message/EndTxnRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class EndTxnRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(26)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The ID of the transaction to end."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The producer ID."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer."""
    committed: bool = field(metadata={"kafka_type": "bool"})
    """True if the transaction was committed, false if it was aborted."""
