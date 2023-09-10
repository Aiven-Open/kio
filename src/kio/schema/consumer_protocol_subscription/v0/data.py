"""
Generated from ConsumerProtocolSubscription.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ConsumerProtocolSubscription.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolSubscription:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    topics: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
