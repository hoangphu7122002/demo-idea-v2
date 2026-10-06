# Demo script — contrast-first (≤120 s)

Split screen whole demo: LEFT = today (Hugo post + Giscus thread + release notes tab), RIGHT = app. Same input both sides: seeded AI post + one real release note.
Framing: author's own need, not validated demand (decision risk 1).

| # | Beat | s | Script |
|---|---|---|---|
| 1 | Hook | 15 | On screen: "People asked us a lot how we'd keep the book up to date. We didn't really know." (E017, HN, 2025-08). Say: "Same for my blog. A model ships, my posts quietly go wrong." |
| 2 | Today | 15 | LEFT: release note open, Ctrl-F through a 4k-word post, Giscus thread at bottom has "this is outdated" with no anchor. Timer keeps running. Say: "Today: reread everything, hope a reader comments." |
| 3 | Core action | 45 | RIGHT: paste the same release-note URL into "Check against release" → click Check. Live Claude call (cached fallback). Paragraphs that contradict the release get highlighted in place. LEFT still scrolling. |
| 4 | Wow | 30 | RIGHT on screen: 3 flagged paragraphs, each with "may be outdated" badge + reason + quoted source line; click one → accept reader suggestion → badge flips to "verified", changelog diff shows. LEFT: still nothing found. Freeze both sides. |
| 5 | Next | 15 | Later: auto-watch release feeds, re-anchor suggestions across edits, contributor credits page, GitHub PR sync, deploy. "Releases flag, readers fix, posts stay true." |

Total: 120 s. Impact lands at ~60 s (flags appear).
