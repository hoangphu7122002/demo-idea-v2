# pr-team plan · F2 · Markdown rendering with code highlight, KaTeX, paragraph ids

Source: roadmap.md#F2 · AC: B2.1–B2.4 (spec.md). F1 plan archived in plan-F1.md.

## Design
- Backend stores a post as ordered **paragraph blocks** (`post_paragraphs`: id, post_id, position, md). Stable `paragraph_id` = DB id string (e.g. `p-<n>`), assigned when the post is created/seeded, never recomputed. F3 sends these ids to Claude, F6 edits one block by id.
- API returns `{slug, title, paragraphs: [{id, md}]}`. Frontend renders each block with react-markdown + remark-gfm + remark-math + rehype-katex + rehype-highlight inside `<section id={id}>` → DOM id == backend id by construction (B2.2, B2.3).
- Seed: one demo post fixture (code blocks + inline/display math) as a seeder module; real D1 wording can replace the fixture text later without code changes.

## Shape
Vertical 1 step on backend (model → api/seed), frontend renderer in parallel from the start; page task last (needs api contract + renderer).

## Tasks
| id | folder | files | blockedBy | flag | owner | PR | state | size | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| post-model | backend | app/models/post.py (Post, PostParagraph), app/models/__init__.py, migrations/versions/<new>.py, app/posts/blocks.py (split markdown → blocks: paragraphs, headings, code fences, lists, $$ math kept whole), tests/test_blocks.py | – | – | builder-1 | #5 | merged (pre-review ok, after merge) | big (migration) | reviewer-pr5 |
| post-seed | backend | app/seed/posts.py, app/seed/fixtures/llm-api-post.md, tests/test_seed_posts.py | post-model | – | builder-1 | #6 | merged | small (seed + fixture, tests) | – |
| post-api | backend | app/api/routes/posts.py (GET /api/posts, GET /api/posts/{slug}), app/api/main.py, tests/test_posts.py, openapi.json + frontend/src/api/schema.d.ts (generated) | post-model, post-seed | – | builder-1 | #7 | merged (pre-review ok @d0d65a9, after merge) | big (API contract) | reviewer-pr7 |
| md-render | frontend | package.json + lock (react-markdown, remark-gfm, remark-math, rehype-katex, rehype-highlight, katex), src/features/posts/PostBody.tsx (props: paragraphs[]), src/features/posts/PostBody.test.tsx, styles (720px col, 18px, lh 1.6, katex + highlight css) | – | – | builder-2 | #4 | merged (mid pre-review) | big (md→HTML, 6 deps, no browser check) | reviewer-pr4 (no blockers; nits → #5 seed, #8 page) |
| post-page | frontend | src/features/posts/postsApi.ts, src/pages/PostPage.tsx, src/app/router.tsx (`/posts/:slug`), nav link, src/pages/PostPage.test.tsx | post-api, md-render | – | builder-2 | #8 | merged (mid pre-review) | big (new page + global theme.ts change) | reviewer-pr8 (no blockers; theme colours only used by PostBody) |

AC per task:
- post-model: migration up/down clean; splitter test: fenced code with blank lines and `$$…$$` stay one block; ids stable across reload.
- post-seed: reseed creates the demo post with ≥8 blocks incl. ≥1 code block (python) and ≥1 math block; idempotent.
- post-api: 200 with ordered paragraphs, 404 unknown slug; contract regenerated.
- md-render: test renders fixture → each block has `id` = paragraph id, code has highlight classes, math renders `.katex`; typography per B2.4.
- post-page: `/posts/<seed-slug>` renders seeded post in browser (screenshot in PR); loading/error states via QueryState.

## Team
- builder-1 → `backend` (post-model → post-seed → post-api)
- builder-2 → `frontend` (md-render → post-page) — reassigned from repo-root
- pr-watcher: 1 · reviewers: on-demand, max_reviewers 3
- Expected big PRs: post-model (migration), post-api (contract), md-render? (deps only, no page) , post-page (visible page)

## Review
- mode: on-demand · max_reviewers: 3 · review budget: 3 (kept from F1)

## Language
- Operator-facing text (lead + all teammates): Vietnamese. Code, commits, PRs, agent-to-agent: English.

## Backlog (nits, not in F2)
- blocks.py: unclosed `$$` swallows rest of post into one block; setext headings (`Title\n===`) not split. Seed fixture avoids both; fix when authoring lands (F15). (reviewer-pr5)
