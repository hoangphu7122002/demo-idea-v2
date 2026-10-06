# pr-team plan · F1 · One-command local start + reseed

Source: scope/2026-10-05-tech-blog-correctness/roadmap.md#F1 · AC: spec.md "Done when" → "App starts locally with one command"; backs B4.5 "Reset demo" (F6).

## Shape
Vertical 1 step: `seed-cli` (contract: seeder registry + `python -m app.seed`) first, then `demo-reset-api` and `one-command-start` in parallel (disjoint folders).
No Post model exists yet (F2) → F1 ships the mechanism + a notes seeder as example; F2 / D1 register post fixtures via the registry.

## Tasks
| id | folder | files | blockedBy | flag | owner | PR | state | size | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| seed-cli | backend | app/seed/__init__.py (registry, `reseed(session)`: truncate seeded tables + load in order), app/seed/__main__.py (`python -m app.seed`), app/seed/notes.py (example seeder), tests/test_seed.py | – | – | builder-1 | #1 | merged | small | – |
| demo-reset-api | backend | app/core/settings.py (`demo_mode: bool = False`), app/api/routes/demo.py (`POST /api/demo/reset` → reseed, 404 when demo_mode off), app/api/main.py (include router), tests/test_demo.py, openapi.json + frontend/src/api/schema.d.ts (generated, shared contract file; CI contract job requires it) | seed-cli | DEMO_MODE | builder-1 | #2 | merged (mid pre-review) | big (API contract) | reviewer-pr2 (no blockers, 2 nits) |
| one-command-start | repo root | Makefile (`make demo`: setup if needed → db+redis up → migrate → seed → api+worker+web), stack.toml (template build adds `uv run python -m app.seed`), .env.example (`DEMO_MODE=1`), README.md (quick start) | seed-cli | – | builder-2 | #3 | merged | small (21 lines, root config; operator smoke) | – |

AC per task:
- seed-cli: `uv run python -m app.seed` idempotent (run twice → same rows); test asserts reseed restores state after mutation; ruff/mypy/pytest green.
- demo-reset-api: reset returns 200 + counts when DEMO_MODE=1, 404 otherwise; test both; openapi.json regenerated.
- one-command-start: fresh clone `make demo` brings up api + web + seeded DB; `make help` lists it; `stack template refresh` works with seed step.

## Team
- builder-1 → folder `backend` (seed-cli, then demo-reset-api)
- builder-2 → folder `.` root files only (one-command-start); spawned after PR #1 merged
- reviewers: none standing (review: on-demand, max_reviewers = 3)
- pr-watcher: 1

## Review
- mode: on-demand · max_reviewers: 3
- review budget (open PRs): 3 (operator, 10:52)

## Language
- Operator-facing text (lead + all teammates): Vietnamese. Code, commits, PRs, agent-to-agent messages: English. Include in every new spawn prompt.

## Lifecycle
- Operator: fresh builders per feature (respawn at feature start); pr-watcher stays.
