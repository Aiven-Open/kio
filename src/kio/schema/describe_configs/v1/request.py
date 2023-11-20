"""
Generated from DescribeConfigsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeConfigsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResource:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    configuration_keys: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The configuration keys to list, or null to list all configuration keys."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    resources: tuple[DescribeConfigsResource, ...]
    """The resources whose configurations we want to describe."""
    include_synonyms: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if we should include all synonyms."""
