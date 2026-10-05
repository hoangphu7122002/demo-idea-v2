# 2 · Add a feature (vertical slice)

A vertical slice goes through every layer in one branch. The built-in **"Summarise a note with AI"** feature is the reference: copy its shape.

```
UI button ─► POST /api/notes/{id}/summary ─► Job row (queued) ─► Celery task on "llm" queue
   ▲                     │ 202 + job_id                                 │ runs summary agent
   └── polls GET /api/jobs/{job_id} ◄────────────── Job row (done) + Note updated
```

## Steps

| # | Layer | Do | Reference file |
|---|---|---|---|
| 1 | Branch | `git switch -c feat/<name>` | |
| 2 | Model | add columns or a table | `backend/app/models/note.py`, `job.py` |
| 3 | Migration | `cd backend && uv run alembic revision --autogenerate -m "<what>"`, review it, `uv run alembic upgrade head` | `backend/migrations/versions/afad6ea87a2a_note_summary_fields.py` |
| 4 | AI | agent with `output_type` = a Pydantic model, plus an offline model for dev and tests | `backend/app/ai/summary.py` |
| 5 | Worker | task that loads the row, runs the agent, stores the result, updates the job; idempotent | `backend/app/worker/tasks.py` → `llm_summarize_note` |
| 6 | API | route that validates, creates a `Job`, enqueues, returns `202` + `job_id` | `backend/app/api/routes/notes.py` → `summarise_note` |
| 7 | Backend tests | agent (incl. invalid output → retry), task, route | `backend/tests/test_summary.py` |
| 8 | Contract | `make gen` | `frontend/src/api/schema.d.ts` |
| 9 | Frontend data | RTK Query endpoints over the typed client (`fromApi`); job polling in a plain function called from a mutation | `frontend/src/features/notes/notesApi.ts`, `summary.ts` |
| 10 | Frontend UI | page + lazy route, MUI with `sx` + theme tokens, forms via Zod + `Form*` inputs in `FormDialog` ([Frontend](09-frontend-ui.md)) | `frontend/src/pages/NotesPage.tsx`, `features/notes/NoteItem.tsx`, `NoteFormDialog.tsx` |
| 11 | Frontend test | `renderApp(path)` / `renderWithProviders` with `api.GET` / `api.POST` mocked | `frontend/src/pages/NotesPage.test.tsx`, `features/notes/NoteItem.test.tsx` |
| 12 | Gate | `make check` | |
| 13 | Prod-like run | `make up`, try it at `http://localhost:8080`, `make down` | |
| 14 | PR | one commit (or a few), conventional message | |

## Sync or async?

| The work… | Do it |
|---|---|
| takes under about 1 s and the user waits for it | inline in the route |
| streams tokens to the user (chat) | in the API process, as SSE (see `backend/app/api/routes/chat.py`) |
| takes longer, calls an LLM without streaming, or runs in batches | a Celery task + `Job` row + polling (this example) |
| runs on a schedule | a Celery beat task (see [Background jobs](03-background-jobs.md#scheduled-tasks)) |

## Checklist before the PR

- [ ] Migration reviewed (autogenerate misses some changes, such as renames and server defaults)
- [ ] `make gen` run and generated files committed
- [ ] Offline model covers the new agent, so tests never need an API key
- [ ] Task is idempotent (a retry must not double-apply)
- [ ] New screens checked in light and dark mode
- [ ] `make check` green
- [ ] Tried once with `make up` if you touched Docker, nginx or worker config
