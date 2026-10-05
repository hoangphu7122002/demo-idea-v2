# 3 · Background jobs (Celery + Redis)

Redis is the broker and result backend. Celery workers run the same code and image as the API.

## Add a task

1. Write it in `backend/app/worker/tasks.py`:

```python
@celery_app.task(name="app.worker.tasks.export_notes")
def export_notes(job_id: str) -> None:
    with SyncSessionLocal() as s:
        job = s.get(Job, uuid.UUID(job_id))
        if job is None or job.status == "done":
            return
        job.status = "running"
        s.commit()
        job.result = {"rows": 42}
        job.status = "done"
        s.commit()
```

2. Enqueue it from a route, using the `Job` id as the Celery task id so both are traceable:

```python
job = Job(kind="export_notes")
session.add(job)
await session.commit()
export_notes.apply_async(args=[str(job.id)], task_id=str(job.id))
return JobAccepted(job_id=job.id, status=job.status)
```

3. The frontend polls `GET /api/jobs/{job_id}` until `status` is `done` or `failed` (see `frontend/src/features/notes/summary.ts`).

## Rules

| Rule | Why |
|---|---|
| Tasks take ids, not objects | args go through JSON; load fresh rows inside the task |
| Make tasks idempotent (skip if already `done`) | `task_acks_late=True` means a task can run again after a worker crash |
| Use the sync DB session (`SyncSessionLocal`) in tasks | Celery tasks are sync; the API uses the async engine |
| Name LLM tasks `llm_*` | they route to the `llm` queue (`celery_app.py`), so slow LLM calls never block quick jobs |
| Store progress and results on the `Job` row | the API and UI read status from the DB, not from Celery |
| Retry transient failures explicitly | tasks don't auto-retry; add `autoretry_for=(httpx.HTTPError,), retry_backoff=True, max_retries=3` to `@celery_app.task` for calls that can hit rate limits |

## Queues and scaling

| Queue | For | Dev | Prod-like (`make up`) |
|---|---|---|---|
| `default` | quick jobs | one worker, `--pool=solo` | 2 workers × concurrency 2 |
| `llm` | LLM calls | same worker | same workers; split into a dedicated service when LLM volume grows |

To give the `llm` queue its own workers, copy the `worker` service in `compose.yml` to `worker-llm` with `-Q llm` and the concurrency you want, and change the original to `-Q default`.

## Scheduled tasks

Add a schedule to `celery_app.conf.beat_schedule` in `backend/app/worker/celery_app.py`, then add one compose service running exactly one beat process:

```yaml
  beat:
    <<: *app
    profiles: ["app"]
    command: ["celery", "-A", "app.worker.celery_app", "beat", "--loglevel=INFO"]
```

Run beat in dev only when you need it: `cd backend && uv run celery -A app.worker.celery_app beat`.

## Debug

| Question | Command |
|---|---|
| Is the worker connected? | look for `ready.` in the `make dev` output |
| What is a job doing? | `curl localhost:8000/api/jobs/<id>` |
| Queue length (prod-like) | `docker compose exec redis redis-cli llen llm` |
| Run a task inline in a test | patch `apply_async`, then call the task body with `.run(...)`, e.g. `llm_summarize_note.run(job_id, note_id)` (see `tests/test_summary.py`) |

macOS note: in dev the worker runs with `--pool=solo` (fork-based pools misbehave on macOS). Containers use the default pool.
