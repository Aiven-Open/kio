"""
This is a less powerful, but good enough approximation of the phantom-types library,
lacking some bells and whistles like Pydantic support and bounds checks.
"""

from __future__ import annotations

import abc

from collections.abc import Callable
from types import ModuleType
from typing import Generic
from typing import Protocol
from typing import Self
from typing import TypeAlias
from typing import TypeVar
from typing import runtime_checkable

hypothesis: ModuleType | None

try:
    import hypothesis.strategies
except ImportError:  # pragma: no cover
    hypothesis = None


U = TypeVar("U")
Predicate: TypeAlias = Callable[[U], bool]


@runtime_checkable
class InstanceCheckable(Protocol):
    def __instancecheck__(self, instance: object) -> bool: ...


class PhantomMeta(abc.ABCMeta):
    def __instancecheck__(self, instance: object) -> bool:
        return (
            issubclass(self, InstanceCheckable) and self.__instancecheck__(instance)  # type: ignore[attr-defined]
        )

    def __call__(cls, instance):  # type: ignore[no-untyped-def]
        return cls.parse(instance)  # type: ignore[attr-defined]


T = TypeVar("T")


class Phantom(Generic[T], metaclass=PhantomMeta):
    __bound__: type[T]
    __predicate__: Predicate[T]

    def __init_subclass__(
        cls,
        bound: type[T] | None = None,
        predicate: Predicate[T] | None = None,
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)
        if bound is None:
            if getattr(cls, "__bound__", ...) is ...:
                raise TypeError("Definition of phantom type must set bound.")
        else:
            cls.__bound__ = bound

        if predicate is None:
            if getattr(cls, "__predicate__", ...) is ...:
                raise TypeError("Definition of phantom type must set predicate.")
        else:
            cls.__predicate__ = predicate

        if hypothesis is not None:  # pragma: no cover
            cls.__hypothesis_hook__()

    @classmethod
    def __hypothesis_hook__(cls) -> None: ...

    @classmethod
    def __instancecheck__(cls, instance: object) -> bool:
        return isinstance(instance, cls.__bound__) and cls.__predicate__(instance)

    @classmethod
    def parse(cls, instance: object) -> Self:
        if not isinstance(instance, cls):
            raise TypeError(f"Could not parse {cls.__qualname__} from {instance!r}")
        return instance
