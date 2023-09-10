"""
Generated from ControlledShutdownRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ControlledShutdownRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ControlledShutdownRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(7)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The id of the broker for which controlled shutdown has been requested."""
