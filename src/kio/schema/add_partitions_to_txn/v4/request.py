"""
Generated from AddPartitionsToTxnRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AddPartitionsToTxnRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.schema.types import TransactionalId
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopic:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes to add to the transaction"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTransaction:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """Current producer id in use by the transactional id."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """Current epoch associated with the producer id."""
    verify_only: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Boolean to signify if we want to check if the partition is in the transaction rather than add it."""
    topics: tuple[AddPartitionsToTxnTopic, ...]
    """The partitions to add to the transaction."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactions: tuple[AddPartitionsToTxnTransaction, ...]
    """List of transactions to add partitions to."""
