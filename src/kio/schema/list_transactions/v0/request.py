"""
Generated from ListTransactionsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListTransactionsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import ProducerId
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ListTransactionsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(66)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    state_filters: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The transaction states to filter by: if empty, all transactions are returned; if non-empty, then only transactions matching one of the filtered states will be returned"""
    producer_id_filters: tuple[ProducerId, ...] = field(
        metadata={"kafka_type": "int64"}, default=()
    )
    """The producerIds to filter by: if empty, all transactions will be returned; if non-empty, only transactions which match one of the filtered producerIds will be returned"""
