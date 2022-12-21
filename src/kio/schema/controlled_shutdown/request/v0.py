"""
Generated from ControlledShutdownRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class ControlledShutdownRequest:
    __flexible__: ClassVar[bool] = False
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The id of the broker for which controlled shutdown has been requested."""
