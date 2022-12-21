from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterator
from typing import NamedTuple


class VersionRange(NamedTuple):
    low: int | float
    high: int | float

    def matches(self, value: int) -> bool:
        return self.low <= value <= self.high

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], VersionRange]]:
        def parse_valid_versions(value: object) -> VersionRange:
            if not isinstance(value, str):
                raise ValueError("Version range must be str")

            if value == "none":
                return VersionRange(float("inf"), float("-inf"))

            if value.endswith("+"):
                return VersionRange(int(value.removesuffix("+")), float("inf"))

            low: str | int
            high: str | int

            try:
                low, high = value.split("-", 1)
            except ValueError as exception:
                try:
                    low = high = int(value)
                except ValueError:
                    raise ValueError(
                        "Version range must be in format 'N-N' or 'N' or 'N+' or 'none'"
                    ) from exception

            return VersionRange(int(low), int(high))

        yield parse_valid_versions

    @property
    def range(self) -> range:
        assert isinstance(self.low, int)
        assert isinstance(self.high, int)
        return range(self.low, self.high + 1)

    def iter(self) -> Iterator[int]:
        return iter(self.range)
