# Work-around for broken support for cache decorators in
# https://github.com/python/typeshed/issues/6347
# https://stackoverflow.com/a/73517689
from typing import TYPE_CHECKING
from typing import TypeVar

__all__ = ("cache",)

if TYPE_CHECKING:
    _C = TypeVar("_C")

    def cache(c: _C) -> _C:
        return c

else:
    from functools import cache
