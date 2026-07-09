"""
Generated from ``clients/src/main/resources/common/message/StreamsGroupDescribeResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.primitive import u16


@dataclass(frozen=True, slots=True, kw_only=True)
class KeyValue:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    key: str = field(metadata={"kafka_type": "string"})
    """key of the config"""
    value: str = field(metadata={"kafka_type": "string"})
    """value of the config"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicInfo:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: i32 = field(metadata={"kafka_type": "int32"})
    """The number of partitions in the topic. Can be 0 if no specific number of partitions is enforced. Always 0 for changelog topics."""
    replication_factor: i16 = field(metadata={"kafka_type": "int16"})
    """The replication factor of the topic. Can be 0 if the default replication factor should be used."""
    topic_configs: tuple[KeyValue, ...]
    """Topic-level configurations as key-value pairs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Subtopology:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """String to uniquely identify the subtopology."""
    source_topics: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The topics the subtopology reads from."""
    repartition_sink_topics: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The repartition topics the subtopology writes to."""
    state_changelog_topics: tuple[TopicInfo, ...]
    """The set of state changelog topics associated with this subtopology. Created automatically."""
    repartition_source_topics: tuple[TopicInfo, ...]
    """The set of source topics that are internally created repartition topics. Created automatically."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Topology:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch of the currently initialized topology for this group."""
    subtopologies: tuple[Subtopology, ...] | None
    """The subtopologies of the streams application. This contains the configured subtopologies, where the number of partitions are set and any regular expressions are resolved to actual topics. Null if the group is uninitialized, source topics are missing or incorrectly partitioned."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Endpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    host: str = field(metadata={"kafka_type": "string"})
    """host of the endpoint"""
    port: u16 = field(metadata={"kafka_type": "uint16"})
    """port of the endpoint"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskOffset:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """The subtopology identifier."""
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition."""
    offset: i64 = field(metadata={"kafka_type": "int64"})
    """The offset."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskIds:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """The subtopology identifier."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions of the input topics processed by this member."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Assignment:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    active_tasks: tuple[TaskIds, ...]
    """Active tasks for this client."""
    standby_tasks: tuple[TaskIds, ...]
    """Standby tasks for this client."""
    warmup_tasks: tuple[TaskIds, ...]
    """Warm-up tasks for this client. """


@dataclass(frozen=True, slots=True, kw_only=True)
class Member:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID."""
    member_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The member epoch."""
    instance_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The member instance ID for static membership."""
    rack_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The rack ID."""
    client_id: str = field(metadata={"kafka_type": "string"})
    """The client ID."""
    client_host: str = field(metadata={"kafka_type": "string"})
    """The client host."""
    topology_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch of the topology on the client."""
    process_id: str = field(metadata={"kafka_type": "string"})
    """Identity of the streams instance that may have multiple clients. """
    user_endpoint: Endpoint | None = field(default=None)
    """User-defined endpoint for Interactive Queries. Null if not defined for this client."""
    client_tags: tuple[KeyValue, ...]
    """Used for rack-aware assignment algorithm."""
    task_offsets: tuple[TaskOffset, ...]
    """Cumulative changelog offsets for tasks."""
    task_end_offsets: tuple[TaskOffset, ...]
    """Cumulative changelog end offsets for tasks."""
    assignment: Assignment
    """The current assignment."""
    target_assignment: Assignment
    """The target assignment."""
    is_classic: bool = field(metadata={"kafka_type": "bool"})
    """True for classic members that have not been upgraded yet."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The describe error, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID string."""
    group_state: str = field(metadata={"kafka_type": "string"})
    """The group state string, or the empty string."""
    group_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The group epoch."""
    assignment_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The assignment epoch."""
    topology: Topology | None = field(default=None)
    """The topology metadata currently initialized for the streams application. Can be null in case of a describe error."""
    members: tuple[Member, ...]
    """The members."""
    authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StreamsGroupDescribeResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(89)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[DescribedGroup, ...]
    """Each described group."""
