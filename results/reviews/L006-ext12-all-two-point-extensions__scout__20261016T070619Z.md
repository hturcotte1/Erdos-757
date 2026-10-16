NOVELTY: CLEAR

# Novelty check: L006 (no 14-point (4,5)-set with h <= 8 contains an extremal 12-point set)

Scan date: 2026-10-16 (UTC). Claim: for each of the 54,243 extremal 12-point classes of census L002 (h = 7), every (4,5) two-point extension has h = 9; hence no 14-point (4,5)-set with h <= 8 contains a 12-point subset with h = 7. Label note: results/reviews/README.md allows CLEAR / PRIOR-WORK / UNSURE; the task text said KNOWN / UNCLEAR. CLEAR is valid in both.

CLEAR means nothing equal or stronger was found. Nothing in the literature or community material mentions even the existence of a census of extremal 12-point sets, so the statement for all classes, and its consequence for non-saturated 14-point sets, has no prior statement.

## Closest prior work (strictly weaker or unrelated)
- Omega thread, the-omega-institute/trureturing issue #9804 (https://github.com/the-omega-institute/trureturing/issues/9804), re-fetched today. It displays two 12-point (4,5)-sets with h = 7 (as counterexamples to an auxiliary inequality, [community]) and says "Each displayed 12-point set has maximum Sidon subset size seven". Its extension statement is only for the 14-point block A_0 = A_base: "extending A_0 by two real points yields a 16-point set whose maximum Sidon subset size is exactly ten", with the caveat that this holds only for extensions retaining this block. Nothing about extending the 12-point sets, about 14-point sets containing them, about a census of h = 7 sets, or f(12), f(14). It also has two-copy union alignments (P+P, P+R, R+R sharing two points), which concern gluing, not extensions. No review comments, no formal reviews.
- Ma-Tang, arXiv:2602.23282v2 (https://arxiv.org/abs/2602.23282v2): abstract and comment field checked today. Contains g(n) = ceil((n+1)/2) for weak Sidon sets, bounds 9/17 <= c* <= 4/7, A_base. No exact f(n), no extremal 12-point sets (only an AI-found 7/12 intermediate example mentioned in the declaration), no extension results.
- Ma-Tang verification repo (https://github.com/QuanyuTang/ep757-45set-base-block-verification): only the A_base verification script; no 12-point, extension or census content.

## Sources checked (all 2026-10-16)
| Source | URL / query | Result |
|---|---|---|
| erdosproblems.com problem page | https://www.erdosproblems.com/757 | Bounds 9/17 <= c <= 4/7 only; no mention of 12-/14-/16-point sets |
| erdosproblems.com forum | https://www.erdosproblems.com/forum/thread/757 | Comments: Lin, Bloom (positivity/integers), Tang (announcement), Tao (constant 5b), Sothanaphan x2. Nothing on extensions or census |
| Omega issue | https://github.com/the-omega-institute/trureturing/issues/9804 | See above |
| arXiv, Ma-Tang | https://arxiv.org/abs/2602.23282v2 | See above |
| arXiv API | http://export.arxiv.org/api/query abs:"weak Sidon" AND abs:Sidon, date-sorted | Only Ma-Tang plus unrelated 2609.12546 and 1910.08377 |
| Semantic Scholar citations of 2602.23282 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23282/citations | Empty data list (index lag or no citers); no citing paper found. WebFetch version got HTTP 429, curl version returned empty data |
| Web search x3 | "Erdős 757 (4,5)-set extremal 12-point Sidon subset size seven extension 14-point"; ""weak Sidon" "Sidon subset" "five distinct differences" Gyárfás Lehel Ma Tang follow-up exact values f(n)"; "mathoverflow 3-term progression free subset linear hypergraph F7 affine plane (4,5)-set largest Sidon subset" | Only Ma-Tang, erdosproblems pages, unrelated Sidon-extension (arXiv:2604.25214), sumset (2605.00040) and line-free-set papers. No MathOverflow thread found |
| GitHub issue search | gh api search/issues | Blocked by the sandbox (HTTP 403, repository-scoped only); the omega issue was read directly via WebFetch. Other repos not searchable |
| Local digests | kb/notes/omega_issue_9804.md, ma_tang_2026.md, gyarfas_lehel_1995.md, neighbouring_problems.md, kb/literature/part1_literature_review.md, part2_supplement.md | Only the omega 12-point examples (refuted inequality, h = 7) and the A_base extension appear; no extension statement for 12-point sets. Earlier scouts L002 and L005 (results/reviews/) found the same |

## Limits
- Google Scholar and MathOverflow cannot be queried directly (web-search snippets only); GitHub issue search was blocked; Semantic Scholar showed no citers. The omega thread is live and could change after this scan.
- Novelty is for the statement as phrased: it relies on the project's own census L002 (54,243 classes), which no outside source reproduces, so an independent prior statement is very unlikely. The weaker consequences (f(13) = 8, f(14) = 8 from Henning-Yeo and A_base) are known; the claim's content beyond them is new.
