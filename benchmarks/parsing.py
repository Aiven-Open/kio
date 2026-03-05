from __future__ import annotations

import datetime
import io
import uuid

from copy import replace

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
            name=TopicName(f"topic {n}"),
            topic_id=uuid.uuid4(),
            is_internal=False,
            partitions=(
                MetadataResponsePartition(
                    error_code=ErrorCode.delegation_token_expired,
                    partition_index=i32(5679),
                    leader_id=BrokerId(2345),
                    leader_epoch=i32(6445678),
                    replica_nodes=(BrokerId(12345), BrokerId(7651)),
                    isr_nodes=(),
                    offline_replicas=(),
                ),
            ),
            topic_authorized_operations=i32(765443),
        )
        for n in range(100)
    ),
)

with io.BytesIO() as buffer:
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1001)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1002)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1003)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1004)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1005)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1006)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1007)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1008)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1009)))
    write_metadata_response(buffer, replace(instance, controller_id=BrokerId(1010)))
    buffer = buffer.getvalue()


def perform_parsing(
    loops: int,
) -> float:
    loop_range = range(loops)
    # accumulated = 0.0

    for _ in loop_range:
        offset = 0
        # t0 = pyperf.perf_counter()
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
        # accumulated += pyperf.perf_counter() - t0
        # assert offset == len(buffer), "buffer not exhausted after read"

    # return accumulated


if __name__ == "__main__":
    # from scalene import scalene_profiler
    # scalene_profiler.start()
    # perform_parsing(1000)
    # scalene_profiler.stop()

    perform_parsing(1000)

    # import pyperf
    # runner = pyperf.Runner()
    # runner.bench_time_func("roundtrip", perform_parsing, inner_loops=10000)
