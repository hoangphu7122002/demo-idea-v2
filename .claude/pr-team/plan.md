# pr-team plan · F3 · Check post against release note (LLM flags outdated paragraphs)

Source: roadmap.md#F3 · AC: B1.1–B1.5 (spec.md). Earlier plans: plan-F1.md, plan-F2.md.

## Design
- `POST /api/posts/{slug}/check` body `{release_url?: str, release_text?: str}` → resolve release text → run PydanticAI agent with structured output `list[Flag{paragraph_id, reason, source_quote, proposed_fix}]` over the post's `[{id, md}]` → persist a `ReleaseCheck` + its `ParagraphFlag`s → return them. `GET /api/posts/{slug}/flags` returns flags of the latest check (F4/F5/F6 read this).
- **No live fetch on stage** (B1.1): release URLs resolve from a local map `app/releases/fixtures/` (URL → cached release text). Pasted text works for any release.
- **Fallback** (B1.4): cache keyed `sha256(post paragraphs + release text)` stored as JSON under `app/releases/fixtures/cache/`. Live call has a timeout; on error/timeout/offline → cached response in ≤2 s, same flag ids and count. `LLM_MODEL=test` (default, offline) always uses the cache. A `python -m app.releases.record` CLI writes the cache from one live run (operator runs it once with a key).
- Sync HTTP request (no Celery job): UI shows a spinner; live ≤20 s (B1.5).
- Ids returned are the existing `p-<id>` paragraph ids (B2.3 mapping).

## Tasks
| id | folder | files | blockedBy | flag | owner | PR | state | size | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| flag-model | backend | app/models/release_check.py (ReleaseCheck: id, post_id, source_url, release_hash, model, created_at; ParagraphFlag: id, check_id, paragraph_id FK, reason, source_quote, proposed_fix), models/__init__.py, migration, tests/test_flag_model.py | – | – | builder-1 | PR #11 | merged | big (migration) | reviewer-pr11 (ok) |
| release-source | backend | app/releases/__init__.py (`resolve(url?, text?) -> ReleaseSource`), app/releases/fixtures/<release>.md + index.json (URL → file), tests/test_releases.py | – | – | builder-1 | PR #9 | merged | small (resolver + fixture) | – |
| check-agent | backend | app/ai/release_check.py (agent, prompt, `check(paragraphs, release) -> list[Flag]` with timeout + cache fallback), app/releases/cache.py, app/releases/record.py (CLI), app/releases/fixtures/cache/<key>.json (demo cache), tests/test_release_check.py (FunctionModel: live ok, live error → cache, offline → cache) | release-source | – | builder-1 | PR #12 | merged (mid pre-review) | big (LLM path, API key, new dep, runtime cache writes) | reviewer-pr12 |
| check-api | backend | app/api/routes/posts.py or new routes/checks.py, app/posts/service.py, tests/test_check_api.py, openapi.json + frontend/src/api/schema.d.ts (generated) | flag-model, check-agent | – | builder-1 | PR #13 | fix round (operator: logic out of controller, docstrings); ok @205ed67 stale after push | big (API contract, ~330 lines) | reviewer-pr13 |
| check-panel | frontend | src/features/checks/CheckPanel.tsx (URL or text input, Check button, spinner, error) + CheckResults.tsx (list: paragraph link #p-N, reason, quote, fix), tests | – | – | builder-2 | PR #10 | merged (mid pre-review) | big (form UI, jsdom only, test-timeout change) | reviewer-pr10 |
| check-wire | frontend | src/features/checks/checksApi.ts (mutation + flags query), PostPage.tsx (mount panel, click result scrolls to #p-N), tests, screenshots | check-api, check-panel | – | builder-2 | PR #16 | merged (mid pre-review) | big | reviewer-pr16 |
| cache-hardening | backend | app/releases/cache.py, app/ai/release_check.py, tests (atomic write, corrupt=miss, prompt delimiters, no empty overwrite, verbatim quote filter) | – | – | builder-1 | PR #14 | merged (after pre-review ok) | big (fixes post-merge blocker, LLM input sanitising) | reviewer-pr14 |
| llm-providers | backend | pyproject.toml, uv.lock, release_check.py + record.py docstrings, backend/README.md, tests (Anthropic/OpenAI/Gemini via LLM_MODEL) | cache-hardening | – | builder-1 | PR #15 | merged (mid pre-review) | big (new deps, websockets downgrade) | reviewer-pr15 |
| check-hardening-2 | backend | release_check.py (tag escape, min quote, cache-path id filter), backend .gitignore (*.tmp), tests | llm-providers, resource-rename-backend | – | builder-1 | PR #18 | merged (after pre-review ok) | big (LLM input sanitising) | reviewer-pr18 |
| resource-rename-backend | backend | app/releases→app/resources, release_check.py→resource_check.py, ResourceCheck model, migration rename table/column, API accepts resource_* + deprecated release_*, contract regen | – | – | builder-1 | PR #17 | merged; post-merge checks ok on main 8c792ce | big (migration + contract, 36 files) | reviewer-pr17 |
| resource-rename-frontend | frontend | features/checks (label "Check against a resource"), checksApi payload resource_*, tests, screenshots | resource-rename-backend, check-wire | – | builder-2 | PR #19 | merged (after pre-review ok) | big (visible page change; small diff) | reviewer-pr19 |
| resource-rename-cleanup | backend | drop release_* API fields, contract regen | resource-rename-frontend | – | builder-1 | PR #20 | merged (after pre-review ok) | big (contract removal; small diff) | reviewer-pr20 |

AC per task:
- flag-model: migration up/down clean; flag rows cascade with check and with post.
- release-source: demo URL resolves offline to fixture text; pasted text passes through; unknown URL → clear 422 error (no network).
- check-agent: tests prove live path, error → cache, offline → cache with identical flag ids/count; cache served ≤2 s; demo cache for seeded post + demo release has ≥3 flags (B1.3) — operator records it live once; until then a hand-checked cache file.
- check-api: 200 with flags, persisted; GET flags returns latest; 404 unknown slug; contract regenerated.
- check-panel: URL or text required; spinner while pending; renders flags list; tests.
- check-wire: in browser, demo URL → Check → ≥3 flags listed, click scrolls to paragraph; screenshots.

## Shape
Backend vertical: release-source → check-agent; flag-model in parallel (different files, same builder → serial). Frontend: check-panel now (props only), check-wire after check-api.

## Team
- builder-1 → backend (flag-model, release-source, check-agent, check-api)
- builder-2 → frontend (check-panel, check-wire)
- pr-watcher; reviewers on-demand (max 3); budget 3

## Open questions (operator)
- Demo release note: which real Anthropic release note? (decides the fixture + which seeded paragraphs become outdated)
- ANTHROPIC_API_KEY for the one live record run + B1.5 live path (not in .env now; `pydantic-ai-slim[anthropic]` dep added by check-agent)

## Language
- Operator-facing text (lead + all teammates): Vietnamese. Code, commits, PRs, agent-to-agent: English.

## Backlog
- blocks.py: unclosed `$$`, setext headings (reviewer-pr5) → F15.
- test_posts: pin 20 paragraphs; assert order by position directly (reviewer-pr7).
- cache-path flags not filtered against current paragraph ids (live path is) → do in #16 or next backend task (reviewer-pr13)
- test_check_api: assert persisted paragraph ids in DB (reviewer-pr13)
- release_check prompt: escape `</release_note>` inside release text; min quote length for verbatim check; gitignore `*.tmp` in fixtures/cache (reviewer-pr14)
- Gemini prefix is `google:` (not `google-gla:`) in the installed pydantic-ai (builder-1, PR #15)
- resource_check: zero-width / fullwidth look-alike tags; min-quote rule lets "a b c d" through (use chars AND words) (reviewer-pr18)
- test_check_api: stray release_url test should also assert flags = p-6, p-7, p-11 (reviewer-pr20)
