"""Memory benchmark for parsing Kafka metadata responses."""

from __future__ import annotations

import datetime
import gc
import io
import os
import time
import uuid

from dataclasses import replace

import psutil

from kio.schema.errors import ErrorCode
from kio.schema.metadata.v12 import MetadataResponse
from kio.schema.metadata.v12.response import MetadataResponseBroker
from kio.schema.metadata.v12.response import MetadataResponsePartition
from kio.schema.metadata.v12.response import MetadataResponseTopic
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta

write_metadata_response = entity_writer(MetadataResponse)
read_metadata_response = entity_reader(MetadataResponse)

# Create metadata response with 100 topics, 12 partitions each
instance = MetadataResponse(
    throttle_time=i32Timedelta.parse(datetime.timedelta(milliseconds=123)),
    brokers=tuple(
        MetadataResponseBroker(
            node_id=BrokerId(n),
            host="foo.bar",
            port=i32(1234),
            rack=None,
        )
        for n in range(20)
    ),
    cluster_id="556",
    controller_id=BrokerId(3),
    topics=tuple(
        MetadataResponseTopic(
            error_code=ErrorCode.kafka_storage_error,
            name=TopicName(f"topic-{topic_n}"),
            topic_id=uuid.uuid4(),
            is_internal=False,
            partitions=tuple(
                MetadataResponsePartition(
                    error_code=ErrorCode.delegation_token_expired,
                    partition_index=i32(partition_n),
                    leader_id=BrokerId(2345),
                    leader_epoch=i32(6445678),
                    replica_nodes=(BrokerId(12345), BrokerId(7651)),
                    isr_nodes=(),
                    offline_replicas=(),
                )
                for partition_n in range(12)
            ),
            topic_authorized_operations=i32(765443),
        )
        for topic_n in range(100)
    ),
)

# Serialize once and reuse buffer
with io.BytesIO() as buffer:
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1001)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1002)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1003)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1004)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1005)))
    buffer = buffer.getvalue()


def parse_messages(loops: int) -> tuple[float, float]:
    """Parse metadata messages and track peak memory during execution.

    Returns:
        Tuple of (elapsed_time, peak_rss_delta_mb)
    """
    process = psutil.Process(os.getpid())
    rss_start = process.memory_info().rss / (1024 * 1024)
    peak_rss = rss_start

    t0 = time.perf_counter()

    for _ in range(loops):
        offset = 0
        _, size = read_metadata_response(buffer, offset)
        offset += size
        _, size = read_metadata_response(buffer, offset)
        offset += size
        _, size = read_metadata_response(buffer, offset)
        offset += size
        _, size = read_metadata_response(buffer, offset)
        offset += size
        _, size = read_metadata_response(buffer, offset)
        offset += size

        # Track peak during loop
        current_rss = process.memory_info().rss / (1024 * 1024)
        peak_rss = max(peak_rss, current_rss)

    elapsed = time.perf_counter() - t0
    peak_delta = peak_rss - rss_start

    return elapsed, peak_delta


def measure_memory(loop_counts: list[int]) -> None:
    """Measure peak RSS memory consumption across different workload sizes."""
    print(f"Buffer size: {len(buffer) / 1024:.2f} KB")
    print(f"Metadata: 100 topics × 12 partitions\n")
    print("Loop Count | Peak RSS (MB) | Per-Loop (KB) | Elapsed (ms)")
    print("-" * 60)

    for loops in loop_counts:
        # Warm up
        parse_messages(100)

        # Force garbage collection
        gc.collect()

        # Measure peak memory during execution
        elapsed, peak_delta = parse_messages(loops)
        per_loop = peak_delta * 1_000_000 / loops if loops > 0 else 0
        print(
            f"{loops:>10} | {peak_delta:>13.2f} | {per_loop:>13.2f} | {elapsed*1000:>12.2f}"
        )


if __name__ == "__main__":
    # Test with different loop counts to check for linear memory growth
    loop_counts = [1000]
    measure_memory(loop_counts)
