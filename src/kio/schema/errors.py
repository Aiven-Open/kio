from __future__ import annotations

import enum

from typing import TYPE_CHECKING

from kio.static.primitive import i16


class ErrorCode(enum.IntEnum):
    retriable: bool
    value: i16

    # Note: Pragma is needed to ignore the negative branch, the branch where the
    # conditional check fails.
    if not TYPE_CHECKING:  # pragma: no cover

        def __new__(cls, value: int, retriable: bool) -> ErrorCode:
            normalized_value = i16(value)
            obj = int.__new__(cls, normalized_value)
            obj._value_ = normalized_value
            obj.retriable = retriable
            return obj

    unknown_server_error = -1, False
    """The server experienced an unexpected error when processing the request."""
    none = 0, False
    offset_out_of_range = 1, False
    """The requested offset is not within the range of offsets maintained by the server."""
    corrupt_message = 2, True
    """This message has failed its CRC checksum, exceeds the valid size, has a null key for a compacted topic, or is otherwise corrupt."""
    unknown_topic_or_partition = 3, True
    """This server does not host this topic-partition."""
    invalid_fetch_size = 4, False
    """The requested fetch size is invalid."""
    leader_not_available = 5, True
    """There is no leader for this topic-partition as we are in the middle of a leadership election."""
    not_leader_or_follower = 6, True
    """For requests intended only for the leader, this error indicates that the broker is not the current leader. For requests intended for any replica, this error indicates that the broker is not a replica of the topic partition."""
    request_timed_out = 7, True
    """The request timed out."""
    broker_not_available = 8, False
    """The broker is not available."""
    replica_not_available = 9, True
    """The replica is not available for the requested topic-partition. Produce/Fetch requests and other requests intended only for the leader or follower return NOT_LEADER_OR_FOLLOWER if the broker is not a replica of the topic-partition."""
    message_too_large = 10, False
    """The request included a message larger than the max message size the server will accept."""
    stale_controller_epoch = 11, False
    """The controller moved to another broker."""
    offset_metadata_too_large = 12, False
    """The metadata field of the offset request was too large."""
    network_exception = 13, True
    """The server disconnected before a response was received."""
    coordinator_load_in_progress = 14, True
    """The coordinator is loading and hence can't process requests."""
    coordinator_not_available = 15, True
    """The coordinator is not available."""
    not_coordinator = 16, True
    """This is not the correct coordinator."""
    invalid_topic_exception = 17, False
    """The request attempted to perform an operation on an invalid topic."""
    record_list_too_large = 18, False
    """The request included message batch larger than the configured segment size on the server."""
    not_enough_replicas = 19, True
    """Messages are rejected since there are fewer in-sync replicas than required."""
    not_enough_replicas_after_append = 20, True
    """Messages are written to the log, but to fewer in-sync replicas than required."""
    invalid_required_acks = 21, False
    """Produce request specified an invalid value for required acks."""
    illegal_generation = 22, False
    """Specified group generation id is not valid."""
    inconsistent_group_protocol = 23, False
    """The group member's supported protocols are incompatible with those of existing members or first group member tried to join with empty protocol type or empty protocol list."""
    invalid_group_id = 24, False
    """The configured groupId is invalid."""
    unknown_member_id = 25, False
    """The coordinator is not aware of this member."""
    invalid_session_timeout = 26, False
    """The session timeout is not within the range allowed by the broker (as configured by group.min.session.timeout.ms and group.max.session.timeout.ms)."""
    rebalance_in_progress = 27, False
    """The group is rebalancing, so a rejoin is needed."""
    invalid_commit_offset_size = 28, False
    """The committing offset data size is not valid."""
    topic_authorization_failed = 29, False
    """Topic authorization failed."""
    group_authorization_failed = 30, False
    """Group authorization failed."""
    cluster_authorization_failed = 31, False
    """Cluster authorization failed."""
    invalid_timestamp = 32, False
    """The timestamp of the message is out of acceptable range."""
    unsupported_sasl_mechanism = 33, False
    """The broker does not support the requested SASL mechanism."""
    illegal_sasl_state = 34, False
    """Request is not valid given the current SASL state."""
    unsupported_version = 35, False
    """The version of API is not supported."""
    topic_already_exists = 36, False
    """Topic with this name already exists."""
    invalid_partitions = 37, False
    """Number of partitions is below 1."""
    invalid_replication_factor = 38, False
    """Replication factor is below 1 or larger than the number of available brokers."""
    invalid_replica_assignment = 39, False
    """Replica assignment is invalid."""
    invalid_config = 40, False
    """Configuration is invalid."""
    not_controller = 41, True
    """This is not the correct controller for this cluster."""
    invalid_request = 42, False
    """This most likely occurs because of a request being malformed by the client library or the message was sent to an incompatible broker. See the broker logs for more details."""
    unsupported_for_message_format = 43, False
    """The message format version on the broker does not support the request."""
    policy_violation = 44, False
    """Request parameters do not satisfy the configured policy."""
    out_of_order_sequence_number = 45, False
    """The broker received an out of order sequence number."""
    duplicate_sequence_number = 46, False
    """The broker received a duplicate sequence number."""
    invalid_producer_epoch = 47, False
    """Producer attempted to produce with an old epoch."""
    invalid_txn_state = 48, False
    """The producer attempted a transactional operation in an invalid state."""
    invalid_producer_id_mapping = 49, False
    """The producer attempted to use a producer id which is not currently assigned to its transactional id."""
    invalid_transaction_timeout = 50, False
    """The transaction timeout is larger than the maximum value allowed by the broker (as configured by transaction.max.timeout.ms)."""
    concurrent_transactions = 51, True
    """The producer attempted to update a transaction while another concurrent operation on the same transaction was ongoing."""
    transaction_coordinator_fenced = 52, False
    """Indicates that the transaction coordinator sending a WriteTxnMarker is no longer the current coordinator for a given producer."""
    transactional_id_authorization_failed = 53, False
    """Transactional Id authorization failed."""
    security_disabled = 54, False
    """Security features are disabled."""
    operation_not_attempted = 55, False
    """The broker did not attempt to execute this operation. This may happen for batched RPCs where some operations in the batch failed, causing the broker to respond without trying the rest."""
    kafka_storage_error = 56, True
    """Disk error when trying to access log file on the disk."""
    log_dir_not_found = 57, False
    """The user-specified log directory is not found in the broker config."""
    sasl_authentication_failed = 58, False
    """SASL Authentication failed."""
    unknown_producer_id = 59, False
    """This exception is raised by the broker if it could not locate the producer metadata associated with the producerId in question. This could happen if, for instance, the producer's records were deleted because their retention time had elapsed. Once the last records of the producerId are removed, the producer's metadata is removed from the broker, and future appends by the producer will return this exception."""
    reassignment_in_progress = 60, False
    """A partition reassignment is in progress."""
    delegation_token_auth_disabled = 61, False
    """Delegation Token feature is not enabled."""
    delegation_token_not_found = 62, False
    """Delegation Token is not found on server."""
    delegation_token_owner_mismatch = 63, False
    """Specified Principal is not valid Owner/Renewer."""
    delegation_token_request_not_allowed = 64, False
    """Delegation Token requests are not allowed on PLAINTEXT/1-way SSL channels and on delegation token authenticated channels."""
    delegation_token_authorization_failed = 65, False
    """Delegation Token authorization failed."""
    delegation_token_expired = 66, False
    """Delegation Token is expired."""
    invalid_principal_type = 67, False
    """Supplied principalType is not supported."""
    non_empty_group = 68, False
    """The group is not empty."""
    group_id_not_found = 69, False
    """The group id does not exist."""
    fetch_session_id_not_found = 70, True
    """The fetch session ID was not found."""
    invalid_fetch_session_epoch = 71, True
    """The fetch session epoch is invalid."""
    listener_not_found = 72, True
    """There is no listener on the leader broker that matches the listener on which metadata request was processed."""
    topic_deletion_disabled = 73, False
    """Topic deletion is disabled."""
    fenced_leader_epoch = 74, True
    """The leader epoch in the request is older than the epoch on the broker."""
    unknown_leader_epoch = 75, True
    """The leader epoch in the request is newer than the epoch on the broker."""
    unsupported_compression_type = 76, False
    """The requesting client does not support the compression type of given partition."""
    stale_broker_epoch = 77, False
    """Broker epoch has changed."""
    offset_not_available = 78, True
    """The leader high watermark has not caught up from a recent leader election so the offsets cannot be guaranteed to be monotonically increasing."""
    member_id_required = 79, False
    """The group member needs to have a valid member id before actually entering a consumer group."""
    preferred_leader_not_available = 80, True
    """The preferred leader was not available."""
    group_max_size_reached = 81, False
    """The consumer group has reached its max size."""
    fenced_instance_id = 82, False
    """The broker rejected this static consumer since another consumer with the same group.instance.id has registered with a different member.id."""
    eligible_leaders_not_available = 83, True
    """Eligible topic partition leaders are not available."""
    election_not_needed = 84, True
    """Leader election not needed for topic partition."""
    no_reassignment_in_progress = 85, False
    """No partition reassignment is in progress."""
    group_subscribed_to_topic = 86, False
    """Deleting offsets of a topic is forbidden while the consumer group is actively subscribed to it."""
    invalid_record = 87, False
    """This record has failed the validation on broker and hence will be rejected."""
    unstable_offset_commit = 88, True
    """There are unstable offsets that need to be cleared."""
    throttling_quota_exceeded = 89, True
    """The throttling quota has been exceeded."""
    producer_fenced = 90, False
    """There is a newer producer with the same transactionalId which fences the current one."""
    resource_not_found = 91, False
    """A request illegally referred to a resource that does not exist."""
    duplicate_resource = 92, False
    """A request illegally referred to the same resource twice."""
    unacceptable_credential = 93, False
    """Requested credential would not meet criteria for acceptability."""
    inconsistent_voter_set = 94, False
    """Indicates that the either the sender or recipient of a voter-only request is not one of the expected voters"""
    invalid_update_version = 95, False
    """The given update version was invalid."""
    feature_update_failed = 96, False
    """Unable to update finalized features due to an unexpected server error."""
    principal_deserialization_failure = 97, False
    """Request principal deserialization failed during forwarding. This indicates an internal error on the broker cluster security setup."""
    snapshot_not_found = 98, False
    """Requested snapshot was not found"""
    position_out_of_range = 99, False
    """Requested position is not greater than or equal to zero, and less than the size of the snapshot."""
    unknown_topic_id = 100, True
    """This server does not host this topic ID."""
    duplicate_broker_registration = 101, False
    """This broker ID is already in use."""
    broker_id_not_registered = 102, False
    """The given broker ID was not registered."""
    inconsistent_topic_id = 103, True
    """The log's topic ID did not match the topic ID in the request"""
    inconsistent_cluster_id = 104, False
    """The clusterId in the request does not match that found on the server"""
    transactional_id_not_found = 105, False
    """The transactionalId could not be found"""
    fetch_session_topic_id_error = 106, True
    """The fetch session encountered inconsistent topic ID usage"""
    ineligible_replica = 107, False
    """The new ISR contains at least one ineligible replica."""
    new_leader_elected = 108, False
    """The AlterPartition request successfully updated the partition state but the leader has changed."""
    offset_moved_to_tiered_storage = 109, False
    """The requested offset is moved to tiered storage."""
    fenced_member_epoch = 110, False
    """The member epoch is fenced by the group coordinator. The member must abandon all its partitions and rejoin."""
    unreleased_instance_id = 111, False
    """The instance ID is still used by another member in the consumer group. That member must leave first."""
    unsupported_assignor = 112, False
    """The assignor or its version range is not supported by the consumer group."""
    stale_member_epoch = 113, False
    """The member epoch is stale. The member must retry after receiving its updated member epoch via the ConsumerGroupHeartbeat API."""
    mismatched_endpoint_type = 114, False
    """The request was sent to an endpoint of the wrong type."""
    unsupported_endpoint_type = 115, False
    """This endpoint type is not supported yet."""
    unknown_controller_id = 116, False
    """This controller ID is not known."""
    unknown_subscription_id = 117, False
    """Client sent a push telemetry request with an invalid or outdated subscription ID."""
    telemetry_too_large = 118, False
    """Client sent a push telemetry request larger than the maximum size the broker will accept."""
    invalid_registration = 119, False
    """The controller has considered the broker registration to be invalid."""
