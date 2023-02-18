"""
Generated from ConsumerProtocolSubscription.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolSubscription:
    __flexible__: ClassVar[bool] = False
    topics: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
