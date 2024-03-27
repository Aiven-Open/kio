"""
Generated from ``clients/src/main/resources/common/message/WriteTxnMarkersRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The indexes of the partitions to write transaction markers for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarker:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The current producer ID."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer ID."""
    transaction_result: bool = field(metadata={"kafka_type": "bool"})
    """The result of the transaction to write to the partitions (false = ABORT, true = COMMIT)."""
    topics: tuple[WritableTxnMarkerTopic, ...]
    """Each topic that we want to write transaction marker(s) for."""
    coordinator_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """Epoch associated with the transaction state partition hosted by this transaction coordinator"""


@dataclass(frozen=True, slots=True, kw_only=True)
class WriteTxnMarkersRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    markers: tuple[WritableTxnMarker, ...]
    """The transaction markers to be written."""
