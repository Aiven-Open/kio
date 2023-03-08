"""
Generated from DeleteTopicsResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletableTopicResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The deletion error, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(20)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    responses: tuple[DeletableTopicResult, ...]
    """The results for each topic we tried to delete."""
