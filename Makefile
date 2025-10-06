install:
	uvsync

install-dev:
	uv sync --dev

lint:
	ruff check

IP ?= 192.168.0.200
dev:
	uv run flask --debug --app page_analyzer:app run --host=$(IP)
