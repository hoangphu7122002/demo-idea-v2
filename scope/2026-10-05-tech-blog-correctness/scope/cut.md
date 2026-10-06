# Cut test — single-feature web app, solo, 2 days
Strict pass. Rules: 1 not on screen→Later; 2 fakeable without breaking beat 3/4→Fake; 3 2nd user type→Later; 4 always-later→Later.

| feature | column | rule | reason | beat | hours | fake method |
|---|---|---|---|---|---|---|
| LLM-assisted flag of outdated statements vs pasted release note | Build | — | IS the core action; paragraph flags+reasons must be real | 3,4 | 5 | live Claude call + cached fallback |
| Markdown post rendering w/ code highlight (paragraph ids) | Build | — | highlights need real paragraph DOM | 2,4 | 2 | — |
| Reader-visible freshness badge (amber "May be outdated" → green "Verified") | Build | — | the wow visual | 4 | 1.5 | — |
| Accepted fix applies directly to post body | Build | — | text update is wow payoff | 4 | 2 | — |
| Inline diff preview of fix vs original | Build | — | diff shown in wow | 4 | 1.5 | — |
| AI-drafted correction proposals | Fake | 2 | same LLM response carries fix text | 4 | | cached in same API response |
| Claim-level staleness extraction | Fake | 2 | folded into flag prompt | 3 | | part of live call + cache |
| Reader "Suggest edit" on highlighted text | Fake | 2 | one seeded suggestion | 4 | | seeded data (W1 wording) |
| Author accept/decline/withdraw one click | Fake | 2 | only Accept button, wired to apply | 4 | | accept only; others static |
| Inline paragraph "Updated <date>" marker | Fake | 2 | static text appended on apply | 4 | | template string on apply |
| Seeded sample AI + system-design posts | Fake | 2 | data | 2-4 | | realistic seeded dataset |
| Reader identity / login | Fake | 2 | auth | 4 | | one seeded account logged in |
| Detect outdated code snippets/versions | Fake | 2 | covered by LLM flag | 3 | | part of live call + cache |
| Post page with TOC + anchored headings | Later | 1 | not in beat | | | |
| Select text inline comment | Later | 1 | not in beat | | | |
| Margin view of comments | Later | 1 | not in beat | | | |
| Comment anchors surviving edits | Later | 1 | roadmap only | | | |
| Orphaned-anchor detection | Later | 1 | not shown | | | |
| Auto-appended public changelog | Later | 1 | roadmap only | | | |
| Reader credit on accepted correction | Later | 1 | roadmap only | | | |
| Notify proposer | Later | 1 | not shown | | | |
| Proposal status visible to reader | Later | 3 | reader-side view = 2nd user type | | | |
| Report error flag | Later | 3 | reader actor | | | |
| Correction types taxonomy | Later | 1 | not shown | | | |
| Version history + restore | Later | 1 | not shown | | | |
| Diff between post versions | Later | 1 | inline diff covers beat | | | |
| Last reviewed date on post | Later | 1 | updated marker covers it | | | |
| Staleness banner after N days | Later | 1 | not shown | | | |
| Configurable stale threshold | Later | 4 | settings | | | |
| Per-post staleness score | Later | 1 | not shown | | | |
| Staleness dashboard | Later | 1 | not shown | | | |
| Reader outdated vote | Later | 3 | reader actor | | | |
| Outbound link checker | Later | 1 | not shown | | | |
| Author review queue | Later | 1 | not shown | | | |
| Severity ranking | Later | 1 | not shown | | | |
| Mark section superseded | Later | 1 | not shown | | | |
| Per-paragraph discussion thread | Later | 3 | reader actor | | | |
| Reactions/upvotes | Later | 3 | reader actor | | | |
| Spam/rate limiting | Later | 4 | edge case off path | | | |
| Moderation tools | Later | 4 | admin | | | |
| Anonymous suggestions | Later | 3 | reader actor | | | |
| Email/webhook notification | Later | 4 | integration off path | | | |
| Notification digest | Later | 1 | not shown | | | |
| Export corrections to Git PR | Later | 4 | integration off path | | | |
| Import posts from Markdown/repo | Later | 1 | seeded instead | | | |
| Embeddable widget for static blog | Later | 4 | integration off path | | | |
| Markdown editor w/ preview | Later | 1 | not shown | | | |
| Draft review mode | Later | 1 | not shown | | | |
| RSS "what changed" feed | Later | 1 | roadmap only | | | |
| Subscribe to post | Later | 3 | reader actor | | | |
| Search | Later | 1 | not shown | | | |
| Dark mode / responsive | Later | 4 | always-later | | | |
| Paragraph citation link | Later | 1 | not shown | | | |
| Paragraph analytics | Later | 1 | not shown | | | |
| Per-post feedback counts | Later | 1 | not shown | | | |
| Prose linting | Later | 1 | not shown | | | |
| Open data export | Later | 1 | not shown | | | |

## Totals
Build 5 items, 12 h (≤14 OK) · Fake 8 · Later 43. Riskiest dep: Claude call → cached fallback.

## User decisions (2026-10-05)
- Accepted cut-critic move 5: **Inline diff preview** = whole-paragraph render, old in `<del>`, new in `<ins>`; no word-level diff algorithm. Stays Build.
- Rejected moves 1–4: the LLM flag stays real (brief requires a technically challenging differentiator), real Markdown/MDX rendering, real badge state, real apply/revision.
- Build hours: user estimate **12 h** (5 items), within the rule.

## Later: added from the brief's full feature map (all stay on the roadmap, not dropped)
See scope/features.md § "Added from the brief's full feature map": roles, EN+VI, deploy, series/categories, illustrations, voice→draft, mobile reading + follow, reputation/credit, new-finding service (ingest, rank, daily digest, feedback tuning, item→draft, outdated-post flags), motion video, seed users/posts.
