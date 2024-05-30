"""
Generated from ``clients/src/main/resources/common/message/CreateTopicsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicConfigs:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The configuration value."""
    read_only: bool = field(metadata={"kafka_type": "bool"})
    """True if the configuration is read-only."""
    config_source: i8 = field(metadata={"kafka_type": "int8"}, default=i8(-1))
    """The configuration source."""
    is_sensitive: bool = field(metadata={"kafka_type": "bool"})
    """True if this configuration is sensitive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    topic_config_error_code: i16 = field(
        metadata={"kafka_type": "int16", "tag": 0}, default=i16(0)
    )
    """Optional topic config error returned if configs are not returned in the response."""
    num_partitions: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """Number of partitions of the topic."""
    replication_factor: i16 = field(metadata={"kafka_type": "int16"}, default=i16(-1))
    """Replication factor of the topic."""
    configs: tuple[CreatableTopicConfigs, ...] | None
    """Configuration of the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[CreatableTopicResult, ...]
    """Results for each topic we tried to create."""
