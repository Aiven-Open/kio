# Note! This file is auto-generated from a template, make changes in
# codegen/template/protocol.py.

from typing import ClassVar
from typing import Protocol

from .primitive import i16


class Entity(Protocol):
    __version__: ClassVar[i16]
    __flexible__: ClassVar[bool]


# Kafka calls this "message", but it also calls the whole message (header +
# payload) "message", so to disambiguate, we call this part of the message
# "payload" instead.
class Payload(Protocol):
    __version__: ClassVar[i16]
    __flexible__: ClassVar[bool]
    __api_key__: ClassVar[i16]

    # This must be defined as a property without a setter, otherwise subclasses cannot
    # narrow the type to a subtype of Entity, because to fulfill LSP they would be
    # required to accept ANY subtype of Entity as set-type. This is quirky but sound
    # from static type checking perspective.
    @property
    def __header_schema__(self) -> type[Entity]:
        ...
