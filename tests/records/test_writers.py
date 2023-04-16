import datetime
from typing import IO

from kio.records.schema import Record
from kio.records.schema import RecordBatch
from kio.records.schema import RecordHeader
from kio.records.writers import write_batch

from .fixtures import record_batch_data_v2


def test_write_record_batch(buffer: IO[bytes]) -> None:
    expected_result = b"".join(record_batch_data_v2)
    batches = [
        RecordBatch(
            base_offset=0,
            batch_length=59,
            partition_leader_epoch=1,
            crc=51946096,
            attributes=0,
            last_offset_delta=0,
            base_timestamp=1503229838908,
            max_timestamp=1503229838908,
            producer_id=-1,
            producer_epoch=-1,
            base_sequence=-1,
            records=(
                Record(
                    attributes=0,
                    timestamp=datetime.datetime(
                        2017, 8, 20, 11, 50, 38, 908000, tzinfo=datetime.UTC
                    ),
                    offset=0,
                    key=None,
                    value=b"123",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=1,
            batch_length=64,
            partition_leader_epoch=2,
            crc=3361520931,
            attributes=0,
            last_offset_delta=1,
            base_timestamp=1503229959532,
            max_timestamp=1503229959700,
            producer_id=-1,
            producer_epoch=-1,
            base_sequence=-1,
            records=(
                Record(
                    attributes=0,
                    timestamp=datetime.datetime(
                        2017, 8, 20, 11, 52, 39, 532000, tzinfo=datetime.UTC
                    ),
                    offset=1,
                    key=None,
                    value=b"",
                    headers=(),
                ),
                Record(
                    attributes=0,
                    timestamp=datetime.datetime(
                        2017, 8, 20, 11, 52, 39, 700000, tzinfo=datetime.UTC
                    ),
                    offset=2,
                    key=None,
                    value=b"",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=3,
            batch_length=59,
            partition_leader_epoch=2,
            crc=772507063,
            attributes=0,
            last_offset_delta=0,
            base_timestamp=1503229962141,
            max_timestamp=1503229962141,
            producer_id=-1,
            producer_epoch=-1,
            base_sequence=-1,
            records=(
                Record(
                    attributes=0,
                    timestamp=datetime.datetime(
                        2017, 8, 20, 11, 52, 42, 141000, tzinfo=datetime.UTC
                    ),
                    offset=3,
                    key=None,
                    value=b"123",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=0,
            batch_length=69,
            partition_leader_epoch=0,
            crc=1557720914,
            attributes=0,
            last_offset_delta=0,
            base_timestamp=1535546684353,
            max_timestamp=1535546684353,
            producer_id=-1,
            producer_epoch=-1,
            base_sequence=-1,
            records=(
                Record(
                    attributes=0,
                    timestamp=datetime.datetime(
                        2018, 8, 29, 12, 44, 44, 353000, tzinfo=datetime.UTC
                    ),
                    offset=0,
                    key=None,
                    value=b"hdr",
                    headers=(
                        RecordHeader(
                            key=b"hkey",
                            value=b"hval",
                        ),
                    ),
                ),
            ),
        )
    ]

    for batch in batches:
        write_batch(buffer, batch)

    buffer.seek(0)

    assert buffer.read(len(expected_result)) == expected_result
