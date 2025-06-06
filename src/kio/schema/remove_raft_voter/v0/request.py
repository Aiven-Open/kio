"""
Generated from ``clients/src/main/resources/common/message/RemoveRaftVoterRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class RemoveRaftVoterRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(81)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    cluster_id: str | None = field(metadata={"kafka_type": "string"})
    voter_id: i32 = field(metadata={"kafka_type": "int32"})
    """The replica id of the voter getting removed from the topic partition"""
    voter_directory_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The directory id of the voter getting removed from the topic partition"""
