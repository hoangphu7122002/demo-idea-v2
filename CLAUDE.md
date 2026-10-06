# demo-idea-v2

Technical knowledge blog. Plan: `scope/2026-10-05-tech-blog-correctness/roadmap.md` (features `F<n>`, waves). Work one feature at a time with `/bach:pr-team <roadmap>#F<n>`.

## Talking to the operator (lead and any agent the operator talks to)

- **Language:** English everywhere: messages to the operator, code, commits, PRs, file contents and messages between agents.
- **Questions to the operator** must be clear, short and to the point:
  - One question per message (or one `AskUserQuestion` call with up to 4 related questions).
  - Bullet points, not paragraphs. Each bullet ≤ 1 line.
  - Say what you need decided, the options (2–4), and which one you recommend and why (one line).
  - No background the operator didn't ask for; link the file instead.
- **Status updates:** 2–5 bullets: what finished, what's running, what's blocked on the operator.

## Workflow log (update continuously)

`workflow-log.md` is append-only and updated **as events happen**, not at the end. The lead appends one line per event:

```
- HH:MM · <F id or phase> · <event> · <detail / link>
```

Log at least:
- session start/end, feature picked, plan approved (with task list)
- each teammate spawn/shutdown, each PR opened / pre-review verdict / merged (with number)
- each operator decision and each blocker (permission prompt, failing check, conflict)
- problems or improvement ideas for the plugin (demo-scope, pr-team, stack) under the current session's heading

Start a heading per session: `## <date> · F<n> · <short name>`. Keep times in local time.
