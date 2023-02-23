fetch-schema-src:
	python3 -m codegen.fetch_schema

generate-schema:
	python3 -m codegen
	bash -c 'pre-commit run --all-files || true'

build-schema: fetch-schema-src generate-schema
