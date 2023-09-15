import pytest

from kio.static._phantom import Phantom


def truthy(value: bool) -> bool:
    return value is True


class Truthy(Phantom[bool], predicate=truthy, bound=bool):
    ...


class TestPhantom:
    def test_raises_type_error_when_omitting_bound(self) -> None:
        with pytest.raises(
            TypeError,
            match=r"^Definition of phantom type must set bound\.$",
        ):

            class A(Phantom, predicate=truthy):
                ...

    def test_raises_type_error_when_omitting_predicate(self) -> None:
        with pytest.raises(
            TypeError,
            match=r"^Definition of phantom type must set predicate\.$",
        ):

            class A(Phantom, bound=bool):
                ...

    def test_can_inherit_attributes(self) -> None:
        class A(Phantom, predicate=truthy, bound=bool):
            ...

        class B(A):
            ...

        assert B.__bound__ is bool  # type: ignore[misc]
        assert B.__predicate__ is truthy  # type: ignore[misc]

    def test_passing_predicate_is_instance(self) -> None:
        assert isinstance(True, Truthy)

    def test_rejecting_predicate_is_not_instance(self) -> None:
        assert not isinstance(False, Truthy)
