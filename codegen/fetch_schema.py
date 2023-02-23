import shutil
from pathlib import Path
from typing import Final

import requests
from pydantic import BaseModel
from pydantic import HttpUrl

schema_dir: Final = Path(__file__).parent.parent.resolve() / "schema"
build_tag: Final = "3.4.0"
list_url: Final = (
    f"https://api.github.com/repos/apache/kafka/contents/clients/src/main/resources"
    f"/common/message?ref={build_tag}"
)


class ContentFile(BaseModel, allow_mutation=False):
    name: str
    download_url: HttpUrl


class ContentsResponse(BaseModel, allow_mutation=False):
    __root__: tuple[ContentFile, ...]


def main() -> None:
    # Remove existing schema directory.
    if schema_dir.exists():
        shutil.rmtree(schema_dir)
    schema_dir.mkdir(parents=True)

    # Fetch and parse file list.
    response = requests.get(list_url)
    response.raise_for_status()
    parsed_response = ContentsResponse.parse_raw(response.content)

    # Fetch and store
    for content_file in parsed_response.__root__:
        file_path = schema_dir / content_file.name
        with (
            file_path.open("wb") as fd,
            requests.get(content_file.download_url, stream=True) as stream_response,
        ):
            stream_response.raise_for_status()
            for chunk in stream_response.iter_content(chunk_size=131_072):
                fd.write(chunk)


if __name__ == "__main__":
    main()
