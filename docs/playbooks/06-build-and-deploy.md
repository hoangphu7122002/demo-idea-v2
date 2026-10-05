# 6 · Build and deploy

## Artifacts

| Artifact | Built from | Runs as |
|---|---|---|
| backend image `<PROJECT_NAME>-backend` | `backend/Dockerfile` (multi-stage, uv) | **migrate**: `alembic upgrade head` · **api**: `uvicorn` on 8000 · **worker**: `celery ... worker -Q default,llm` |
| web image `<PROJECT_NAME>-web` | `frontend/Dockerfile` (Vite build → nginx) | static files + `/api` proxy to `api:8000`, streaming-safe (`proxy_buffering off`) |

One backend image for all three roles means the API and workers always run the same code version.

## Prod-like run on your machine

```sh
make up
```

It builds both images, starts db, redis, migrate (one-shot), api, 2 workers and web, then waits for `/ready`.
Open `http://localhost:8080` (`APP_PORT`). Stop with `make down`; add `-v` to the underlying command (`docker compose --profile app down -v`) to also wipe the data volume.

More workers: `docker compose --profile app up -d --scale worker=4`.

## CI/CD (`.github/workflows/ci.yml`)

On a PR: the backend, frontend and contract jobs (path-filtered).
On push to `main`:
1. Build and push `ghcr.io/<owner>/<repo>/backend:<sha>` and `.../web:<sha>`, with the GitHub Actions layer cache.
2. `deploy.sh <sha>` (job `deploy`, GitHub environment `production`).

`deploy.sh` is a placeholder. Fill it in for your target, keeping this order:
1. run the backend image once with `alembic upgrade head` (migrate),
2. roll out **api** and **worker** with the same `<sha>` tag,
3. roll out **web**,
4. roll back by redeploying the previous `<sha>`.

## Where to run it

| Stage | Setup | Scale by |
|---|---|---|
| 0 · one VM | this `compose.yml` on a VM + Caddy/nginx for TLS; managed backups | `--scale worker=N` |
| 1 · managed containers (recommended) | AWS ECS Fargate (or Cloud Run / Fly / Render); RDS Postgres; ElastiCache Redis; web as static files on S3 + CloudFront, or the web image | API on CPU/requests; workers on **queue length** |
| 2 · Kubernetes | EKS/GKE + Helm | HPA for the API; KEDA on Redis list length for workers (down to zero) |

Most apps stay at stage 1: the real ceiling is usually the LLM provider's rate limit, not your containers.

## Production checklist

- [ ] Secrets (`ANTHROPIC_API_KEY`, DB password) from the platform's secret store, not baked into images
- [ ] `DATABASE_URL` / `REDIS_URL` point at managed services; PgBouncer in front of Postgres once API + worker replicas exceed about 50 connections
- [ ] Load balancer health check on `/health`, readiness on `/ready`
- [ ] Load balancer / CDN idle timeout of at least 300 s for SSE chat
- [ ] Graceful shutdown: uvicorn `--timeout-graceful-shutdown 30`; Celery workers get a stop grace period of at least the longest task
- [ ] Migrations follow expand → contract (see [Database](05-database.md#safe-migrations-in-production))
- [ ] Logs and traces: Logfire / OpenTelemetry, including LLM token usage
