import pydantic


class BaseModel(
    pydantic.BaseModel,
    allow_mutation=False,
):
    ...
