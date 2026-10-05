# 1 · Daily workflow

## The loop

```sh
git switch main
git pull
git switch -c feat/short-name
make dev
```

Code with `make dev` running (API, worker and web all hot reload). Then:

| Step | Command | Why |
|---|---|---|
| Changed an endpoint, request or response model? | `make gen` | regenerates the typed client; type errors in the frontend now show what to update |
| Changed a model (table)? | see [Database](05-database.md) | new Alembic migration |
| Before every push | `make check` | lint, format, types, tests for both sides |
| Commit | `git commit -m "feat(notes): ..."` | conventional commits keep history readable |
| Push and open a PR | `git push -u origin HEAD` | CI runs |

## What CI runs on your PR

`.github/workflows/ci.yml` uses path filters, so you only wait for what you touched:

| You changed | Jobs |
|---|---|
| `backend/**` or `compose.yml` | backend (ruff, mypy, pytest against Postgres) + contract |
| `frontend/**` | frontend (eslint, tsc, vitest) + contract |
| both | all three |

The **contract** job runs `make gen` and fails if `backend/openapi.json` or `frontend/src/api/schema.d.ts` changed. Meaning: you changed the API but forgot `make gen`. Run it, commit, push.

On merge to `main`, CI builds the backend and web images, tagged with the commit SHA, and runs `deploy.sh` (see [Build and deploy](06-build-and-deploy.md)).

## Working in parallel without stepping on each other

- Keep a feature in its own folders: `frontend/src/features/<feature>/`, `backend/app/api/routes/<feature>.py`, `backend/app/models/<feature>.py`.
- The generated files (`openapi.json`, `schema.d.ts`) are the only shared hot spots. On a merge conflict there, do not hand-merge: take either side, run `make gen`, commit.
- Migrations: two branches that each add a migration produce two heads. See [Database](05-database.md#two-heads-after-a-merge).

## Handy commands

| Command | Use |
|---|---|
| `make help` | list targets |
| `cd backend && uv run pytest -k notes -x` | run some backend tests |
| `cd frontend && npx vitest` | frontend tests in watch mode |
| `cd backend && uv add httpx` / `cd frontend && npm install zod` | add a dependency (commits the lockfile change) |
| `docker compose logs -f db redis` | infra logs during `make dev` |
