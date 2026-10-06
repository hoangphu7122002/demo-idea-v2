# Workflow log

## demo-scope · 2026-10-05
Run: scope/2026-10-05-tech-blog-correctness/ · outcome: roadmap.md, 79 features (M1 = 9 features, 6 waves)

Problems / plugin improvements:
- Workflow tool refused scriptPath outside workspace (plugin dir) → had to copy workflows into <run>/.workflows/. demo-scope should copy scripts into the run folder itself.
- plan.js only planned cut.md scope; brief needs full feature map with demo = M1. Patched local plan.js (reads brief + features.md, Milestone line, rule check fails on missing brief features). Upstream this.
- Gates 24-month recency rule dropped all human-collected rows (2005–2021, Reddit blocked) → G1 fail. Runbook should warn humans to collect only recent quotes.
- Cut stage ran before user's appended features.md edits landed; cut.md missed them (roadmap step re-read features.md, so no loss).
- Spec worksheets judged the reader-correction angle; core job picked later in S2 (release staleness) → gates/critic did not re-evaluate the chosen job.

## 2026-10-06 · roadmap refine (operator + Claude in VS Code)
- 10:0x · roadmap · 79 → 38 features, bilingual EN+VI to M2, new-finding service as parallel M2 track, demo artifacts moved to "M1 demo prep" · roadmap.v1.md kept
- 10:2x · roadmap · dependency graph replaced by a cluster graph (14 clusters, 21 edges) + cluster table; per-feature graph was unreadable (38 nodes, 66 edges)
- 10:3x · process · CLAUDE.md added: lead talks Vietnamese with the operator, short bullet questions, workflow-log updated per event
- 10:35 · process · operator: English everywhere (files, PRs, lead messages); CLAUDE.md updated
- 10:36 · setup · bach plugin source moved to archive/bach-workflow in this repo (local/all-prs, 0.6.2); reinstalled for demo-idea-v2 and demo-idea
