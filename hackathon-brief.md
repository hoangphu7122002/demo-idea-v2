# Hackathon brief: A technical knowledge blog with community contributions

## Context

I need a personal blog for sharing in-depth technical knowledge (long posts, math, code, illustrations, post series), and I will keep using it after the hackathon. The blog is not read-only: other people must be able to discuss, give feedback and contribute, so the content gets better over time.

## Problems (starting points for research, to be verified)

1. Technical authors stop writing: it takes time, perfectionism, fear of being wrong, not knowing whether anyone reads, slow feedback.
2. Reader feedback rarely makes a post better; comments sink to the bottom of the page or drown in spam.
3. Technical knowledge goes stale fast; readers can't tell which posts are still correct.
4. Long technical content is hard to follow, hard to find again, and hard to know whether you understood it.
5. No mechanism for reputation or credit for quality contributors.

## Brief

Build a technical blogging platform with everything a real blog needs, where authors, readers and contributors improve the content together. Do your own research to verify the problems above, find the gaps existing solutions don't solve, then pick **one differentiator** as the demo core. The differentiator must be technically challenging (not just CRUD).

## Full feature map (the roadmap lists ALL of these)

The roadmap is the **whole product**, not only the demo. Every feature below gets an `F<n>` entry with dependencies and waves. The demo is one milestone (`M1`) that picks a subset; it does not decide what is in the roadmap.

| Group | Features |
|---|---|
| Platform | Sign-in and roles (guest, member, author/admin); bilingual UI and posts (EN + VI, one post with two language versions); one-command local start; deploy |
| Authoring | Draft, preview, publish and edit posts; Markdown/MDX with code, math (KaTeX) and illustrations; series and categories; create content by voice |
| Reading | Search; comfortable reading on desktop and mobile; follow new content; freshness / "may be outdated" label |
| Community | Discussion; inline suggestions on a text span; approve → credited revision; reputation and credit for contributors |
| Moderation | Spam filtering (rules + LLM); author review queue |
| New-finding service | Scheduled ingest from followed sources plus links the author saves by hand; filter and rank (relevance, novelty vs what the author knows or wrote, source quality, no duplicates or hype); daily digest of 2–3 items in EN + VI (what's new, why it matters, summary, source link); author feedback (useful / already known / skip) tunes ranking; one click turns an item into a draft post or TIL; flags posts a new release makes outdated |
| Sharing | Turn a post into a short motion video |
| Seed data | A few real posts and several fake users to demo interaction between roles |

Topics: **AI** (applied + deep research) and **System Design / Architecture** (author's path: AI Solution Engineer).

### Content sources

- Followed sources for the new-finding service and references (link + summary, never copied verbatim): **Lil'Log** (https://lilianweng.github.io), **Knowbie** (https://knowbie.vercel.app), plus tech blogs, newsletters, release notes, papers and YouTube channels chosen during research. Facebook pages can't be crawled (login wall, ToS).
- Importing third-party posts as seed content requires checking their license first.

## Scope

- **Roadmap:** the full feature map above, as features `F<n>` with dependencies and parallel waves.
- **Demo milestone (M1):** the differentiator core plus the minimum blog working end-to-end, chosen by demo-scope based on time and risk. At minimum it starts locally with one command; local or deployed is demo-scope's call.

## Technical constraints

- Base: this repo (`demo-idea-v2`, from the `lean-web-stack` template).
- Read-only references (never modify, re-implement here instead of copying): `~/Downloads/banhloc-be-anh`, `~/Downloads/ott-chat`, and `~/demo-idea` (v1: MDX render, inline suggestion popup, moderation panel, approve → revision, app stack, test-DB isolation).
- Repo has a GitHub remote and `gh auth` works (real PRs).
- **Model choice:** every spawned agent or teammate picks its model by task difficulty: lookup, polling, running tests, formatting → cheapest model; implementation → mid-tier model; architecture, review, critic → strongest model. Spawn an agent team only when the work is truly parallel.

## Process

1. `/bach:demo-scope hackathon-brief.md` → research, decide, demo script, cut, spec, and `roadmap.md` (full feature map, demo = M1).
2. For each feature, with the human working alongside the lead in the Claude CLI (tmux):
   `/bach:pr-team <run>/roadmap.md#F<n> review: on-demand`.
   Features in the same wave may run in parallel, one tmux session each.
3. After a feature's PRs are merged, mark it ✅ in `roadmap.md` and move to the next.

## What to log

- `workflow-log.md`, per feature: start/end time, PRs opened/merged, review rounds, problems and suggested improvements for the plugin (demo-scope, pr-team).
- Key decisions and why: `docs/decisions/`.
