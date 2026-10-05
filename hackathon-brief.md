# Hackathon brief: A technical knowledge blog with community contributions

## Context

I need a personal blog for sharing in-depth technical knowledge (long posts, math, code, illustrations, post series), and I will keep using it after the hackathon. The blog is not read-only: other people must be able to discuss, give feedback and contribute, so the content gets better over time.

## Problems (starting points for research, to be verified)

1. Technical authors stop writing: it takes time, perfectionism, fear of being wrong, not knowing
  whether anyone reads, slow feedback.
2. Reader feedback rarely makes a post better; comments sink to the bottom of the page or drown in spam.
3. Technical knowledge goes stale fast; readers can't tell which posts are still correct.
4. Long technical content is hard to follow, hard to find again, and hard to know whether you understood it.
5. No mechanism for reputation or credit for quality contributors.



## Brief

Build a technical blogging platform with everything a real blog needs, where authors, readers and contributors improve the content together. Do your own research to verify the problems above, find the gaps existing solutions don't solve, then pick **one differentiator** as the demo core. The differentiator must be technically challenging (not just CRUD).

## Open ideas (optional; research may pick, change or drop them)

- Create content by voice: people share more easily when they speak than when they write
- Turn content into short motion videos with Claude Code for sharing



## Minimum requirements of a real blog

- Author: draft, preview, publish and edit technical posts; manage series and categories
- Reader: find, read and follow new content comfortably on desktop and mobile
- Community: multiple roles (guest, member, author/admin); discussion; content contributions;
credit for contributors; moderation and anti-spam
- **Bilingual:** every post and the UI in English and Vietnamese (one post, two language versions)
- **Topics:** AI (applied + deep research) and System Design / Architecture (author's path: AI Solution Engineer)
- **New-finding service (required):** the author falls behind without others updating them, so a
  service must deliver **2–3 new pieces of knowledge per day** on the two topics:
  - Ingest on a schedule from followed sources (tech blogs, newsletters, release notes, papers,
    YouTube channels; list in `scope/2026-10-03-dev-knowledge-blog/refs/sources.md`) plus links the
    author saves by hand (Facebook pages can't be crawled: login wall, ToS).
  - Filter and rank automatically: relevance to the topics, novelty versus what the author already
    knows or wrote, source quality; drop duplicates and hype.
  - Daily digest in EN + VI: what's new, why it matters, a short summary, source link.
  - Author feedback (useful / already known / skip) tunes the ranking; one click turns an item into a draft post or TIL.
  - Can feed the freshness signal: a new release flags posts whose claims it makes outdated.
- Seed data: a few real posts and several fake users to demo interaction between roles



## Scope

- Local or deployed, either is fine; demo-scope decides based on time and risk.
At minimum it must start locally with one command.
- Hackathon version: differentiator core + minimum blog working end-to-end. Everything else goes
to `v2.md` as the roadmap.



## Technical constraints

- Base: the `lean-web-stack` template
- Can refer `~/Downloads/banhloc-be-anh` and `~/Downloads/ott-chat`
(read-only, never modify)
- Repo has a GitHub remote and `gh auth` works (real PRs)
- **Agent cost:** every spawned agent or teammate picks its model by task difficulty:
lookup, polling, running tests, formatting → cheapest model; implementation → mid-tier model;
architecture, review, critic → strongest model. Spawn an agent team only when the work is truly parallel.

## Usage budget (hard limit)

The operator has limited weekly usage: **≤ 20% of the weekly limit for this whole project**.
Every agent, workflow and teammate must respect it.

| Phase | Budget | How |
|---|---|---|
| demo-scope | ~6–8% | Reuse the existing research run (`scope/2026-10-03-dev-knowledge-blog/`); resume from Step 2, don't redo Step 1 |
| pr-team (build hour 1) | ~10–12% | Max **2 builders**, 1 reviewer, 1 watcher on **Haiku**; review budget **3** open PRs |
| Focus Hour (build hour 2) | 0% now | Postponed until the weekly limit resets |

Rules when spawning:
- Ask before spawning more than 3 agents at once, or any extra Opus agent.
- Prefer Haiku/low effort for lookup, polling, extraction, formatting; Sonnet for code; Opus only for critic and PR review.
- Don't re-run a step whose output already exists; reuse files.
- Check `/usage` after each phase and log it; stop and ask the operator when a phase goes over its budget.



## Process

1. `/bach:demo-scope` → research, decide, demo script, cut, spec, plan. Log the time of each step.
2. **Build hour 1 (60 min), bach-workflow only:** `/bach:pr-team <spec>`. Focus Hour stays off
   (not even `--observe`: its hooks, system-prompt section and pane would change how pr-team runs).
   Run it in tmux (`teammateMode: "tmux"`): in a fresh VS Code terminal, `tmux new -s work`, then
   `claude`, then type the slash command at Claude's prompt (mouse on, so click a pane to focus it).
   Log start/end by hand; PR data comes from
   `gh pr list --state all --json number,title,createdAt,mergedAt,reviews`.
3. **Between hours:** merge or close every open PR so hour 2 starts from a clean `main`.
4. **Build hour 2 (60 min), Focus Hour:** `cd <repo> && focus init` → `/focus start --difficulty <1-5>` →
   build with focus workers → `/focus stop`.
5. **Compare:** use the same `gh pr list` data for both hours; the focus digest is extra data.
   Not a pure A/B: hour 2 builds different tasks on top of hour 1, so note the difficulty of each hour.



## What to log

- Research time, time to reach a solution (each demo-scope step)
- Per build hour: PRs opened / reviewed / merged, review rounds per PR, review time per PR
  (`gh pr list` for both hours; focus digest for hour 2)
- Token / $ cost per agent role and model; which tasks used the wrong model size
- Key decisions and why (`docs/decisions/`)
- Difficulties and suggested improvements for all three tools: demo-scope, pr-team, focus-hour

