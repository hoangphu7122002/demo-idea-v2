# 5 · Database (Postgres + SQLAlchemy + Alembic)

- Postgres 16 with pgvector (`pgvector/pgvector:pg16`), in Docker.
- SQLAlchemy 2 with psycopg 3. One URL serves the async engine (API) and the sync engine (Celery tasks), see `backend/app/core/db.py`.
- Tests use a separate database `app_test`, created by `backend/scripts/init-test-db.sql` on the first start of the db container. Tables are recreated per test.

## Change the schema

```sh
cd backend
uv run alembic revision --autogenerate -m "add tags to notes"
uv run alembic upgrade head
```

Always open the generated file in `backend/migrations/versions/` and review it. Autogenerate misses or mis-reads:
- column and table **renames** (it emits drop + add, which loses data),
- server defaults, enum changes, some index changes,
- data migrations (write those yourself with `op.execute`).

## Common commands

| Task | Command (from `backend/`) |
|---|---|
| apply all | `uv run alembic upgrade head` |
| undo the last one | `uv run alembic downgrade -1` |
| where am I | `uv run alembic current` |
| history | `uv run alembic history` |
| SQL shell | `docker compose exec db psql -U app app` |
| reset local data | `docker compose down -v` (deletes the volume), then `make dev` |

## Two heads after a merge

Two branches that each add a migration leave two heads; `upgrade head` then fails with "multiple heads". Fix it on main:

```sh
cd backend
uv run alembic heads
uv run alembic merge -m "merge heads" <rev1> <rev2>
uv run alembic upgrade head
```

## Safe migrations in production

Deploys run `migrate` before the new `api` and `worker` start, while old containers may still be running. Keep each migration backward-compatible:
1. **Expand**: add nullable columns or new tables; deploy code that writes both.
2. **Contract**: in a later release, drop the old columns once nothing reads them.

## pgvector

The extension is available in the image. Enable it in a migration with `op.execute("CREATE EXTENSION IF NOT EXISTS vector")`, then use `pgvector.sqlalchemy.Vector(dim)` columns. It handles RAG up to tens of millions of vectors before you need a dedicated vector DB.
