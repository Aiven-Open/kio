from typing import NewType

from kio.schema.primitive import i32
from kio.schema.primitive import i64

TopicName = NewType("TopicName", str)
BrokerId = NewType("BrokerId", i32)
ProducerId = NewType("ProducerId", i64)
TransactionalId = NewType("TransactionalId", str)
GroupId = NewType("GroupId", str)
