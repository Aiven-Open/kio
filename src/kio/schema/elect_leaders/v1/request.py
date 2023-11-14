"""
Generated from ElectLeadersRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ElectLeadersRequest.json
"""

import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartitions:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(43)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The name of a topic."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions of this topic whose leader should be elected."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectLeadersRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(43)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    election_type: i8 = field(metadata={"kafka_type": "int8"})
    """Type of elections to conduct for the partition. A value of '0' elects the preferred replica. A value of '1' elects the first live replica if there are no in-sync replica."""
    topic_partitions: tuple[TopicPartitions, ...]
    """The topic partitions to elect leaders."""
    timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=60000)),
    )
    """The time in ms to wait for the election to complete."""
