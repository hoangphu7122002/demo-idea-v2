# 0001 · Differentiator: release → flagged stale paragraphs (2026-10-05)

- **Decision:** Demo core (M1) = paste a release note → LLM flags the exact post paragraphs it contradicts (reason + source) → accept reader/AI fix → freshness badge flips to Verified.
- **Rule said KILL** (G1 pain fail: ~2 real recent quotes; critic NO-GO, held under push-back). **User override → GO**: brief mandates building the blog; the decision only picks the differentiator.
- **Accepted risks:** weak demand evidence (pitch as author's own need); visible loop resembles Hypothesis/Brevy (re-anchoring deferred to roadmap F42); LLM check needs a 30-min spike + cached fallback with identical flag ids.
- **Cut:** LLM flag, MDX+KaTeX rendering, badge, apply-fix stay real (technical-challenge requirement); diff = whole-paragraph del/ins.
- Details: scope/2026-10-05-tech-blog-correctness/{decision.md,scope/cut.md,specs/spec.md,roadmap.md}
