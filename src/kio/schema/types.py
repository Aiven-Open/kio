from kio.static.primitive import PhantomStr
from kio.static.primitive import i32
from kio.static.primitive import i64


class BrokerId(i32): ...


class GroupId(PhantomStr): ...


class ProducerId(i64): ...


class TopicName(PhantomStr): ...


class TransactionalId(PhantomStr): ...
