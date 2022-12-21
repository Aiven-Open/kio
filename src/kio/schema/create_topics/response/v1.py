"""
Generated from CreateTopicsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicResult:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsResponse:
    __flexible__: ClassVar[bool] = False
    topics: tuple[CreatableTopicResult, ...]
    """Results for each topic we tried to create."""
