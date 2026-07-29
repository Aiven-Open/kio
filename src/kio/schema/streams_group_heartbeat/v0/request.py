"""
Generated from ``clients/src/main/resources/common/message/StreamsGroupHeartbeatRequest.json``.
"""

import datetime

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
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
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    key: str = field(metadata={"kafka_type": "string"})
    """key of the config"""
    value: str = field(metadata={"kafka_type": "string"})
    """value of the config"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicInfo:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: i32 = field(metadata={"kafka_type": "int32"})
    """The number of partitions in the topic. Can be 0 if no specific number of partitions is enforced. Always 0 for changelog topics."""
    replication_factor: i16 = field(metadata={"kafka_type": "int16"})
    """The replication factor of the topic. Can be 0 if the default replication factor should be used."""
    topic_configs: tuple[KeyValue, ...]
    """Topic-level configurations as key-value pairs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CopartitionGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    source_topics: tuple[i16, ...] = field(metadata={"kafka_type": "int16"}, default=())
    """The topics the topology reads from. Index into the array on the subtopology level."""
    source_topic_regex: tuple[i16, ...] = field(
        metadata={"kafka_type": "int16"}, default=()
    )
    """Regular expressions identifying topics the subtopology reads from. Index into the array on the subtopology level."""
    repartition_source_topics: tuple[i16, ...] = field(
        metadata={"kafka_type": "int16"}, default=()
    )
    """The set of source topics that are internally created repartition topics. Index into the array on the subtopology level."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Subtopology:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """String to uniquely identify the subtopology. Deterministically generated from the topology"""
    source_topics: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The topics the topology reads from."""
    source_topic_regex: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The regular expressions identifying topics the subtopology reads from."""
    state_changelog_topics: tuple[TopicInfo, ...]
    """The set of state changelog topics associated with this subtopology. Created automatically."""
    repartition_sink_topics: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The repartition topics the subtopology writes to."""
    repartition_source_topics: tuple[TopicInfo, ...]
    """The set of source topics that are internally created repartition topics. Created automatically."""
    copartition_groups: tuple[CopartitionGroup, ...]
    """A subset of source topics that must be copartitioned."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Topology:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch of the topology. Used to check if the topology corresponds to the topology initialized on the brokers."""
    subtopologies: tuple[Subtopology, ...]
    """The sub-topologies of the streams application."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskIds:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """The subtopology identifier."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions of the input topics processed by this member."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Endpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    host: str = field(metadata={"kafka_type": "string"})
    """host of the endpoint"""
    port: u16 = field(metadata={"kafka_type": "uint16"})
    """port of the endpoint"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskOffset:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """The subtopology identifier."""
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition."""
    offset: i64 = field(metadata={"kafka_type": "int64"})
    """The offset."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StreamsGroupHeartbeatRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(88)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID generated by the streams consumer. The member ID must be kept during the entire lifetime of the streams consumer process."""
    member_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current member epoch; 0 to join the group; -1 to leave the group; -2 to indicate that the static member will rejoin."""
    endpoint_information_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current endpoint epoch of this client, represents the latest endpoint epoch this client received"""
    instance_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """null if not provided or if it didn't change since the last heartbeat; the instance ID for static membership otherwise."""
    rack_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """null if not provided or if it didn't change since the last heartbeat; the rack ID of the member otherwise."""
    rebalance_timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=-1)),
    )
    """-1 if it didn't change since the last heartbeat; the maximum time in milliseconds that the coordinator will wait on the member to revoke its tasks otherwise."""
    topology: Topology | None = field(default=None)
    """The topology metadata of the streams application. Used to initialize the topology of the group and to check if the topology corresponds to the topology initialized for the group. Only sent when memberEpoch = 0, must be non-empty. Null otherwise."""
    active_tasks: tuple[TaskIds, ...] | None
    """Currently owned active tasks for this client. Null if unchanged since last heartbeat."""
    standby_tasks: tuple[TaskIds, ...] | None
    """Currently owned standby tasks for this client. Null if unchanged since last heartbeat."""
    warmup_tasks: tuple[TaskIds, ...] | None
    """Currently owned warm-up tasks for this client. Null if unchanged since last heartbeat."""
    process_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """Identity of the streams instance that may have multiple consumers. Null if unchanged since last heartbeat."""
    user_endpoint: Endpoint | None = field(default=None)
    """User-defined endpoint for Interactive Queries. Null if unchanged since last heartbeat, or if not defined on the client."""
    client_tags: tuple[KeyValue, ...] | None
    """Used for rack-aware assignment algorithm. Null if unchanged since last heartbeat."""
    task_offsets: tuple[TaskOffset, ...] | None
    """Cumulative changelog offsets for tasks. Only updated when a warm-up task has caught up, and according to the task offset interval. Null if unchanged since last heartbeat."""
    task_end_offsets: tuple[TaskOffset, ...] | None
    """Cumulative changelog end-offsets for tasks. Only updated when a warm-up task has caught up, and according to the task offset interval. Null if unchanged since last heartbeat."""
    shutdown_application: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Whether all Streams clients in the group should shut down."""
