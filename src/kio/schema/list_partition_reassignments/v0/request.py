"""
Generated from ListPartitionReassignmentsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListPartitionReassignmentsRequest.json
"""

import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ListPartitionReassignmentsTopics:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(46)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partitions to list partition reassignments for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListPartitionReassignmentsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(46)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=60000)),
    )
    """The time in ms to wait for the request to complete."""
    topics: tuple[ListPartitionReassignmentsTopics, ...]
    """The topics to list partition reassignments for, or null to list everything."""
