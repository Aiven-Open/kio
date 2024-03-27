"""
Generated from ``clients/src/main/resources/common/message/DeleteTopicsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The names of the topics to delete"""
    timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
