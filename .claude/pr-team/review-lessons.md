# Review lessons

Shared corpus of review feedback (operator comments + pre-reviewer findings). Every builder reads this before sending a plan; every reviewer checks new PRs against it.
pr-watcher appends one line per operator comment; the lead appends reviewer findings. Format:

`- [folder] rule — source (PR #, who)`

## Operator (human) comments
- [backend] Routes/controllers only handle HTTP (parse, call, map errors). Domain logic and queries live in `app/<domain>/service.py`, schemas in `app/<domain>/schemas.py`. — PR #7 "domain in separated file", PR #13 "move logic out of controller" (operator)
- [backend] Public functions and modules get clear docstrings: what, inputs, outputs, errors. — PR #13 (operator)
- [all] Each follow-up fix with its own intent is its own PR (e.g. cache safety ≠ API). — PR #12/#13 (operator)
- [backend] LLM code stays provider-neutral (Anthropic, OpenAI, Gemini via `LLM_MODEL`); no vendor-specific code paths or docs. — F3 (operator)
- [backend] Model strings: anthropic:<model>, openai:<model>, google:<model> (Gemini prefix is `google:`; `google-gla:` is rejected by the installed pydantic-ai). — PR #15 (builder-1)

## Pre-reviewer findings
- [backend] File writes that others may read concurrently are atomic: temp file in the same dir + `os.replace`; a corrupt file is treated as missing, never a 500. — PR #12 (reviewer-pr12)
- [backend] External text put into an LLM prompt is wrapped in delimiters, the closing tag is escaped, and the model is told to treat it as data. — PR #12, PR #14 (reviewer-pr12, reviewer-pr14)
- [backend] LLM output is validated against inputs: drop unknown ids, check quotes really occur in the source (whitespace-normalised, minimum length). — PR #12, PR #14 (reviewer-pr12, reviewer-pr14)
- [backend] Tests must not depend on the ambient env (`.env`); set settings explicitly. — PR #2 (reviewer-pr2)
- [backend] Every non-2xx response a route can return is declared in OpenAPI `responses=`. — PR #2 (reviewer-pr2)
- [backend] Pin exact counts in tests where the fixture is fixed (e.g. 20 paragraphs), assert ordering on the real key (position), assert persisted ids in the DB. — PR #7, PR #13 (reviewer-pr7, reviewer-pr13)
- [frontend] Security tests must fail when the guard is removed (no vacuous XSS assertions). — PR #8 (reviewer-pr8)
- [frontend] Colours come from theme tokens and meet ≥4.5:1 contrast in light and dark; links are themed. — PR #4, PR #8 (reviewer-pr4, reviewer-pr8)
- [frontend] React list keys are unique even when data repeats (e.g. 2 flags on one paragraph). — PR #10 (reviewer-pr10)
- [frontend] Buttons keep their label while pending (spinner + text). — PR #10 (reviewer-pr10)
- [frontend] Generated API types are the source of truth; nullable fields in the API stay nullable in TS. — PR #13 (reviewer-pr13)
- [process] Before posting a review comment or label, re-check the PR state in a separate command; never chain it with `&&`. — PR #12 (reviewer-pr12)
- [frontend] Mutation/query state is scoped to the entity it belongs to: reset or key the page by id/slug so one post never shows another post's data. — PR #16 (reviewer-pr16)
- [frontend] Tests restore any global/prototype they patch (afterEach). — PR #16 (reviewer-pr16)
- [all] A test for a fix must fail when the fix is reverted (mutation-check it); otherwise it is vacuous. — PR #8, PR #18 (reviewer-pr8, reviewer-pr18)
