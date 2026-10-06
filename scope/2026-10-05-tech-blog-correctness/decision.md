# Decision — 2026-10-05

**Decision: GO (user override of rule).** Rule (rules/gates.md) said KILL: G1 fail.

## Gates
| Gate | Mark |
|---|---|
| G1 Pain | fail — staleness theme ≈2 real recent quotes (E017, E094); inline-correction evidence all pre-2024-10 |
| G2 Gap | partial — no theme across ≥3 competitors; no-inline only Giscus (E132) |
| G3 Demo moment | partial — visible loop resembles Hypothesis/Brevy/Medium |
| G4 2-day build | pass — 1 risky dep (LLM staleness check) with cached fallback |

Critic: NO-GO (held under push-back; critic_discarded=false).

## Why override
Hackathon brief mandates building the blog (author will keep using it). Decision only picks the differentiator. Demo core = **release → flagged stale spans**: feed a real release note, system flags exact paragraphs it contradicts (source + reason), author fixes / accepts reader suggestion, badge flips to verified.

## Accepted risks (critic conditions → must address)
1. Weak pain evidence: demo pitch must not claim validated demand; frame as author's own need.
2. Must not read as Hypothesis clone: staleness flag + re-anchoring must be visible on screen.
3. Run D7 spike (LLM claim-vs-release contradiction check) early; cached fallback per seeded post.
4. Open ~/demo-idea v1 code to confirm reuse of MDX render, suggestion popup, approve→revision before committing.

## Constraints
- Code freeze: Day 2, 16:00
- Stack: this repo (lean-web-stack); re-implement ideas from ~/demo-idea v1 (read-only)
- Local-first demo (one command); Claude API OK; OAuth-only PII
