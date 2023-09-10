"""
Generated from DeleteTopicsRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/DeleteTopicsRequest.json
"""

# ruff: noqa: A003

import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicState:
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName | None = field(metadata={"kafka_type": "string"}, default=None)
    """The topic name"""
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest:
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[DeleteTopicState, ...]
    """The name or topic ID of the topic"""
    timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
