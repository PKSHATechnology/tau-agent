up:
	docker compose -f compose.dev.yml up -d

down:
	docker compose -f compose.dev.yml down

logs:
	docker compose -f compose.dev.yml logs -f

build:
	docker compose -f compose.dev.yml build

format:
	ruff format .
	ruff check . --fix
