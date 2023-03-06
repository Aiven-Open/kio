"""
Generated from DeleteTopicsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The names of the topics to delete"""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
