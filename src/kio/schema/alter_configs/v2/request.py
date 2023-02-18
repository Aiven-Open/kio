"""
Generated from AlterConfigsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterableConfig:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration key name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The value to set for the configuration key."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResource:
    __flexible__: ClassVar[bool] = True
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    configs: tuple[AlterableConfig, ...]
    """The configurations."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsRequest:
    __flexible__: ClassVar[bool] = True
    resources: tuple[AlterConfigsResource, ...]
    """The updates for each resource."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """True if we should validate the request, but not change the configurations."""
