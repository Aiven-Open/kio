from typing import Final
from typing import NamedTuple


class CustomErrorCode(NamedTuple):
    code: int
    name: str
    retriable: bool
    message: str


CUSTOM_ERROR_CODES: Final[dict[str, tuple[CustomErrorCode, ...]]] = {
    "4.3.1": (
        CustomErrorCode(
            code=136,
            name="controller_id_not_registered",
            retriable=False,
            message="The given controller ID was not registered.",
        ),
    ),
}
