# Tech Blog Correctness: 2-day demo spec  (locked 2026-10-05 · code freeze Day 2, 16:00)

USER        Solo technical author (AI Solution Engineer) writing long AI + System Design posts on own blog
PROBLEM     "People asked us a lot how we'd keep the book up to date. We didn't really know."  (https://news.ycombinator.com/item?id=44812367, E017)
CORE JOB    A solo AI author can see which paragraphs a new release makes wrong, without rereading every post.
DIFFERENT   Unlike Giscus/Disqus, which put corrections in a thread at the bottom of the page, we anchor reader suggestions to the exact paragraph and flag sections a new release makes stale.
MVP TYPE    single-feature web app

Framing: author's own need; no "validated demand" claim (decision.md risk 1, G1 fail). Demo = roadmap milestone M1 only; full feature map lives in roadmap.md.

## Demo script
1. Hook (15 s): E017 quote on screen (solo author, HN 2025-08). Say: "Same for me: 20 deep AI posts, any release can quietly make one wrong."
2. Today (15 s): static mock of Hugo post + Giscus box at bottom; corrections land in comments/Twitter/email; only fix = reread every post, type "Updated:" note by hand; no stale signal.
3. Core action (45 s): paste real Anthropic/Claude release note URL (pre-cached) or text into "Check against release" → click Check → live Claude call (cached fallback) scans the one seeded LLM-API usage post.
4. Wow (30 s): exact paragraphs highlight amber with "May be outdated" badge + reason + release source link; post-level badge shows worst state; click the paragraph with seeded reader suggestion (others show AI-proposed fix) → inline diff → accept → text updates, "Updated <date>" marker, badge flips green "Verified", post badge updates.
5. Next (15 s): roadmap: auto-watch release feeds, reader span suggestions w/ credit, re-anchoring suggestions across edits (not built/faked in M1), changelog page, deploy + OAuth, new-finding digest.

## Build (≤ 14 h, ≤ 5 items) — total 12 h (user estimate)
| Item | Demo beat | Hours | Acceptance criteria (≤ 6) |
|---|---|---|---|
| B1 LLM flag of outdated statements vs pasted release note | 3, 4 | 5 | 1. "Check against release" accepts URL or pasted text (demo URL pre-cached, no live fetch on stage) and a Check button triggers it. 2. Backend sends post paragraphs + release text to Claude, returns list of {paragraph_id, reason, quoted source line, proposed fix}. 3. Seeded post + demo release yields ≥3 flagged paragraphs. 4. On API error/timeout/network off, cached response keyed post+release returned within 2 s with same flag ids and count as live path; UI identical. 5. Spinner shown during call; result renders ≤20 s live. |
| B2 Markdown post rendering w/ code highlight, basic KaTeX + paragraph ids | 3, 4 | 2 | 1. Seeded post renders from Markdown with syntax-highlighted code blocks and basic KaTeX math. 2. Every paragraph has stable DOM id matching backend paragraph_id. 3. Flagged paragraph ids from B1 map to visible paragraphs (no misses on demo fixture). 4. Reading column ≤720px, body 18px, line-height ≥1.6. |
| B3 Reader-visible freshness badge | 4 | 1.5 | 1. Flagged paragraph shows amber highlight + "May be outdated" badge. 2. Badge popover shows reason + release source link. 3. After accept, badge flips to green "Verified" without page reload. 4. Post-level badge reflects worst paragraph state. |
| B4 Accepted fix applies to post body | 4 | 2 | 1. Accept button on flagged paragraph (seeded reader suggestion or AI fix) persists new text to DB. 2. Paragraph text updates in place immediately. 3. "Updated <date>" marker appended to paragraph. 4. Reload shows updated text + marker (persisted). 5. "Reset demo" button restores seeded post state. |
| B5 Inline diff preview of fix vs original | 4 | 1.5 | 1. Before accept, popover shows whole old paragraph in `<del>` and new in `<ins>` (no word-level algorithm). 2. Diff visible on demo path for each flagged paragraph. 3. Light theme; diff text 18px, line-height ≥1.6, del/ins distinguishable by color + strike/underline. |

## Fake
| Item | Method |
|---|---|
| AI-drafted correction proposals | Carried in same Claude response; cached with it |
| Claim-level staleness extraction | Folded into flag prompt; part of live call + cache |
| Detect outdated code snippets/versions | Covered by LLM flag; live call + cache |
| Reader "Suggest edit" on highlighted text | One seeded suggestion on one flagged paragraph, W1 wording; other flags use AI fix |
| Author accept/decline/withdraw | Only Accept wired; others static |
| "Today" Hugo+Giscus view (beat 2) | Static screenshot/mock |
| Hook quote slide (beat 1) | Static slide |
| Seeded post | One realistic LLM-API usage post + one real Anthropic/Claude release note |

## Later (≥ 8) — all remain roadmap features (F<n> in roadmap.md), not dropped
Always-later: settings (configurable stale threshold) · dark mode / light+dark toggle · profile editing · email prefs · admin / moderation tools (hide, delete, block) · payments · mobile app · integrations (email/webhook notify, Git PR export, embeddable widget) · multi-tenant · i18n (bilingual EN + VI UI and posts)
Platform: sign-in + roles (guest, member, author/admin), OAuth reader identity · deploy (after local one-command start)
Authoring: Markdown editor w/ live preview · draft/preview/publish/edit flow · draft review mode · KaTeX math + illustrations · series and categories · create content by voice → draft · import posts from Markdown/repo · prose/terminology linting
Reading: TOC sidebar · post page TOC + anchored headings · search · comfortable mobile reading · follow new content (RSS / "what changed" feed, subscribe to post) · paragraph citation link · last-reviewed date · staleness banner after N days · per-post staleness score · staleness dashboard · outbound link checker · mark section superseded
Community: select-text inline comment · margin view · per-paragraph discussion thread · reactions/upvotes · anchors surviving edits + orphaned-anchor detection · reader outdated vote · report error flag · correction types taxonomy · proposal status for reader · notify proposer · reader credit on accepted correction · reputation + contributor profile/badge · anonymous suggestions · public changelog per correction · version history + restore · diff between versions
Moderation: spam filtering (rules + LLM) / rate limiting · author review queue · severity ranking · notification digest
New-finding service: scheduled ingest from followed sources (Lil'Log, Knowbie, blogs, newsletters, release notes, papers, YouTube) + hand-saved links · filter/rank (relevance, novelty, source quality, dedupe, no hype) · daily 2–3 item digest EN + VI · feedback (useful / known / skip) tunes ranking · one click item → draft post/TIL · auto-flag posts a new release makes outdated (auto-watch release feeds)
Sharing: post → short motion video
Data/analytics: paragraph analytics · per-post feedback counts · open data export (JSON/MD) · seed data with several fake users across roles

## Risk
Claude claim-vs-release contradiction check (D7) → 30-min spike first on seeded post + chosen release; fallback: cached response per seeded post+release, served on error/timeout/network off.

## Look & feel
Lil'Log-like clean: reading column ≤720px, body 18px, line-height ≥1.6, math/code first-class, TOC sidebar (Later), Google-Docs-style inline suggestion popovers; airy; light+dark toggle (toggle itself Later; demo in light). Reference screenshots: refs/lillog-post.png, refs/lillog-math.png (Lil'Log, lilianweng.github.io).

## Done when
- [ ] Beats 1–5 in ≤ 2 min, no code edits, no dev tools
- [ ] 3 rehearsals in a row pass
- [ ] Works with network off / API down (fallback)
- [ ] Backup video recorded
- [ ] ≥ 3 of 5 judging criteria (target: creativity, technical fit, growth path)
- [ ] App starts locally with one command

## Stack
lean-web-stack (this repo, demo-idea-v2) + React + MUI + Redux Toolkit + FastAPI + Postgres + PydanticAI (Claude); re-implement ideas from ~/demo-idea v1 (read-only: MDX render, suggestion popup, approve → revision).
