import enum
import os

from typing import Self

import hypothesis

from hypothesis import settings
from hypothesis.strategies import register_type_strategy
from hypothesis.strategies import sampled_from

from kio.static.primitive import Records

from .fixtures import record_batch_data_v2


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

    register_type_strategy(Records, sampled_from(record_batch_data_v2))
