.PHONY: fetch-schema-src
fetch-schema-src:
	python3 -m codegen.fetch_schema

.PHONY: generate-schema
generate-schema:
	python3 -m codegen
	pre-commit run --all-files || true

.PHONY: build-schema
build-schema: fetch-schema-src generate-schema
