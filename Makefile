SHELL := /bin/bash
COMPOSE := docker compose

-include .env
export
API_PORT ?= 8000
APP_PORT ?= 8080

.PHONY: help setup dev gen check up down logs

help:
	@grep -E '^## ' Makefile | sed 's/^## //'

## setup   install backend + frontend deps, create .env
## dev     db + redis in Docker; api, worker, web with hot reload
## gen     regenerate openapi.json and the typed TS client
## check   lint, format, typecheck, tests (backend + frontend)
## up      prod-like stack in Docker (2 workers), web on APP_PORT
## down    stop the prod-like stack
## logs    follow prod-like stack logs

setup:
	cd backend && uv sync --frozen
	cd frontend && npm ci
	test -f .env || cp .env.example .env

dev:
	$(COMPOSE) up -d --wait db redis
	cd backend && uv run alembic upgrade head
	trap 'kill 0' INT TERM EXIT; \
	(cd backend && uv run uvicorn app.api.main:app --reload --host 127.0.0.1 --port $(API_PORT)) & \
	(cd backend && uv run watchfiles --filter python "celery -A app.worker.celery_app worker -Q default,llm --pool=solo --loglevel=INFO" app) & \
	(cd frontend && npm run dev) & \
	wait

gen:
	cd backend && uv run python -m app.export_openapi
	cd frontend && npm run gen

check:
	$(COMPOSE) up -d --wait db redis
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy app tests && uv run pytest -q
	cd frontend && npm run lint && npm run typecheck && npm test

up:
	$(COMPOSE) --profile app up -d --build --scale worker=2
	for i in $$(seq 1 60); do curl -sf localhost:$(API_PORT)/ready && echo && exit 0; sleep 1; done; exit 1

down:
	$(COMPOSE) --profile app down

logs:
	$(COMPOSE) --profile app logs -f --tail=50
