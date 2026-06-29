"""Memory benchmark for parsing Kafka metadata responses.

Usage
-----
Normal RSS working-set measurement:
    PYTHONPATH=src python benchmarks/parsing_memory.py

Full native allocation tracking (requires memray):
    PYTHONPATH=src python benchmarks/parsing_memory.py --memray
    python -m memray stats /tmp/kio-memray.bin
    python -m memray flamegraph /tmp/kio-memray.bin  # opens HTML report
"""

from __future__ import annotations

import argparse
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


def measure_working_set(loops: int) -> tuple[float, float]:
    """Parse and *retain* all results so their memory is live at peak measurement.

    Baseline RSS is sampled after a gc.collect() and before any allocations.
    Peak RSS is sampled after the loop while all parsed objects are still alive.
    The results list is then deleted to confirm the OS returns pages.

    Returns:
        Tuple of (elapsed_seconds, peak_rss_delta_mb)
    """
    process = psutil.Process(os.getpid())

    gc.collect()
    rss_before = process.memory_info().rss

    results: list[object] = []
    t0 = time.perf_counter()

    for _ in range(loops):
        offset = 0
        obj, size = read_metadata_response(buffer, offset)
        results.append(obj)
        offset += size
        obj, size = read_metadata_response(buffer, offset)
        results.append(obj)
        offset += size
        obj, size = read_metadata_response(buffer, offset)
        results.append(obj)
        offset += size
        obj, size = read_metadata_response(buffer, offset)
        results.append(obj)
        offset += size
        obj, size = read_metadata_response(buffer, offset)
        results.append(obj)

    elapsed = time.perf_counter() - t0

    # All parsed objects are alive here — this is the true peak.
    peak_rss = process.memory_info().rss

    del results
    gc.collect()

    peak_delta_mb = (peak_rss - rss_before) / (1024 * 1024)
    return elapsed, peak_delta_mb


def measure_memory(loop_counts: list[int]) -> None:
    """Measure peak RSS working-set across different workload sizes."""
    print(f"Buffer size: {len(buffer) / 1024:.2f} KB")
    print("Metadata: 100 topics × 12 partitions\n")
    print("Loop Count | Peak RSS (MB) | Per-Loop (KB) | Elapsed (ms)")
    print("-" * 60)

    for loops in loop_counts:
        elapsed, peak_delta = measure_working_set(loops)
        per_loop_kb = peak_delta * 1024 / loops if loops > 0 else 0
        print(
            f"{loops:>10} | {peak_delta:>13.2f} | {per_loop_kb:>13.2f} | {elapsed * 1000:>12.2f}"
        )


def measure_memory_with_memray(loop_counts: list[int], output: str) -> None:
    """Same measurement wrapped with memray for full native allocation tracking."""
    import memray

    print(f"Buffer size: {len(buffer) / 1024:.2f} KB")
    print("Metadata: 100 topics × 12 partitions")
    print(f"Writing memray profile to: {output}\n")
    print("Loop Count | Peak RSS (MB) | Per-Loop (KB) | Elapsed (ms)")
    print("-" * 60)

    import pathlib

    for loops in loop_counts:
        pathlib.Path(output).unlink(missing_ok=True)
        with memray.Tracker(output, native_traces=True):
            elapsed, peak_delta = measure_working_set(loops)
        per_loop_kb = peak_delta * 1024 / loops if loops > 0 else 0
        print(
            f"{loops:>10} | {peak_delta:>13.2f} | {per_loop_kb:>13.2f} | {elapsed * 1000:>12.2f}"
        )

    print(f"\nProfile written to {output}")
    print(f"  Stats:     python -m memray stats {output}")
    print(f"  Flamegraph: python -m memray flamegraph {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--memray",
        action="store_true",
        help="Wrap measurement with memray for full native allocation tracking.",
    )
    parser.add_argument(
        "--memray-output",
        default="/tmp/kio-memray.bin",
        metavar="PATH",
        help="Output path for the memray profile (default: /tmp/kio-memray.bin).",
    )
    args = parser.parse_args()

    loop_counts = [1000]

    if args.memray:
        measure_memory_with_memray(loop_counts, args.memray_output)
    else:
        measure_memory(loop_counts)
