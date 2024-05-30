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
