from kio.schema.primitive import i32
from kio.schema.primitive import i64


class BrokerId(i32):
    ...


class TopicName(str):
    ...


class ProducerId(i64):
    ...


class TransactionalId(str):
    ...


class GroupId(str):
    ...
