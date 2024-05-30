from __future__ import annotations

import enum
import uuid

from typing import Final

uuid_zero: Final = uuid.UUID(int=0)


class EntityType(enum.Enum):
    request = enum.auto()
    response = enum.auto()
    header = enum.auto()
    data = enum.auto()
    nested = enum.auto()
