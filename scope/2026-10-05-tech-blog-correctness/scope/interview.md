# S2 interview (2026-10-05)

| Aspect | Answer |
|---|---|
| Persona & situation | Solo technical author (AI Solution Engineer), AI + System Design long posts |
| Trigger | A new release (model/framework/API) makes an old post wrong |
| Input | Contributors bring: inline span suggestion, source link (release notes/paper), code/math fix |
| Output | Reader sees: updated text + contributor credit, freshness badge (verified / may be outdated + reason + source), changelog diff |
| Done | Feed a real release note → system flags the exact paragraphs it contradicts (source + reason) → author fixes or accepts reader suggestion → badge flips to "verified" |
| Today | No blog yet; starting fresh |
| Constraints | Claude API OK; local-first demo (one-command start), deploy later; no reader PII beyond OAuth login |
| Look & feel | Lil'Log-like clean: wide reading column, math/code first-class, TOC sidebar, Google-Docs-style inline suggestion popovers; airy, light+dark toggle |

## Candidate core-job sentences
1. **(CHOSEN)** A solo AI author can see which paragraphs a new release makes wrong, without rereading every post.
2. A solo tech author can turn reader span suggestions into credited revisions without comment noise.
3. A solo tech author can keep posts verifiably current, flagged by releases and fixed by readers, without manual audits.

## Still unclear
- Which real release/post pair to use as the demo fixture
- Reference UI screenshots → save 1–2 into refs/
