from kio.static.primitive import i32
from kio.static.primitive import i64


class BrokerId(i32): ...


class GroupId(str): ...


class ProducerId(i64): ...


class TopicName(str): ...


class TransactionalId(str): ...
