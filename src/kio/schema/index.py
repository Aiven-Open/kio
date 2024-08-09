from collections.abc import Mapping
from types import MappingProxyType
from typing import Final
from typing import Literal
from typing import TypeAlias

from kio.static.constants import EntityType

__all__ = (
    "api_key_map",
    "schema_name_map",
    "PayloadEntityType",
    "LoadableEntityType",
)

PayloadEntityType: TypeAlias = Literal[EntityType.response, EntityType.request]
LoadableEntityType: TypeAlias = (
    Literal[EntityType.header, EntityType.data] | PayloadEntityType
)
TypeMap: TypeAlias = Mapping[LoadableEntityType, str]
VersionMap: TypeAlias = Mapping[int, TypeMap]
SchemaNameMap: TypeAlias = Mapping[str, VersionMap]
APIKeyMap: TypeAlias = Mapping[int, str]


api_key_map: Final[APIKeyMap] = MappingProxyType(
    {
        0: "produce",
        1: "fetch",
        2: "list_offsets",
        3: "metadata",
        4: "leader_and_isr",
        5: "stop_replica",
        6: "update_metadata",
        7: "controlled_shutdown",
        8: "offset_commit",
        9: "offset_fetch",
        10: "find_coordinator",
        11: "join_group",
        12: "heartbeat",
        13: "leave_group",
        14: "sync_group",
        15: "describe_groups",
        16: "list_groups",
        17: "sasl_handshake",
        18: "api_versions",
        19: "create_topics",
        20: "delete_topics",
        21: "delete_records",
        22: "init_producer_id",
        23: "offset_for_leader_epoch",
        24: "add_partitions_to_txn",
        25: "add_offsets_to_txn",
        26: "end_txn",
        27: "write_txn_markers",
        28: "txn_offset_commit",
        29: "describe_acls",
        30: "create_acls",
        31: "delete_acls",
        32: "describe_configs",
        33: "alter_configs",
        34: "alter_replica_log_dirs",
        35: "describe_log_dirs",
        36: "sasl_authenticate",
        37: "create_partitions",
        38: "create_delegation_token",
        39: "renew_delegation_token",
        40: "expire_delegation_token",
        41: "describe_delegation_token",
        42: "delete_groups",
        43: "elect_leaders",
        44: "incremental_alter_configs",
        45: "alter_partition_reassignments",
        46: "list_partition_reassignments",
        47: "offset_delete",
        48: "describe_client_quotas",
        49: "alter_client_quotas",
        50: "describe_user_scram_credentials",
        51: "alter_user_scram_credentials",
        52: "vote",
        53: "begin_quorum_epoch",
        54: "end_quorum_epoch",
        55: "describe_quorum",
        56: "alter_partition",
        57: "update_features",
        58: "envelope",
        59: "fetch_snapshot",
        60: "describe_cluster",
        61: "describe_producers",
        62: "broker_registration",
        63: "broker_heartbeat",
        64: "unregister_broker",
        65: "describe_transactions",
        66: "list_transactions",
        67: "allocate_producer_ids",
        68: "consumer_group_heartbeat",
        69: "consumer_group_describe",
        70: "controller_registration",
        71: "get_telemetry_subscriptions",
        72: "push_telemetry",
        73: "assign_replicas_to_dirs",
        74: "list_client_metrics_resources",
    }
)

schema_name_map: Final[SchemaNameMap] = MappingProxyType(
    {
        "add_offsets_to_txn": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_offsets_to_txn.v0.request:AddOffsetsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_offsets_to_txn.v0.response:AddOffsetsToTxnResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_offsets_to_txn.v1.request:AddOffsetsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_offsets_to_txn.v1.response:AddOffsetsToTxnResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_offsets_to_txn.v2.request:AddOffsetsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_offsets_to_txn.v2.response:AddOffsetsToTxnResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_offsets_to_txn.v3.request:AddOffsetsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_offsets_to_txn.v3.response:AddOffsetsToTxnResponse"
                        ),
                    }
                ),
            }
        ),
        "add_partitions_to_txn": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_partitions_to_txn.v0.request:AddPartitionsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_partitions_to_txn.v0.response:AddPartitionsToTxnResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_partitions_to_txn.v1.request:AddPartitionsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_partitions_to_txn.v1.response:AddPartitionsToTxnResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_partitions_to_txn.v2.request:AddPartitionsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_partitions_to_txn.v2.response:AddPartitionsToTxnResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_partitions_to_txn.v3.request:AddPartitionsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_partitions_to_txn.v3.response:AddPartitionsToTxnResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.add_partitions_to_txn.v4.request:AddPartitionsToTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.add_partitions_to_txn.v4.response:AddPartitionsToTxnResponse"
                        ),
                    }
                ),
            }
        ),
        "allocate_producer_ids": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.allocate_producer_ids.v0.request:AllocateProducerIdsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.allocate_producer_ids.v0.response:AllocateProducerIdsResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_client_quotas": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_client_quotas.v0.request:AlterClientQuotasRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_client_quotas.v0.response:AlterClientQuotasResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_client_quotas.v1.request:AlterClientQuotasRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_client_quotas.v1.response:AlterClientQuotasResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_configs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_configs.v0.request:AlterConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_configs.v0.response:AlterConfigsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_configs.v1.request:AlterConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_configs.v1.response:AlterConfigsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_configs.v2.request:AlterConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_configs.v2.response:AlterConfigsResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_partition": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_partition.v0.request:AlterPartitionRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_partition.v0.response:AlterPartitionResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_partition.v1.request:AlterPartitionRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_partition.v1.response:AlterPartitionResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_partition.v2.request:AlterPartitionRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_partition.v2.response:AlterPartitionResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_partition.v3.request:AlterPartitionRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_partition.v3.response:AlterPartitionResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_partition_reassignments": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_partition_reassignments.v0.request:AlterPartitionReassignmentsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_partition_reassignments.v0.response:AlterPartitionReassignmentsResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_replica_log_dirs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_replica_log_dirs.v0.request:AlterReplicaLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_replica_log_dirs.v0.response:AlterReplicaLogDirsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_replica_log_dirs.v1.request:AlterReplicaLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_replica_log_dirs.v1.response:AlterReplicaLogDirsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_replica_log_dirs.v2.request:AlterReplicaLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_replica_log_dirs.v2.response:AlterReplicaLogDirsResponse"
                        ),
                    }
                ),
            }
        ),
        "alter_user_scram_credentials": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.alter_user_scram_credentials.v0.request:AlterUserScramCredentialsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.alter_user_scram_credentials.v0.response:AlterUserScramCredentialsResponse"
                        ),
                    }
                ),
            }
        ),
        "api_versions": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.api_versions.v0.request:ApiVersionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.api_versions.v0.response:ApiVersionsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.api_versions.v1.request:ApiVersionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.api_versions.v1.response:ApiVersionsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.api_versions.v2.request:ApiVersionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.api_versions.v2.response:ApiVersionsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.api_versions.v3.request:ApiVersionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.api_versions.v3.response:ApiVersionsResponse"
                        ),
                    }
                ),
            }
        ),
        "assign_replicas_to_dirs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.assign_replicas_to_dirs.v0.request:AssignReplicasToDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.assign_replicas_to_dirs.v0.response:AssignReplicasToDirsResponse"
                        ),
                    }
                ),
            }
        ),
        "begin_quorum_epoch": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.begin_quorum_epoch.v0.request:BeginQuorumEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.begin_quorum_epoch.v0.response:BeginQuorumEpochResponse"
                        ),
                    }
                ),
            }
        ),
        "broker_heartbeat": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_heartbeat.v0.request:BrokerHeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_heartbeat.v0.response:BrokerHeartbeatResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_heartbeat.v1.request:BrokerHeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_heartbeat.v1.response:BrokerHeartbeatResponse"
                        ),
                    }
                ),
            }
        ),
        "broker_registration": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_registration.v0.request:BrokerRegistrationRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_registration.v0.response:BrokerRegistrationResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_registration.v1.request:BrokerRegistrationRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_registration.v1.response:BrokerRegistrationResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_registration.v2.request:BrokerRegistrationRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_registration.v2.response:BrokerRegistrationResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.broker_registration.v3.request:BrokerRegistrationRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.broker_registration.v3.response:BrokerRegistrationResponse"
                        ),
                    }
                ),
            }
        ),
        "consumer_group_describe": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.consumer_group_describe.v0.request:ConsumerGroupDescribeRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.consumer_group_describe.v0.response:ConsumerGroupDescribeResponse"
                        ),
                    }
                ),
            }
        ),
        "consumer_group_heartbeat": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.consumer_group_heartbeat.v0.request:ConsumerGroupHeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.consumer_group_heartbeat.v0.response:ConsumerGroupHeartbeatResponse"
                        ),
                    }
                ),
            }
        ),
        "consumer_protocol_assignment": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_assignment.v0.data:ConsumerProtocolAssignment"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_assignment.v1.data:ConsumerProtocolAssignment"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_assignment.v2.data:ConsumerProtocolAssignment"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_assignment.v3.data:ConsumerProtocolAssignment"
                        ),
                    }
                ),
            }
        ),
        "consumer_protocol_subscription": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_subscription.v0.data:ConsumerProtocolSubscription"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_subscription.v1.data:ConsumerProtocolSubscription"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_subscription.v2.data:ConsumerProtocolSubscription"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.consumer_protocol_subscription.v3.data:ConsumerProtocolSubscription"
                        ),
                    }
                ),
            }
        ),
        "controlled_shutdown": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.controlled_shutdown.v0.request:ControlledShutdownRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.controlled_shutdown.v0.response:ControlledShutdownResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.controlled_shutdown.v1.request:ControlledShutdownRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.controlled_shutdown.v1.response:ControlledShutdownResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.controlled_shutdown.v2.request:ControlledShutdownRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.controlled_shutdown.v2.response:ControlledShutdownResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.controlled_shutdown.v3.request:ControlledShutdownRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.controlled_shutdown.v3.response:ControlledShutdownResponse"
                        ),
                    }
                ),
            }
        ),
        "controller_registration": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.controller_registration.v0.request:ControllerRegistrationRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.controller_registration.v0.response:ControllerRegistrationResponse"
                        ),
                    }
                ),
            }
        ),
        "create_acls": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_acls.v0.request:CreateAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_acls.v0.response:CreateAclsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_acls.v1.request:CreateAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_acls.v1.response:CreateAclsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_acls.v2.request:CreateAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_acls.v2.response:CreateAclsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_acls.v3.request:CreateAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_acls.v3.response:CreateAclsResponse"
                        ),
                    }
                ),
            }
        ),
        "create_delegation_token": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_delegation_token.v0.request:CreateDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_delegation_token.v0.response:CreateDelegationTokenResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_delegation_token.v1.request:CreateDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_delegation_token.v1.response:CreateDelegationTokenResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_delegation_token.v2.request:CreateDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_delegation_token.v2.response:CreateDelegationTokenResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_delegation_token.v3.request:CreateDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_delegation_token.v3.response:CreateDelegationTokenResponse"
                        ),
                    }
                ),
            }
        ),
        "create_partitions": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_partitions.v0.request:CreatePartitionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_partitions.v0.response:CreatePartitionsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_partitions.v1.request:CreatePartitionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_partitions.v1.response:CreatePartitionsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_partitions.v2.request:CreatePartitionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_partitions.v2.response:CreatePartitionsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_partitions.v3.request:CreatePartitionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_partitions.v3.response:CreatePartitionsResponse"
                        ),
                    }
                ),
            }
        ),
        "create_topics": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v0.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v0.response:CreateTopicsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v1.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v1.response:CreateTopicsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v2.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v2.response:CreateTopicsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v3.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v3.response:CreateTopicsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v4.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v4.response:CreateTopicsResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v5.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v5.response:CreateTopicsResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v6.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v6.response:CreateTopicsResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.create_topics.v7.request:CreateTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.create_topics.v7.response:CreateTopicsResponse"
                        ),
                    }
                ),
            }
        ),
        "default_principal_data": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.default_principal_data.v0.data:DefaultPrincipalData"
                        ),
                    }
                ),
            }
        ),
        "delete_acls": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_acls.v0.request:DeleteAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_acls.v0.response:DeleteAclsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_acls.v1.request:DeleteAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_acls.v1.response:DeleteAclsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_acls.v2.request:DeleteAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_acls.v2.response:DeleteAclsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_acls.v3.request:DeleteAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_acls.v3.response:DeleteAclsResponse"
                        ),
                    }
                ),
            }
        ),
        "delete_groups": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_groups.v0.request:DeleteGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_groups.v0.response:DeleteGroupsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_groups.v1.request:DeleteGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_groups.v1.response:DeleteGroupsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_groups.v2.request:DeleteGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_groups.v2.response:DeleteGroupsResponse"
                        ),
                    }
                ),
            }
        ),
        "delete_records": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_records.v0.request:DeleteRecordsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_records.v0.response:DeleteRecordsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_records.v1.request:DeleteRecordsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_records.v1.response:DeleteRecordsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_records.v2.request:DeleteRecordsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_records.v2.response:DeleteRecordsResponse"
                        ),
                    }
                ),
            }
        ),
        "delete_topics": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v0.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v0.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v1.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v1.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v2.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v2.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v3.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v3.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v4.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v4.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v5.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v5.response:DeleteTopicsResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.delete_topics.v6.request:DeleteTopicsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.delete_topics.v6.response:DeleteTopicsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_acls": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_acls.v0.request:DescribeAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_acls.v0.response:DescribeAclsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_acls.v1.request:DescribeAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_acls.v1.response:DescribeAclsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_acls.v2.request:DescribeAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_acls.v2.response:DescribeAclsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_acls.v3.request:DescribeAclsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_acls.v3.response:DescribeAclsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_client_quotas": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_client_quotas.v0.request:DescribeClientQuotasRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_client_quotas.v0.response:DescribeClientQuotasResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_client_quotas.v1.request:DescribeClientQuotasRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_client_quotas.v1.response:DescribeClientQuotasResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_cluster": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_cluster.v0.request:DescribeClusterRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_cluster.v0.response:DescribeClusterResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_cluster.v1.request:DescribeClusterRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_cluster.v1.response:DescribeClusterResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_configs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_configs.v0.request:DescribeConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_configs.v0.response:DescribeConfigsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_configs.v1.request:DescribeConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_configs.v1.response:DescribeConfigsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_configs.v2.request:DescribeConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_configs.v2.response:DescribeConfigsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_configs.v3.request:DescribeConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_configs.v3.response:DescribeConfigsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_configs.v4.request:DescribeConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_configs.v4.response:DescribeConfigsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_delegation_token": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_delegation_token.v0.request:DescribeDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_delegation_token.v0.response:DescribeDelegationTokenResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_delegation_token.v1.request:DescribeDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_delegation_token.v1.response:DescribeDelegationTokenResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_delegation_token.v2.request:DescribeDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_delegation_token.v2.response:DescribeDelegationTokenResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_delegation_token.v3.request:DescribeDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_delegation_token.v3.response:DescribeDelegationTokenResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_groups": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v0.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v0.response:DescribeGroupsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v1.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v1.response:DescribeGroupsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v2.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v2.response:DescribeGroupsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v3.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v3.response:DescribeGroupsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v4.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v4.response:DescribeGroupsResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_groups.v5.request:DescribeGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_groups.v5.response:DescribeGroupsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_log_dirs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_log_dirs.v0.request:DescribeLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_log_dirs.v0.response:DescribeLogDirsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_log_dirs.v1.request:DescribeLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_log_dirs.v1.response:DescribeLogDirsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_log_dirs.v2.request:DescribeLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_log_dirs.v2.response:DescribeLogDirsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_log_dirs.v3.request:DescribeLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_log_dirs.v3.response:DescribeLogDirsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_log_dirs.v4.request:DescribeLogDirsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_log_dirs.v4.response:DescribeLogDirsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_producers": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_producers.v0.request:DescribeProducersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_producers.v0.response:DescribeProducersResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_quorum": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_quorum.v0.request:DescribeQuorumRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_quorum.v0.response:DescribeQuorumResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_quorum.v1.request:DescribeQuorumRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_quorum.v1.response:DescribeQuorumResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_transactions": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_transactions.v0.request:DescribeTransactionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_transactions.v0.response:DescribeTransactionsResponse"
                        ),
                    }
                ),
            }
        ),
        "describe_user_scram_credentials": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.describe_user_scram_credentials.v0.request:DescribeUserScramCredentialsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.describe_user_scram_credentials.v0.response:DescribeUserScramCredentialsResponse"
                        ),
                    }
                ),
            }
        ),
        "elect_leaders": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.elect_leaders.v0.request:ElectLeadersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.elect_leaders.v0.response:ElectLeadersResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.elect_leaders.v1.request:ElectLeadersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.elect_leaders.v1.response:ElectLeadersResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.elect_leaders.v2.request:ElectLeadersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.elect_leaders.v2.response:ElectLeadersResponse"
                        ),
                    }
                ),
            }
        ),
        "end_quorum_epoch": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.end_quorum_epoch.v0.request:EndQuorumEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.end_quorum_epoch.v0.response:EndQuorumEpochResponse"
                        ),
                    }
                ),
            }
        ),
        "end_txn": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.end_txn.v0.request:EndTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.end_txn.v0.response:EndTxnResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.end_txn.v1.request:EndTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.end_txn.v1.response:EndTxnResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.end_txn.v2.request:EndTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.end_txn.v2.response:EndTxnResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.end_txn.v3.request:EndTxnRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.end_txn.v3.response:EndTxnResponse"
                        ),
                    }
                ),
            }
        ),
        "envelope": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.envelope.v0.request:EnvelopeRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.envelope.v0.response:EnvelopeResponse"
                        ),
                    }
                ),
            }
        ),
        "expire_delegation_token": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.expire_delegation_token.v0.request:ExpireDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.expire_delegation_token.v0.response:ExpireDelegationTokenResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.expire_delegation_token.v1.request:ExpireDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.expire_delegation_token.v1.response:ExpireDelegationTokenResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.expire_delegation_token.v2.request:ExpireDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.expire_delegation_token.v2.response:ExpireDelegationTokenResponse"
                        ),
                    }
                ),
            }
        ),
        "fetch": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v0.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v0.response:FetchResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v1.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v1.response:FetchResponse"
                        ),
                    }
                ),
                10: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v10.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v10.response:FetchResponse"
                        ),
                    }
                ),
                11: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v11.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v11.response:FetchResponse"
                        ),
                    }
                ),
                12: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v12.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v12.response:FetchResponse"
                        ),
                    }
                ),
                13: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v13.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v13.response:FetchResponse"
                        ),
                    }
                ),
                14: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v14.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v14.response:FetchResponse"
                        ),
                    }
                ),
                15: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v15.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v15.response:FetchResponse"
                        ),
                    }
                ),
                16: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v16.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v16.response:FetchResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v2.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v2.response:FetchResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v3.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v3.response:FetchResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v4.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v4.response:FetchResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v5.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v5.response:FetchResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v6.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v6.response:FetchResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v7.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v7.response:FetchResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v8.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v8.response:FetchResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch.v9.request:FetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch.v9.response:FetchResponse"
                        ),
                    }
                ),
            }
        ),
        "fetch_snapshot": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.fetch_snapshot.v0.request:FetchSnapshotRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.fetch_snapshot.v0.response:FetchSnapshotResponse"
                        ),
                    }
                ),
            }
        ),
        "find_coordinator": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.find_coordinator.v0.request:FindCoordinatorRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.find_coordinator.v0.response:FindCoordinatorResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.find_coordinator.v1.request:FindCoordinatorRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.find_coordinator.v1.response:FindCoordinatorResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.find_coordinator.v2.request:FindCoordinatorRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.find_coordinator.v2.response:FindCoordinatorResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.find_coordinator.v3.request:FindCoordinatorRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.find_coordinator.v3.response:FindCoordinatorResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.find_coordinator.v4.request:FindCoordinatorRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.find_coordinator.v4.response:FindCoordinatorResponse"
                        ),
                    }
                ),
            }
        ),
        "get_telemetry_subscriptions": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.get_telemetry_subscriptions.v0.request:GetTelemetrySubscriptionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.get_telemetry_subscriptions.v0.response:GetTelemetrySubscriptionsResponse"
                        ),
                    }
                ),
            }
        ),
        "heartbeat": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.heartbeat.v0.request:HeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.heartbeat.v0.response:HeartbeatResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.heartbeat.v1.request:HeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.heartbeat.v1.response:HeartbeatResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.heartbeat.v2.request:HeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.heartbeat.v2.response:HeartbeatResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.heartbeat.v3.request:HeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.heartbeat.v3.response:HeartbeatResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.heartbeat.v4.request:HeartbeatRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.heartbeat.v4.response:HeartbeatResponse"
                        ),
                    }
                ),
            }
        ),
        "incremental_alter_configs": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.incremental_alter_configs.v0.request:IncrementalAlterConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.incremental_alter_configs.v0.response:IncrementalAlterConfigsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.incremental_alter_configs.v1.request:IncrementalAlterConfigsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.incremental_alter_configs.v1.response:IncrementalAlterConfigsResponse"
                        ),
                    }
                ),
            }
        ),
        "init_producer_id": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.init_producer_id.v0.request:InitProducerIdRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.init_producer_id.v0.response:InitProducerIdResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.init_producer_id.v1.request:InitProducerIdRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.init_producer_id.v1.response:InitProducerIdResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.init_producer_id.v2.request:InitProducerIdRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.init_producer_id.v2.response:InitProducerIdResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.init_producer_id.v3.request:InitProducerIdRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.init_producer_id.v3.response:InitProducerIdResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.init_producer_id.v4.request:InitProducerIdRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.init_producer_id.v4.response:InitProducerIdResponse"
                        ),
                    }
                ),
            }
        ),
        "join_group": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v0.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v0.response:JoinGroupResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v1.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v1.response:JoinGroupResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v2.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v2.response:JoinGroupResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v3.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v3.response:JoinGroupResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v4.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v4.response:JoinGroupResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v5.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v5.response:JoinGroupResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v6.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v6.response:JoinGroupResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v7.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v7.response:JoinGroupResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v8.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v8.response:JoinGroupResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.join_group.v9.request:JoinGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.join_group.v9.response:JoinGroupResponse"
                        ),
                    }
                ),
            }
        ),
        "leader_and_isr": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v0.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v0.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v1.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v1.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v2.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v2.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v3.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v3.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v4.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v4.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v5.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v5.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v6.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v6.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leader_and_isr.v7.request:LeaderAndIsrRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leader_and_isr.v7.response:LeaderAndIsrResponse"
                        ),
                    }
                ),
            }
        ),
        "leader_change_message": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.leader_change_message.v0.data:LeaderChangeMessage"
                        ),
                    }
                ),
            }
        ),
        "leave_group": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v0.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v0.response:LeaveGroupResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v1.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v1.response:LeaveGroupResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v2.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v2.response:LeaveGroupResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v3.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v3.response:LeaveGroupResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v4.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v4.response:LeaveGroupResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.leave_group.v5.request:LeaveGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.leave_group.v5.response:LeaveGroupResponse"
                        ),
                    }
                ),
            }
        ),
        "list_client_metrics_resources": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_client_metrics_resources.v0.request:ListClientMetricsResourcesRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_client_metrics_resources.v0.response:ListClientMetricsResourcesResponse"
                        ),
                    }
                ),
            }
        ),
        "list_groups": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_groups.v0.request:ListGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_groups.v0.response:ListGroupsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_groups.v1.request:ListGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_groups.v1.response:ListGroupsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_groups.v2.request:ListGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_groups.v2.response:ListGroupsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_groups.v3.request:ListGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_groups.v3.response:ListGroupsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_groups.v4.request:ListGroupsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_groups.v4.response:ListGroupsResponse"
                        ),
                    }
                ),
            }
        ),
        "list_offsets": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v0.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v0.response:ListOffsetsResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v1.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v1.response:ListOffsetsResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v2.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v2.response:ListOffsetsResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v3.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v3.response:ListOffsetsResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v4.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v4.response:ListOffsetsResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v5.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v5.response:ListOffsetsResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v6.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v6.response:ListOffsetsResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v7.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v7.response:ListOffsetsResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_offsets.v8.request:ListOffsetsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_offsets.v8.response:ListOffsetsResponse"
                        ),
                    }
                ),
            }
        ),
        "list_partition_reassignments": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_partition_reassignments.v0.request:ListPartitionReassignmentsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_partition_reassignments.v0.response:ListPartitionReassignmentsResponse"
                        ),
                    }
                ),
            }
        ),
        "list_transactions": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.list_transactions.v0.request:ListTransactionsRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.list_transactions.v0.response:ListTransactionsResponse"
                        ),
                    }
                ),
            }
        ),
        "metadata": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v0.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v0.response:MetadataResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v1.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v1.response:MetadataResponse"
                        ),
                    }
                ),
                10: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v10.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v10.response:MetadataResponse"
                        ),
                    }
                ),
                11: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v11.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v11.response:MetadataResponse"
                        ),
                    }
                ),
                12: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v12.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v12.response:MetadataResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v2.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v2.response:MetadataResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v3.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v3.response:MetadataResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v4.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v4.response:MetadataResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v5.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v5.response:MetadataResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v6.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v6.response:MetadataResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v7.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v7.response:MetadataResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v8.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v8.response:MetadataResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.metadata.v9.request:MetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.metadata.v9.response:MetadataResponse"
                        ),
                    }
                ),
            }
        ),
        "offset_commit": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v0.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v0.response:OffsetCommitResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v1.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v1.response:OffsetCommitResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v2.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v2.response:OffsetCommitResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v3.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v3.response:OffsetCommitResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v4.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v4.response:OffsetCommitResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v5.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v5.response:OffsetCommitResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v6.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v6.response:OffsetCommitResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v7.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v7.response:OffsetCommitResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v8.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v8.response:OffsetCommitResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_commit.v9.request:OffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_commit.v9.response:OffsetCommitResponse"
                        ),
                    }
                ),
            }
        ),
        "offset_delete": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_delete.v0.request:OffsetDeleteRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_delete.v0.response:OffsetDeleteResponse"
                        ),
                    }
                ),
            }
        ),
        "offset_fetch": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v0.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v0.response:OffsetFetchResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v1.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v1.response:OffsetFetchResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v2.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v2.response:OffsetFetchResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v3.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v3.response:OffsetFetchResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v4.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v4.response:OffsetFetchResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v5.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v5.response:OffsetFetchResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v6.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v6.response:OffsetFetchResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v7.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v7.response:OffsetFetchResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v8.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v8.response:OffsetFetchResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_fetch.v9.request:OffsetFetchRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_fetch.v9.response:OffsetFetchResponse"
                        ),
                    }
                ),
            }
        ),
        "offset_for_leader_epoch": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_for_leader_epoch.v0.request:OffsetForLeaderEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_for_leader_epoch.v0.response:OffsetForLeaderEpochResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_for_leader_epoch.v1.request:OffsetForLeaderEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_for_leader_epoch.v1.response:OffsetForLeaderEpochResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_for_leader_epoch.v2.request:OffsetForLeaderEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_for_leader_epoch.v2.response:OffsetForLeaderEpochResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_for_leader_epoch.v3.request:OffsetForLeaderEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_for_leader_epoch.v3.response:OffsetForLeaderEpochResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.offset_for_leader_epoch.v4.request:OffsetForLeaderEpochRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.offset_for_leader_epoch.v4.response:OffsetForLeaderEpochResponse"
                        ),
                    }
                ),
            }
        ),
        "produce": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v0.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v0.response:ProduceResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v1.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v1.response:ProduceResponse"
                        ),
                    }
                ),
                10: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v10.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v10.response:ProduceResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v2.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v2.response:ProduceResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v3.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v3.response:ProduceResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v4.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v4.response:ProduceResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v5.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v5.response:ProduceResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v6.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v6.response:ProduceResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v7.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v7.response:ProduceResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v8.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v8.response:ProduceResponse"
                        ),
                    }
                ),
                9: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.produce.v9.request:ProduceRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.produce.v9.response:ProduceResponse"
                        ),
                    }
                ),
            }
        ),
        "push_telemetry": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.push_telemetry.v0.request:PushTelemetryRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.push_telemetry.v0.response:PushTelemetryResponse"
                        ),
                    }
                ),
            }
        ),
        "renew_delegation_token": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.renew_delegation_token.v0.request:RenewDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.renew_delegation_token.v0.response:RenewDelegationTokenResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.renew_delegation_token.v1.request:RenewDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.renew_delegation_token.v1.response:RenewDelegationTokenResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.renew_delegation_token.v2.request:RenewDelegationTokenRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.renew_delegation_token.v2.response:RenewDelegationTokenResponse"
                        ),
                    }
                ),
            }
        ),
        "request_header": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.header: (
                            "kio.schema.request_header.v0.header:RequestHeader"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.header: (
                            "kio.schema.request_header.v1.header:RequestHeader"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.header: (
                            "kio.schema.request_header.v2.header:RequestHeader"
                        ),
                    }
                ),
            }
        ),
        "response_header": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.header: (
                            "kio.schema.response_header.v0.header:ResponseHeader"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.header: (
                            "kio.schema.response_header.v1.header:ResponseHeader"
                        ),
                    }
                ),
            }
        ),
        "sasl_authenticate": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sasl_authenticate.v0.request:SaslAuthenticateRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sasl_authenticate.v0.response:SaslAuthenticateResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sasl_authenticate.v1.request:SaslAuthenticateRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sasl_authenticate.v1.response:SaslAuthenticateResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sasl_authenticate.v2.request:SaslAuthenticateRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sasl_authenticate.v2.response:SaslAuthenticateResponse"
                        ),
                    }
                ),
            }
        ),
        "sasl_handshake": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sasl_handshake.v0.request:SaslHandshakeRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sasl_handshake.v0.response:SaslHandshakeResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sasl_handshake.v1.request:SaslHandshakeRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sasl_handshake.v1.response:SaslHandshakeResponse"
                        ),
                    }
                ),
            }
        ),
        "snapshot_footer_record": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.snapshot_footer_record.v0.data:SnapshotFooterRecord"
                        ),
                    }
                ),
            }
        ),
        "snapshot_header_record": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.data: (
                            "kio.schema.snapshot_header_record.v0.data:SnapshotHeaderRecord"
                        ),
                    }
                ),
            }
        ),
        "stop_replica": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.stop_replica.v0.request:StopReplicaRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.stop_replica.v0.response:StopReplicaResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.stop_replica.v1.request:StopReplicaRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.stop_replica.v1.response:StopReplicaResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.stop_replica.v2.request:StopReplicaRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.stop_replica.v2.response:StopReplicaResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.stop_replica.v3.request:StopReplicaRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.stop_replica.v3.response:StopReplicaResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.stop_replica.v4.request:StopReplicaRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.stop_replica.v4.response:StopReplicaResponse"
                        ),
                    }
                ),
            }
        ),
        "sync_group": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v0.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v0.response:SyncGroupResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v1.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v1.response:SyncGroupResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v2.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v2.response:SyncGroupResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v3.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v3.response:SyncGroupResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v4.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v4.response:SyncGroupResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.sync_group.v5.request:SyncGroupRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.sync_group.v5.response:SyncGroupResponse"
                        ),
                    }
                ),
            }
        ),
        "txn_offset_commit": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.txn_offset_commit.v0.request:TxnOffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.txn_offset_commit.v0.response:TxnOffsetCommitResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.txn_offset_commit.v1.request:TxnOffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.txn_offset_commit.v1.response:TxnOffsetCommitResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.txn_offset_commit.v2.request:TxnOffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.txn_offset_commit.v2.response:TxnOffsetCommitResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.txn_offset_commit.v3.request:TxnOffsetCommitRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.txn_offset_commit.v3.response:TxnOffsetCommitResponse"
                        ),
                    }
                ),
            }
        ),
        "unregister_broker": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.unregister_broker.v0.request:UnregisterBrokerRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.unregister_broker.v0.response:UnregisterBrokerResponse"
                        ),
                    }
                ),
            }
        ),
        "update_features": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_features.v0.request:UpdateFeaturesRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_features.v0.response:UpdateFeaturesResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_features.v1.request:UpdateFeaturesRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_features.v1.response:UpdateFeaturesResponse"
                        ),
                    }
                ),
            }
        ),
        "update_metadata": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v0.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v0.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v1.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v1.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                2: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v2.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v2.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                3: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v3.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v3.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                4: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v4.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v4.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                5: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v5.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v5.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                6: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v6.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v6.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                7: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v7.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v7.response:UpdateMetadataResponse"
                        ),
                    }
                ),
                8: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.update_metadata.v8.request:UpdateMetadataRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.update_metadata.v8.response:UpdateMetadataResponse"
                        ),
                    }
                ),
            }
        ),
        "vote": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: ("kio.schema.vote.v0.request:VoteRequest"),
                        EntityType.response: (
                            "kio.schema.vote.v0.response:VoteResponse"
                        ),
                    }
                ),
            }
        ),
        "write_txn_markers": MappingProxyType(
            {
                0: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.write_txn_markers.v0.request:WriteTxnMarkersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.write_txn_markers.v0.response:WriteTxnMarkersResponse"
                        ),
                    }
                ),
                1: MappingProxyType(
                    {
                        EntityType.request: (
                            "kio.schema.write_txn_markers.v1.request:WriteTxnMarkersRequest"
                        ),
                        EntityType.response: (
                            "kio.schema.write_txn_markers.v1.response:WriteTxnMarkersResponse"
                        ),
                    }
                ),
            }
        ),
    }
)
