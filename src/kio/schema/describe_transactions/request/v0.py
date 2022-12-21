"""
Generated from DescribeTransactionsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTransactionsRequest:
    __flexible__: ClassVar[bool] = True
    transactional_ids: tuple[TransactionalId, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Array of transactionalIds to include in describe results. If empty, then no results will be returned."""
