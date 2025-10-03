install:
	uv sync

install-dev:
	uv sync --dev

lint:
	ruff check

dev:
	uv run flask --debug --app page_analyzer:app run --host=192.168.0.200 --port 5000

