"""
Generated from FindCoordinatorResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/FindCoordinatorResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(10)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    node_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The node id."""
    host: str = field(metadata={"kafka_type": "string"})
    """The host name."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The port."""
