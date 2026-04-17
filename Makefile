# Enable globstar to allow ** to match recursive directories.
SHELL := /usr/bin/env bash -O globstar

.PHONY: fetch-schema-src
fetch-schema-src:
	python3 -m codegen.fetch_schema

.PHONY: generate-schema
generate-schema:
	docker compose build java_tester
	docker compose run --rm java_tester --print-error-codes > error-codes.txt
	python3 -m codegen error-codes.txt
	pre-commit run --all-files || true

.PHONY: build-schema
build-schema: fetch-schema-src generate-schema

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info {**/,}/__pycache__ build dist src/{**/,}*.so .coverage rust/target src/kio/_version.py src/kio/lib_kio_native.dylib.dSYM

.PHONY: nuke
nuke: clean
	rm -rf .hypothesis .mypy_cache .import_linter_cache .pytest_cache .ruff_cache

build:
	maturin develop
