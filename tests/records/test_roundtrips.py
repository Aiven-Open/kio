import io

from hypothesis import given
from hypothesis.strategies import builds
from hypothesis.strategies import integers
from hypothesis.strategies import lists

from kio.records.readers import read_batch
from kio.records.schema import NewRecordBatch
from kio.records.schema import Record
from kio.records.writers import write_new_batch
from kio.static.primitive import i32


@given(
    builds(
        NewRecordBatch,
        records=lists(
            builds(
                Record,
                # The offsets field is an i64 field, but logically all values in the i64
                # space cannot be supported as it breaks RecordBatch.last_offset_delta.
                # Alternatively we could do something more fancy here to limit the
                # actual delta between lowest and highest generated.
                offset=integers(min_value=0, max_value=i32.__high__),
            ),
            min_size=1,
        ).map(tuple),
    )
)
def test_roundtrip_new_record_batch(new_record_batch: NewRecordBatch) -> None:
    with io.BytesIO() as buffer:
        write_new_batch(buffer, new_record_batch)
        buffer.seek(0)
        result = read_batch(buffer)

    assert result.producer_id == new_record_batch.producer_id
    assert result.producer_epoch == new_record_batch.producer_epoch
    assert result.partition_leader_epoch == new_record_batch.partition_leader_epoch
    assert result.base_sequence == new_record_batch.base_sequence
    assert result.records == new_record_batch.records
    assert result.attributes == new_record_batch.attributes
