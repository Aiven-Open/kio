fetch-schema-src:
	python3 -m codegen.fetch_schema

generate-schema:
	python3 -m codegen
	pre-commit run --all-files

build-schema: fetch-schema-src generate-schema
