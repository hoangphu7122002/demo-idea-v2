# 7 · New project from this template

## 1. Copy it (from git, never by copying the folder)

On GitHub: **Use this template → Create a new repository**, then clone your new repo.
Or from the command line:

```sh
git clone --depth 1 git@github.com:bachtly/lean-web-stack.git myapp
cd myapp
./scripts/new-project.sh myapp
```

`new-project.sh` sets the project name (Docker project, image names, API title) in `.env.example`, resets git history to one fresh commit, and removes the template's `origin` remote. Copying a working folder instead drags along `.venv` and `node_modules` with stale absolute paths.

## 2. Point it at your repo

```sh
git remote add origin git@github.com:<you>/myapp.git
git push -u origin main
```

## 3. Install and verify

```sh
make setup
make check
make dev
```

## 4. Rebrand the UI

Edit `frontend/src/app/theme.ts` (palette for light and dark, font, corner radius) and the title in `frontend/index.html` and `frontend/src/components/layout/AppShell.tsx`. Components use theme tokens, so nothing else changes. See [Frontend](09-frontend-ui.md#7-dark-mode-and-theming).

## 5. Remove the examples when you're ready

The notes, summary and chat features are working references. Keep them until your first real feature works, then delete them:

| Remove | Files |
|---|---|
| Notes + AI summary | `frontend/src/pages/NotesPage*.tsx`, `backend/app/api/routes/notes.py`, `backend/app/models/note.py`, `backend/app/ai/summary.py`, `llm_summarize_note` in `backend/app/worker/tasks.py`, `backend/tests/test_notes.py`, `backend/tests/test_summary.py`, `frontend/src/features/notes/` |
| Chat | `backend/app/api/routes/chat.py`, `backend/app/ai/agents.py`, `backend/tests/test_chat.py`, `frontend/src/features/chat/`, `frontend/src/pages/ChatPage.tsx` |
| Demo job | `word_stats` in `tasks.py` and its route in `backend/app/api/routes/jobs.py` (keep `GET /api/jobs/{id}` and the `Job` model) |

Then:
1. Unregister the routers in `backend/app/api/main.py` and the imports in `backend/app/models/__init__.py`.
2. Frontend: remove the routes in `src/app/router.tsx`, the links in `NAV_LINKS` (`src/components/layout/AppShell.tsx`), `notesFilterSlice` in `src/app/store.ts`, and the `'Note'` tag in `src/services/baseApi.ts`. Keep `src/app/`, `src/components/`, `src/hooks/`, `src/services/` and `src/test/`.
3. Add a migration that drops the `notes` table (`alembic revision --autogenerate`).
4. Run `make gen` and `make check`.

## Keeping your project current

Projects copied from the template do not receive later template fixes. To pull one in, read the template's commit and apply the same change.
Dependency upgrades are per project:

```sh
cd backend && uv lock --upgrade && cd ..
cd frontend && npx npm-check-updates -u && npm install && cd ..
make check
```
