"""
Generated from AddOffsetsToTxnRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AddOffsetsToTxnRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AddOffsetsToTxnRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(25)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """Current producer id in use by the transactional id."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """Current epoch associated with the producer id."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
