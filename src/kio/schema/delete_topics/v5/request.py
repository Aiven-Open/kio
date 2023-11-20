"""
Generated from DeleteTopicsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DeleteTopicsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The names of the topics to delete"""
    timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
