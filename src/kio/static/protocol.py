from __future__ import annotations

from typing import ClassVar
from typing import Protocol
from typing import TypeAlias

import kio.schema.request_header.v0
import kio.schema.request_header.v1
import kio.schema.request_header.v2
import kio.schema.response_header.v0
import kio.schema.response_header.v1

from kio._utils import DataclassInstance

from .constants import EntityType
from .primitive import i16

__all__ = (
    "Entity",
    "Payload",
    "ResponsePayload",
    "RequestPayload",
    "RequestHeader",
    "ResponseHeader",
    "Header",
    "HeaderV0RequestPayload",
    "HeaderV1RequestPayload",
    "HeaderV2RequestPayload",
    "HeaderV0ResponsePayload",
    "HeaderV1ResponsePayload",
)


RequestHeader: TypeAlias = (
    kio.schema.request_header.v0.RequestHeader
    | kio.schema.request_header.v1.RequestHeader
    | kio.schema.request_header.v2.RequestHeader
)
"""Convenient union type of all possible request header types."""
ResponseHeader: TypeAlias = (
    kio.schema.response_header.v0.ResponseHeader
    | kio.schema.response_header.v1.ResponseHeader
)
"""Convenient union type of all possible response header types."""
Header: TypeAlias = RequestHeader | ResponseHeader
"""Convenient union type of all possible request and response header types."""


class Entity(DataclassInstance, Protocol):
    """All schema entities adhere to this protocol."""

    __type__: ClassVar[EntityType]
    __version__: ClassVar[i16]
    """The version of the protocol API that the entity is modeling."""
    __flexible__: ClassVar[bool]
    """
    Whether the API version is "flexible" or not, see `upstream protocol documentation
    <https://github.com/apache/kafka/tree/79b5f7f/clients/src/main/resources/common/message#flexible-versions>`_.
    """


# Apache Kafka® calls this "message", but it also calls the whole message (header +
# payload) "message", so to disambiguate, we call this part of the message
# "payload" instead.
class Payload(DataclassInstance, Protocol):
    """
    All payload entities, i.e. `requests and responses
    <https://kafka.apache.org/protocol#protocol_api_keys>`_, adhere to this protocol.
    """

    __type__: ClassVar[EntityType]
    __version__: ClassVar[i16]
    """The version of the protocol API that the entity is modeling."""
    __flexible__: ClassVar[bool]
    """
    Whether the API version is "flexible" or not, see `upstream protocol documentation
    <https://github.com/apache/kafka/tree/79b5f7f/clients/src/main/resources/common/message#flexible-versions>`_.
    """
    __api_key__: ClassVar[i16]
    """
    Corresponding key_ of the modeled API.

    .. _key: https://kafka.apache.org/protocol#protocol_api_keys
    """

    # This must be defined as a property without a setter, otherwise subclasses cannot
    # narrow the type to a subtype of Entity, because to fulfill LSP they would be
    # required to accept ANY subtype of Entity as set-type. This is quirky but sound
    # from static type checking perspective.
    @property
    def __header_schema__(self) -> type[Header]:
        """
        The header entity type that should be used when sending or receiving this
        payload.
        """


class HeaderV0RequestPayload(Payload, Protocol):
    """Protocol describing a request payload entity type with a V0 header."""

    __header_schema__: ClassVar[type[kio.schema.request_header.v0.RequestHeader]]


class HeaderV1RequestPayload(Payload, Protocol):
    """Protocol describing a request payload entity type with a V1 header."""

    __header_schema__: ClassVar[type[kio.schema.request_header.v1.RequestHeader]]


class HeaderV2RequestPayload(Payload, Protocol):
    """Protocol describing a request payload entity type with a V2 header."""

    __header_schema__: ClassVar[type[kio.schema.request_header.v2.RequestHeader]]


RequestPayload: TypeAlias = (
    HeaderV0RequestPayload | HeaderV1RequestPayload | HeaderV2RequestPayload
)
"""Convenient union type of all possible request payloads."""


class HeaderV0ResponsePayload(Payload, Protocol):
    """Protocol describing a response payload entity type with a V0 header."""

    __header_schema__: ClassVar[type[kio.schema.response_header.v0.ResponseHeader]]


class HeaderV1ResponsePayload(Payload, Protocol):
    """Protocol describing a response payload entity type with a V1 header."""

    __header_schema__: ClassVar[type[kio.schema.response_header.v1.ResponseHeader]]


ResponsePayload: TypeAlias = HeaderV0ResponsePayload | HeaderV1ResponsePayload
"""Convenient union type of all possible response payloads."""
