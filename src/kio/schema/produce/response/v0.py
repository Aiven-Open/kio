"""
Generated from ProduceResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionProduceResponse:
    __flexible__: ClassVar[bool] = False
    index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    base_offset: int = field(metadata={"kafka_type": "int64"})
    """The base offset."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicProduceResponse:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_responses: tuple[PartitionProduceResponse, ...]
    """Each partition that we produced to within the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProduceResponse:
    __flexible__: ClassVar[bool] = False
    responses: tuple[TopicProduceResponse, ...]
    """Each produce response"""
