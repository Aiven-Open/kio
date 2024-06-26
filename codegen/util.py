import pathlib

import pydantic


class BaseModel(
    pydantic.BaseModel,
    allow_mutation=False,
): ...


def create_package(path: pathlib.Path) -> None:
    path.mkdir(exist_ok=True)
    (path / "__init__.py").touch(exist_ok=True)
