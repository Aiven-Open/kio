"""
Generated from ``clients/src/main/resources/common/message/ControllerRegistrationRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class Listener:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(70)
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
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(70)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The feature name."""
    min_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported feature level."""
    max_supported_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported feature level."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ControllerRegistrationRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(70)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    controller_id: i32 = field(metadata={"kafka_type": "int32"})
    """The ID of the controller to register."""
    incarnation_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The controller incarnation ID, which is unique to each process run."""
    zk_migration_ready: bool = field(metadata={"kafka_type": "bool"})
    """Set if the required configurations for ZK migration are present."""
    listeners: tuple[Listener, ...]
    """The listeners of this controller"""
    features: tuple[Feature, ...]
    """The features on this controller"""
