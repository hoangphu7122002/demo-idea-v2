# Your research tasks (about 40 minutes, while the agents run)

Agents cannot open these sites (403 / login walls). Paste what you find into
`evidence_human.csv` in this folder, one row per quote. Columns:

| Column | Value |
|---|---|
| type | `pain` (a complaint), `review` (competitor 1–3★ review), `competitor` (a tool you found), `spend` (someone paying for it) |
| source | e.g. `reddit r/freelance`, `G2 <competitor>`, `Capterra <competitor>` |
| url | link to the post or review |
| date | YYYY-MM-DD (approx is fine) |
| quote_or_number | the exact words, copy-pasted |
| persona_match | `y` if the writer matches the persona, else `n` |
| theme | 2–4 word tag, e.g. `chasing payment`, `too complex` (optional) |
| note | anything else |

## H1 · Reddit (20 min)
Open each link, set **Sort: Top · Time: Past year** if not already, open the
10 longest threads, copy the most specific complaints. Long rants with details
count most.

- Global `blog post outdated`: https://www.reddit.com/search/?q=blog%20post%20outdated&sort=top&t=year
- Global `inline comments technical blog`: https://www.reddit.com/search/?q=inline%20comments%20technical%20blog&sort=top&t=year
- Global `suggest edit blog post`: https://www.reddit.com/search/?q=suggest%20edit%20blog%20post&sort=top&t=year
- Global `reader feedback technical writing`: https://www.reddit.com/search/?q=reader%20feedback%20technical%20writing&sort=top&t=year
- Global `keep technical content up to date`: https://www.reddit.com/search/?q=keep%20technical%20content%20up%20to%20date&sort=top&t=year
- r/ExperiencedDevs `blog post outdated`: https://www.reddit.com/r/ExperiencedDevs/search/?q=blog%20post%20outdated&restrict_sr=1&sort=top&t=year
- r/ExperiencedDevs `inline comments technical blog`: https://www.reddit.com/r/ExperiencedDevs/search/?q=inline%20comments%20technical%20blog&restrict_sr=1&sort=top&t=year
- r/ExperiencedDevs `suggest edit blog post`: https://www.reddit.com/r/ExperiencedDevs/search/?q=suggest%20edit%20blog%20post&restrict_sr=1&sort=top&t=year
- r/technicalwriting `blog post outdated`: https://www.reddit.com/r/technicalwriting/search/?q=blog%20post%20outdated&restrict_sr=1&sort=top&t=year
- r/technicalwriting `inline comments technical blog`: https://www.reddit.com/r/technicalwriting/search/?q=inline%20comments%20technical%20blog&restrict_sr=1&sort=top&t=year
- r/technicalwriting `suggest edit blog post`: https://www.reddit.com/r/technicalwriting/search/?q=suggest%20edit%20blog%20post&restrict_sr=1&sort=top&t=year
- r/MachineLearning `blog post outdated`: https://www.reddit.com/r/MachineLearning/search/?q=blog%20post%20outdated&restrict_sr=1&sort=top&t=year
- r/MachineLearning `inline comments technical blog`: https://www.reddit.com/r/MachineLearning/search/?q=inline%20comments%20technical%20blog&restrict_sr=1&sort=top&t=year
- r/MachineLearning `suggest edit blog post`: https://www.reddit.com/r/MachineLearning/search/?q=suggest%20edit%20blog%20post&restrict_sr=1&sort=top&t=year

## H4 · G2 / Capterra 1–3★ reviews (20 min)
For each competitor: open reviews, filter to 1–3 stars, read 10, copy each
complaint and tag a theme (price, missing feature, too complex, support, …).

- Ghost: https://www.g2.com/search?query=Ghost · https://www.capterra.com/search/?query=Ghost
- Giscus: https://www.g2.com/search?query=Giscus · https://www.capterra.com/search/?query=Giscus
- Hypothesis: https://www.g2.com/search?query=Hypothesis · https://www.capterra.com/search/?query=Hypothesis
- GitBook: https://www.g2.com/search?query=GitBook · https://www.capterra.com/search/?query=GitBook
- Lil'Log / Knowbie: not on G2/Capterra — skim their comment/feedback setup (or lack of) and note as `competitor` rows.

When done, reply **done** in the Claude session.
