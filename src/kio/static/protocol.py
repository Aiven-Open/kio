from typing import ClassVar
from typing import Protocol

from kio._utils import DataclassInstance

from .primitive import i16

__all__ = ("ApiMessage", "Entity", "Payload")


class ApiMessage:
    pass


class Entity(DataclassInstance, Protocol):
    """All schema entities adhere to this protocol."""

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
    def __header_schema__(self) -> type[Entity]:
        """
        The header entity type that should be used when sending or receiving this
        payload.
        """
