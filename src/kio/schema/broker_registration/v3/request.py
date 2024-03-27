"""
Generated from ``clients/src/main/resources/common/message/BrokerRegistrationRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i64
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class Listener:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(62)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the endpoint."""
    host: str = field(metadata={"kafka_type": "string"})
    """The hostname."""
    port: u16 = field(metadata={"kafka_type": "uint16"})
    """The port."""
    security_protocol: i16 = field(metadata={"kafka_type": "int16"})
    """The security protocol."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Feature:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(62)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The feature name."""
    min_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported feature level."""
    max_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported feature level."""


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerRegistrationRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(62)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    cluster_id: str = field(metadata={"kafka_type": "string"})
    """The cluster id of the broker process."""
    incarnation_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The incarnation id of the broker process."""
    listeners: tuple[Listener, ...]
    """The listeners of this broker"""
    features: tuple[Feature, ...]
    """The features on this broker"""
    rack: str | None = field(metadata={"kafka_type": "string"})
    """The rack which this broker is in."""
    is_migrating_zk_broker: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """If the required configurations for ZK migration are present, this value is set to true"""
    log_dirs: tuple[uuid.UUID | None, ...] = field(
        metadata={"kafka_type": "uuid"}, default=()
    )
    """Log directories configured in this broker which are available."""
    previous_broker_epoch: i64 = field(
        metadata={"kafka_type": "int64"}, default=i64(-1)
    )
    """The epoch before a clean shutdown."""
