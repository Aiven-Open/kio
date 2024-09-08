"""
Generated from ``clients/src/main/resources/common/message/ListTransactionsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import ProducerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListTransactionsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
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
    duration_filter: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """Duration (in millis) to filter by: if < 0, all transactions will be returned; otherwise, only transactions running longer than this duration will be returned"""
