# 0 · First day

Goal: a running app on your machine in about 10 minutes, and a map of where things live.

## 1. Install the tools

| Tool | Check | Notes |
|---|---|---|
| git, make | `git --version`, `make --version` | macOS: Xcode command line tools |
| Docker Desktop | `docker info` | must be running; runs Postgres and Redis |
| uv | `uv --version` | `brew install uv`; manages Python too |
| Node | `node --version` | 22.12+ recommended. 22.11 works with the current pins (Vite 6, vitest 3, jsdom 26) |

## 2. Get it running

```sh
git clone git@github.com:bachtly/lean-web-stack.git
cd lean-web-stack
make setup
make dev
```

`make dev` starts Postgres and Redis in Docker, applies migrations, then runs three processes with hot reload in one terminal: the API (uvicorn), the worker (Celery) and the web app (Vite). `Ctrl+C` stops all three.

Check it:

| URL | Expect |
|---|---|
| http://localhost:5173 | Notes and Chat pages; light/dark toggle top-right |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/ready | `{"db":"ok","redis":"ok"}` |

Try the full path once: create a note, click **Summarise**. The API queues a Celery job, the worker runs the AI agent (offline model), the page polls the job and shows the summary and tags.

## 3. Run the checks

```sh
make check
```

This is the same gate CI runs. It must be green before you push.

## Ports

All host ports come from `.env` (created from `.env.example` by `make setup`):

| Variable | Default | Used by |
|---|---|---|
| `API_PORT` | 8000 | FastAPI in `make dev` and `make up` |
| `WEB_PORT` | 5173 | Vite dev server |
| `APP_PORT` | 8080 | nginx (web + /api) in `make up` |
| `DB_PORT` | 5432 | Postgres on your machine |
| `REDIS_PORT` | 6379 | Redis on your machine |

If you change `DB_PORT` or `REDIS_PORT`, also change the port inside `DATABASE_URL` / `REDIS_URL` in `.env`.

## 4. Where things live

| You want to change… | Go to |
|---|---|
| a page / route | `frontend/src/pages/` + `frontend/src/app/router.tsx` (read [Frontend](09-frontend-ui.md) first) |
| a feature's components, endpoints, state | `frontend/src/features/<feature>/` |
| colours, fonts, dark mode, component defaults | `frontend/src/app/theme.ts` |
| shared UI (form inputs, dialogs, loading/error) | `frontend/src/components/` |
| how the frontend calls the API | RTK Query endpoints in `features/<f>/<f>Api.ts`, over `frontend/src/api/client.ts` (typed by `schema.d.ts`, never edit that by hand) |
| an endpoint | `backend/app/api/routes/` |
| a table | `backend/app/models/` + a migration in `backend/migrations/` |
| background work | `backend/app/worker/tasks.py` |
| an AI agent | `backend/app/ai/` |
| config | `backend/app/core/settings.py` (values come from env / `.env`) |

Next: [Daily workflow](01-daily-workflow.md). Touching the frontend? Also read [Frontend](09-frontend-ui.md).
