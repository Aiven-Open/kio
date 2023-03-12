# ruff: noqa: T201

import hashlib
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Final

import requests
from pydantic import BaseModel
from pydantic import HttpUrl

from . import build_tag

base: Final = Path(__file__).parent.parent.resolve() / "schema"
schema_dir: Final = base / build_tag
cache_dir: Final = base / "cache"
list_url: Final = (
    f"https://api.github.com/repos/apache/kafka/contents/clients/src/main/resources"
    f"/common/message?ref={build_tag}"
)


class ContentFile(BaseModel, allow_mutation=False):
    name: str
    download_url: HttpUrl
    sha: str


class ContentsResponse(BaseModel, allow_mutation=False):
    __root__: tuple[ContentFile, ...]


def git_hash(file: Path) -> str | None:
    if not file.exists():
        return None
    size = file.stat().st_size
    raw = b"blob " + str(size).encode() + b"\00" + file.read_bytes()
    return hashlib.sha1(raw).hexdigest()  # noqa: S324


def fetch_file(content_file: ContentFile) -> None:
    cache_path = cache_dir / content_file.name
    file_path = schema_dir / content_file.name

    # Use cached file if exists and hash matches.
    if cache_path.exists() and (content_file.sha == git_hash(cache_path)):
        print(f"Using up-to-date {file_path.name} from cache.", file=sys.stderr)
        shutil.move(cache_path, file_path)
        return

    with (
        requests.get(
            content_file.download_url,
            stream=True,
            timeout=5,
        ) as stream_response,
        file_path.open("wb") as fd,
    ):
        stream_response.raise_for_status()
        for chunk in stream_response.iter_content(chunk_size=131_072):
            fd.write(chunk)


def main() -> None:
    base.mkdir(parents=True, exist_ok=True)

    # Remove existing cache directory.
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    # Make existing schema directory the new cache directory.
    if schema_dir.exists():
        shutil.move(schema_dir, cache_dir)

    # Create schema directory.
    schema_dir.mkdir(parents=True)

    # Fetch and parse file list.
    print("Fetching file list ...", end="", file=sys.stderr)
    response = requests.get(list_url, timeout=5)
    response.raise_for_status()
    parsed_response = ContentsResponse.parse_raw(response.content)
    print(" done.", file=sys.stderr)

    # Fetch and store each file, using threading.
    print("Fetching files ...", end="", file=sys.stderr)
    with ThreadPoolExecutor() as pool:
        for content_file in parsed_response.__root__:
            pool.submit(fetch_file, content_file)
    print(" done.")


if __name__ == "__main__":
    main()
