"""
Generated from AlterConfigsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterConfigsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterableConfig:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(33)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration key name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The value to set for the configuration key."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResource:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(33)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    configs: tuple[AlterableConfig, ...]
    """The configurations."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(33)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resources: tuple[AlterConfigsResource, ...]
    """The updates for each resource."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """True if we should validate the request, but not change the configurations."""
