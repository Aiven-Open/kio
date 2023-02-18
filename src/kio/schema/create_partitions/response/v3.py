"""
Generated from CreatePartitionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsTopicResult:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The result error, or zero if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The result message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePartitionsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[CreatePartitionsTopicResult, ...]
    """The partition creation results for each topic."""
