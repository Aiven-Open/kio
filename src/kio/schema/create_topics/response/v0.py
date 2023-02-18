"""
Generated from CreateTopicsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicResult:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsResponse:
    __flexible__: ClassVar[bool] = False
    topics: tuple[CreatableTopicResult, ...]
    """Results for each topic we tried to create."""
