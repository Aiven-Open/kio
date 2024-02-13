import enum
import os

from typing import Self

import hypothesis

from hypothesis import settings


class HypothesisProfile(enum.Enum):
    deterministic = enum.auto()
    exhaustive = enum.auto()

    @classmethod
    def from_env(cls) -> Self:
        return cls[
            os.environ.get("HYPOTHESIS_PROFILE", HypothesisProfile.deterministic.name)
        ]


settings.register_profile(
    HypothesisProfile.deterministic.name,
    deadline=None,
    suppress_health_check=[hypothesis.HealthCheck.too_slow],
    derandomize=True,
    max_examples=5,
)
settings.register_profile(
    HypothesisProfile.exhaustive.name,
    deadline=None,
    suppress_health_check=[hypothesis.HealthCheck.too_slow],
)


def configure_hypothesis() -> None:
    settings.load_profile(HypothesisProfile.from_env().name)
