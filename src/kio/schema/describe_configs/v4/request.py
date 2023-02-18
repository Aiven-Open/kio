"""
Generated from DescribeConfigsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResource:
    __flexible__: ClassVar[bool] = True
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    configuration_keys: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The configuration keys to list, or null to list all configuration keys."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsRequest:
    __flexible__: ClassVar[bool] = True
    resources: tuple[DescribeConfigsResource, ...]
    """The resources whose configurations we want to describe."""
    include_synonyms: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if we should include all synonyms."""
    include_documentation: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if we should include configuration documentation."""
