# Add Share Group Offsets support to kio (KCON-454 blocker)

## Verified facts (2026-07-29)

- This repo (`/home/olena.linux/aiven/kio`) is at `870abef7`, tag `0.6.2` — matches the ticket's pinned commit/version exactly.
- kio's schema tree is **fully generated**, never hand-written. Nothing needs to be manually authored under `src/kio/schema/`.
- Confirmed directly against `apache/kafka` on GitHub:
  - Kafka **4.2.0** (released 2026-02-17) contains `DescribeShareGroupOffsetsRequest.json` / `...Response.json` (apiKey 90) with `validVersions: "0-1"` and the KIP-1226 `Lag` field (`int64`, `versions: "1+"`, `ignorable`, `default: -1`) on `DescribeShareGroupOffsetsResponsePartition`.
  - `AlterShareGroupOffsetsRequest.json` (apiKey 91) and `DeleteShareGroupOffsetsRequest.json` (apiKey 92) also exist at 4.2.0.
  - Kafka `4.1.0` only has DescribeShareGroupOffsets **v0** (no Lag) — confirms v1/Lag is new in 4.2.0, matching KIP-1226's "Accepted for 4.2" status.
- The current pin, `3.9.0`, predates all of these (kio's `share_group_describe`, API 77, tops out at key 87 in this pin — matches the ticket's own investigation).
- Codegen already supports every shape these new messages need — no pipeline changes required:
  - Nullable array-of-struct fields (`Topics` is `nullableVersions: "0+"`) — same pattern already generated for `topics: tuple[OffsetFetchRequestTopic, ...] | None` in `src/kio/schema/offset_fetch/v4/request.py`.
  - Versioned `int64` field with non-zero default (`Lag`, `versions: "1+"`, `default: -1`) — same pattern as `log_start_offset: i64 = field(..., default=i64(-1))` in `src/kio/schema/fetch/v5/request.py`.
- `codegen/fetch_schema.py` fetches **all** JSON files for the pinned tag unconditionally (no per-API filter). We accept the full 3.9.0 -> 4.2.0 bump (bringing in unrelated new messages: `StreamsGroupDescribe`/`Heartbeat`, `EndTxnMarker`, a `ListClientMetricsResources` -> `ListConfigResources` rename) rather than trying to cherry-pick only the share-group-offsets files, consistent with how prior version bumps in this repo were done (e.g. commit `a4a78b18` #206, `c73175a5` #213).
- Generate all three of 90/91/92 together since they come for free from the same regeneration.

## Steps

1. **Bump the Kafka pin in lockstep** (3 files):
   - `codegen/__init__.py`: `build_tag: Final = "3.9.0"` -> `"4.2.0"`.
   - `java_tester/build.gradle`: `org.apache.kafka:kafka-clients:3.9.0` -> `4.2.0` (needed because `make generate-schema` runs this Java tester to print `error-codes.txt` and for the Java-roundtrip tests).
   - `compose.yml`: `apache/kafka:3.9.0` image -> `4.2.0` (used for integration tests / local broker).

2. **Regenerate the schema**: run `make build-schema` (`fetch-schema-src` then `generate-schema`), which:
   - Wipes and repopulates `src/kio/schema/` from the fetched 4.2.0 JSON, producing new packages `describe_share_group_offsets/{v0,v1}/`, `alter_share_group_offsets/v0/`, `delete_share_group_offsets/v0/` (mirroring the `share_group_describe/v0/` pattern: frozen dataclass, `EntityType`, `__api_key__`, `kafka_type` metadata).
   - Regenerates `src/kio/schema/index.py` (api_key_map/schema_name_map), `src/kio/schema/types.py`, `src/kio/schema/errors.py`.
   - Regenerates matching Hypothesis roundtrip + Java-roundtrip tests under `tests/generated/`.
   - Runs `pre-commit run --all-files` for formatting.

3. **Triage incidental churn from the full pin bump**: review the diff beyond the 3 target APIs. Based on prior bumps, watch for:
   - New `*Ms` duration-like field names not in codegen's `timedelta_names`/`datetime_names` allowlist (`codegen/parser.py`) — would raise `NotImplementedError`; add to the allowlist if needed (e.g. for `StreamsGroup*`).
   - New non-`*Data`-suffixed class names needed in `RootMessageInfo.java`'s exception list (prior precedent: KRaft `VotersRecord` in the 3.7->3.8 bump) — likely relevant for `EndTxnMarker`.
   - The `ListClientMetricsResources` -> `ListConfigResources` rename removing old generated modules; confirm nothing outside `kio` depends on the old name (it's internal/generated, so this repo alone should be safe, but check `docs/` references).
   - Fix these iteratively by re-running `make build-schema` until it completes cleanly.

4. **Verify the new share-group-offsets schemas concretely**:
   - Confirm `describe_share_group_offsets/v1/response.py` includes `lag: i64` (with `default=i64(-1)`) on the partition-level nested dataclass, and that `v0/response.py` does not have it — matching KIP-1226's ignorable/versioned semantics from the ticket's decision log ("Lag = broker-side (KIP-1226); use it directly").
   - Confirm request/response dataclasses match the ticket's expected shape: `groups: [{group_id, topics: [{topic_name, partitions: [int32]}] | None}]`.
   - Spot-check `alter_share_group_offsets` and `delete_share_group_offsets` v0 generated modules for sanity (API keys 91/92).

5. **Run full test/lint suite** to confirm correctness before release:
   - `pytest` (unit + Hypothesis roundtrip tests, including new `tests/generated/test_describe_share_group_offsets_*` etc.)
   - `docker compose run --rm java_tester ...` based Java-roundtrip tests for top-level request/response types (validates wire-format compatibility against real kafka-clients 4.2.0 classes).
   - `mypy` (repo requires passing static type checks per `.github/CONTRIBUTING.md`).
   - Coverage check (repo requires 100% test coverage per `setup.cfg`/CONTRIBUTING; generated schema is excluded from coverage per `setup.cfg`, but hand-touched codegen fixes are not).
   - CI will also run `.github/workflows/ci.yaml`'s `check-generate-schema` job, which fails if committed generated output doesn't match a fresh regeneration — treat this as the final correctness gate.

6. **Cut a new kio release** per `.github/CONTRIBUTING.md`:
   - Merge the pin-bump PR to `main`.
   - Create and publish a GitHub Release with a new SemVer tag (minor bump, e.g. `0.7.0`, since this is a backward-compatible feature addition) — this triggers `.github/workflows/release.yaml` to build wheels/sdist via maturin and publish to PyPI.

7. **Hand off to aiven-core / KCON-454** (outside this repo, not implemented here):
   - Bump `deps/python3-kio/python3-kio.spec` in `aiven-core` (commit ref + `Version:` field) to the new kio release.
   - Notify/unblock KCON-454 so `py/kafka-caller/src/avn/kafka_caller/api/describe_share_group_offsets.py` can be implemented on top of the new `kio.schema.describe_share_group_offsets` module, using the response's `lag` field directly (per the ticket's decision log, not `latest_offset - start_offset`).

## Key risk / open item to flag back to the ticket owner

Jumping from `3.9.0` straight to `4.2.0` pulls in several Kafka releases' worth of unrelated protocol changes (not just share groups). This is unavoidable given `fetch_schema.py` has no per-API filtering, and matches how this repo has always done version bumps, but it does mean the PR's diff and review surface will be larger than "just the 3 share-group-offsets APIs" — this should be called out explicitly in the PR description so reviewers aren't surprised.

## Todos

- [ ] Bump Kafka pin to 4.2.0 in `codegen/__init__.py`, `java_tester/build.gradle`, `compose.yml`
- [ ] Run `make build-schema` to regenerate `src/kio/schema`, `index.py`, `types.py`, `errors.py`, `tests/generated`
- [ ] Fix any incidental codegen issues from unrelated new messages (StreamsGroup*, EndTxnMarker, ListConfigResources rename)
- [ ] Verify describe/alter/delete_share_group_offsets generated dataclasses match expected shapes, especially v1 lag field
- [ ] Run pytest, java_tester roundtrip tests, mypy, and coverage; confirm `check-generate-schema` CI job is clean
- [ ] Cut a new SemVer minor GitHub Release to publish to PyPI
- [ ] Document handoff steps for bumping `deps/python3-kio/python3-kio.spec` in aiven-core and unblocking KCON-454
