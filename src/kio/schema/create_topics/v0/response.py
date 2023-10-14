"""
Generated from CreateTopicsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/CreateTopicsResponse.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topics: tuple[CreatableTopicResult, ...]
    """Results for each topic we tried to create."""
