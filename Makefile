install:
	uv sync

install-dev:
	uv sync --dev

lint:
	ruff check

IP ?= 192.168.0.200
dev:
	uv run flask --debug --app page_analyzer:app run --host=$(IP)

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b $(IP):$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
