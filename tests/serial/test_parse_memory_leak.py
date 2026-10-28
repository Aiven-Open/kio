from __future__ import annotations

import datetime
import gc
import io
import sys
import uuid

from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import replace
from functools import partial

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


@dataclass(frozen=True, slots=True)
class MemoryStabilityConfig:
    warmup: int
    iterations: int
    sample_every: int = 100
    plateau_mb: float = 2.0
    drift_mb: float = 1.0
    early_window: int = 10
    late_window: int = 10


@dataclass(frozen=True, slots=True)
class MemoryStabilityResult:
    early_mean_mb: float
    late_mean_mb: float
    late_min_mb: float
    late_max_mb: float
    drift_mb: float
    plateau_mb: float


@dataclass(frozen=True, slots=True)
class MetadataParseBuffers:
    single: bytes
    concatenated: bytes


def _make_metadata_parse_buffers() -> MetadataParseBuffers:
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

    with io.BytesIO() as single_buffer:
        write_metadata_response(
            single_buffer,
            replace(instance, controller_id=BrokerId(1001)),
        )
        single = single_buffer.getvalue()

    with io.BytesIO() as concatenated_buffer:
        for controller_id in range(1001, 1006):
            write_metadata_response(
                concatenated_buffer,
                replace(instance, controller_id=BrokerId(controller_id)),
            )
        concatenated = concatenated_buffer.getvalue()

    return MetadataParseBuffers(single=single, concatenated=concatenated)


def _parse_single_message(buffer: bytes) -> None:
    read_metadata_response(buffer, 0)


def _parse_concatenated_messages(buffer: bytes) -> None:
    offset = 0
    for _ in range(5):
        _, size = read_metadata_response(buffer, offset)
        offset += size
    assert offset == len(buffer)


def _sample_memory_mb(process: psutil.Process | None = None) -> float:
    proc = process or psutil.Process()
    gc.collect()
    if sys.platform == "darwin" or "bsd" in sys.platform:
        usage = proc.memory_info().rss
    else:
        usage = proc.memory_full_info().uss
    return float(usage) / (1024 * 1024)


def _measure_memory_stability(
    action: Callable[[], object],
    config: MemoryStabilityConfig,
    *,
    process: psutil.Process | None = None,
) -> MemoryStabilityResult:
    proc = process or psutil.Process()

    for _ in range(config.warmup):
        action()

    samples: list[float] = []
    for iteration in range(config.iterations):
        action()
        if iteration % config.sample_every == 0:
            samples.append(_sample_memory_mb(proc))

    if len(samples) < config.early_window + config.late_window:
        msg = (
            f"Not enough memory samples ({len(samples)}) for windows "
            f"early={config.early_window}, late={config.late_window}"
        )
        raise ValueError(msg)

    early = samples[config.early_window : config.early_window + config.early_window]
    late = samples[-config.late_window :]
    early_mean = sum(early) / len(early)
    late_mean = sum(late) / len(late)
    late_min = min(late)
    late_max = max(late)

    return MemoryStabilityResult(
        early_mean_mb=early_mean,
        late_mean_mb=late_mean,
        late_min_mb=late_min,
        late_max_mb=late_max,
        drift_mb=late_mean - early_mean,
        plateau_mb=late_max - late_min,
    )


def _assert_memory_stable(
    action: Callable[[], object],
    config: MemoryStabilityConfig,
    *,
    process: psutil.Process | None = None,
) -> MemoryStabilityResult:
    result = _measure_memory_stability(action, config, process=process)
    assert result.plateau_mb <= config.plateau_mb, (
        f"Late-window memory range {result.plateau_mb:.2f} MB exceeds "
        f"plateau limit {config.plateau_mb:.2f} MB "
        f"(late samples {result.late_min_mb:.2f}–{result.late_max_mb:.2f} MB)"
    )
    assert result.drift_mb <= config.drift_mb, (
        f"Late-window drift {result.drift_mb:.2f} MB exceeds "
        f"drift limit {config.drift_mb:.2f} MB "
        f"(early mean {result.early_mean_mb:.2f} MB, "
        f"late mean {result.late_mean_mb:.2f} MB)"
    )
    return result


_METADATA_BUFFERS = _make_metadata_parse_buffers()

CI_LEAK_CONFIG = MemoryStabilityConfig(
    warmup=100,
    iterations=2_000,
    sample_every=50,
    plateau_mb=3.0,
    drift_mb=2.0,
)


def test_single_message_parse_does_not_leak() -> None:
    _assert_memory_stable(
        partial(_parse_single_message, _METADATA_BUFFERS.single),
        CI_LEAK_CONFIG,
    )


def test_concatenated_buffer_parse_does_not_leak() -> None:
    _assert_memory_stable(
        partial(_parse_concatenated_messages, _METADATA_BUFFERS.concatenated),
        CI_LEAK_CONFIG,
    )


class _ParseRetainer:
    def __init__(self, buffer: bytes) -> None:
        self._buffer = buffer
        self.objects: list[object] = []

    def __call__(self) -> object:
        obj, _ = read_metadata_response(self._buffer, 0)
        self.objects.append(obj)
        return obj


def test_retaining_parsed_results_increases_memory() -> None:
    retainer = _ParseRetainer(_METADATA_BUFFERS.single)
    result = _measure_memory_stability(
        retainer,
        MemoryStabilityConfig(
            warmup=10,
            iterations=200,
            sample_every=10,
            early_window=5,
            late_window=5,
            plateau_mb=100.0,
            drift_mb=100.0,
        ),
    )
    del retainer.objects

    assert result.drift_mb > 0.5, (
        f"Expected retained parses to increase memory, "
        f"but drift was only {result.drift_mb:.2f} MB"
    )
