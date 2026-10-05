# demo-idea-v2

A lean starter for AI-heavy web apps: **React + MUI + Redux Toolkit + FastAPI + Celery + Postgres + Redis + PydanticAI**.

- Two folders, two package managers you already know: `frontend/` (npm) and `backend/` (uv).
- No monorepo tooling. A `Makefile` and `compose.yml` at the root tie it together.
- One backend image runs three roles: **api**, **worker**, **migrate**.
- Works offline out of the box: the AI agents use a fake model until you set a real one.

```
browser ─► web (Vite in dev, nginx in prod) ─► /api ─► FastAPI ──► Postgres (+pgvector)
                                                  │  └─ SSE chat (PydanticAI agent)
                                                  └─► Redis ─► Celery workers ─► LLM jobs
```

## Quick start

Prerequisites: git, make, Docker Desktop (running), [uv](https://docs.astral.sh/uv/), Node 22.12+ (22.11 works with the current pins).

```sh
git clone git@github.com:bachtly/lean-web-stack.git myapp
cd myapp
make setup
make dev
```

Open http://localhost:5173. You get a **Notes** page (create a note, click **Summarise**: that runs an AI job on a Celery worker) and a streaming **Chat** page.
API docs: http://localhost:8000/docs.

Ports busy on your machine? Edit `.env` (created by `make setup`), see [First day](docs/playbooks/00-first-day.md#ports).

## Everyday commands

| Command | What it does |
|---|---|
| `make setup` | install backend + frontend deps, create `.env` |
| `make dev` | Postgres + Redis in Docker; api, worker and web with hot reload |
| `make gen` | regenerate `backend/openapi.json` and the typed client `frontend/src/api/schema.d.ts` |
| `make check` | ruff, ruff format, mypy, pytest, eslint, tsc, vitest: run before every push |
| `make up` / `make down` | production-like stack in Docker (2 workers, nginx on `APP_PORT`) |
| `make help` | list all targets |

## Layout

```
.
├─ Makefile  compose.yml  .env.example  deploy.sh
├─ .github/workflows/ci.yml        path-filtered CI + contract check + build/deploy on main
├─ docs/playbooks/                 how-to guides (start here)
├─ scripts/new-project.sh          start a new project from this template
├─ frontend/                       npm · Vite + React + TS · MUI v9 · RTK Query · React Router · RHF + Zod · vitest
│  ├─ CLAUDE.md                    frontend rules for AI assistants (incl. MUI v9 gotchas)
│  └─ src/
│     ├─ app/                      theme, providers, router, store
│     ├─ services/baseApi.ts       RTK Query root + fromApi() over the typed client
│     ├─ api/                      client.ts (openapi-fetch) + schema.d.ts (generated)
│     ├─ pages/                    one per route (lazy-loaded)
│     ├─ components/               shared UI: layout, QueryState, FormDialog, form/ inputs
│     └─ features/                 notes/ (CRUD + filters + AI summary job), chat/ (SSE stream)
└─ backend/                        uv · one package "app" · one Dockerfile
   ├─ app/core/                    settings (env only), db (async + sync engines), redis
   ├─ app/models/                  SQLAlchemy models
   ├─ app/api/                     FastAPI app + routes (health, notes, jobs, chat)
   ├─ app/ai/                      PydanticAI agents, offline models, rate limits
   ├─ app/worker/                  Celery app + tasks (queues: default, llm)
   ├─ migrations/                  Alembic
   └─ tests/
```

## Playbooks

| # | Playbook | Read it when |
|---|---|---|
| 0 | [First day](docs/playbooks/00-first-day.md) | you just joined |
| 1 | [Daily workflow](docs/playbooks/01-daily-workflow.md) | every day: branch, code, check, PR |
| 2 | [Add a feature (vertical slice)](docs/playbooks/02-add-a-feature.md) | you build something across DB, API, worker, AI and UI |
| 3 | [Background jobs](docs/playbooks/03-background-jobs.md) | work takes more than about a second, or runs on a schedule |
| 4 | [AI agents](docs/playbooks/04-ai-agents.md) | you add or change an agent, or switch to a real model |
| 5 | [Database](docs/playbooks/05-database.md) | you change a model |
| 6 | [Build and deploy](docs/playbooks/06-build-and-deploy.md) | you ship, or plan scaling |
| 7 | [New project from this template](docs/playbooks/07-new-project.md) | you start a new app |
| 8 | [Troubleshooting](docs/playbooks/08-troubleshooting.md) | something is off |
| 9 | [Frontend (MUI, RTK Query, Router)](docs/playbooks/09-frontend-ui.md) | before your first frontend change |

## When to add more tooling

This template stays small on purpose. Add Turborepo (caching, affected-only runs) when `make check` takes more than about 5 minutes; consider Nx when there are many apps and Python packages owned by several teams.
