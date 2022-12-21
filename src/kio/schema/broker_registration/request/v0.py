"""
Generated from BrokerRegistrationRequest.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class Listener:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the endpoint."""
    host: str = field(metadata={"kafka_type": "string"})
    """The hostname."""
    port: int = field(metadata={"kafka_type": "uint16"})
    """The port."""
    security_protocol: int = field(metadata={"kafka_type": "int16"})
    """The security protocol."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Feature:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The feature name."""
    min_supported_version: int = field(metadata={"kafka_type": "int16"})
    """The minimum supported feature level."""
    max_supported_version: int = field(metadata={"kafka_type": "int16"})
    """The maximum supported feature level."""


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerRegistrationRequest:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    cluster_id: str = field(metadata={"kafka_type": "string"})
    """The cluster id of the broker process."""
    incarnation_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The incarnation id of the broker process."""
    listeners: tuple[Listener, ...]
    """The listeners of this broker"""
    features: tuple[Feature, ...]
    """The features on this broker"""
    rack: str | None = field(metadata={"kafka_type": "string"})
    """The rack which this broker is in."""
