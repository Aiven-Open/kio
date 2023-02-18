"""
Generated from DeleteTopicsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletableTopicResult:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The deletion error, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    responses: tuple[DeletableTopicResult, ...]
    """The results for each topic we tried to delete."""
