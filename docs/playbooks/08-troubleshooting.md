# 8 · Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `make dev` / `make check`: `port is already allocated` or `address already in use` | another app uses the port | change it in `.env` (see [ports](00-first-day.md#ports)); for DB/Redis also update `DATABASE_URL` / `REDIS_URL` |
| `Cannot connect to the Docker daemon` | Docker Desktop not running | start Docker Desktop, wait for `docker info` to succeed |
| pytest: `connection refused` / `database "app_test" does not exist` | db container not up, or the volume was created before `init-test-db.sql` existed | `make check` starts db + redis first; otherwise `docker compose down -v` and retry |
| Vite or vitest crash on start with a Node version error | Node 22.11 or older with newer Vite/vitest/jsdom | upgrade Node to 22.12+, or keep the pins in `frontend/package.json` (Vite 6, vitest 3, jsdom 26) |
| eslint: `… was removed in MUI v9`, `Raw colour`, `Use the sx prop`, `'@mui/material' import is restricted` | old MUI API or styling outside the theme | see the fix table in [Frontend](09-frontend-ui.md#8-guardrails) |
| `tsc`: `Property 'InputProps' does not exist` (or another `*Props`) | MUI v9 removed it | use `slotProps`, see `frontend/CLAUDE.md` |
| Test fails with `could not find react-redux context`, `useSnackbar` undefined, or a date picker error | rendered without the providers | use `renderWithProviders` / `renderApp` from `src/test/render.tsx` |
| Mutation succeeds but the list doesn't update | missing tags | query `providesTags` and mutation `invalidatesTags` must share a tag listed in `tagTypes` (`src/services/baseApi.ts`) |
| Refreshing `/notes` on the prod build returns 404 | server not falling back to `index.html` | the shipped `nginx.conf` already does; keep `try_files ... /index.html` if you change it |
| Worker logs nothing or hangs on macOS | fork-based pool | dev already uses `--pool=solo`; keep it |
| Job stays `queued` | no worker, or wrong queue | check the worker output says `ready.`; LLM tasks must be named `llm_*`, and the worker must listen on `-Q default,llm` |
| CI `contract` job fails | API changed without `make gen` | `make gen`, commit `backend/openapi.json` and `frontend/src/api/schema.d.ts` |
| Merge conflict in `schema.d.ts` / `openapi.json` | both branches changed the API | take either side, `make gen`, commit |
| `alembic upgrade head`: multiple heads | two branches added migrations | see [Database](05-database.md#two-heads-after-a-merge) |
| Chat stops after about 60 s behind a proxy | proxy buffering or idle timeout | keep `X-Accel-Buffering: no`; raise the proxy / load balancer idle timeout to at least 300 s |
| `429 rate limited` from `/api/chat` | Redis rate limit (30 requests/min per client) | wait, or adjust `allow()` in `backend/app/ai/limits.py` |
| `make up` hangs at the `/ready` wait | migrate failed, or api unhealthy | `docker compose --profile app logs migrate api` |
| Real model errors with `unknown model` or an auth error | provider extra or key missing | `uv add 'pydantic-ai-slim[anthropic]'`; set the key in `.env` ([AI agents](04-ai-agents.md)) |
