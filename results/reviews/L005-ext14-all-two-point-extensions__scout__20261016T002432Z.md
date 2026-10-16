NOVELTY: CLEAR

# Novelty check: L005 (two-point extensions of all 2,910 saturated extremal 14-point classes)

Scan date: 2026-10-16 (UTC). Claim: no 16-point (4,5)-set with h <= 9 contains a saturated extremal 14-point (4,5)-set (equivalently, every 14-point subset with h=8 of a 16-point record has m=11), obtained by running the L001 case analysis on all 2,910 classes of census L004.

CLEAR means: nothing equal or stronger was found. The closest prior item is the community (unrefereed) A_base-only result, which is strictly weaker; this was already known to the project as L001 (see below). Note on label set: results/reviews/README.md allows CLEAR / PRIOR-WORK / UNSURE; the task text said KNOWN / UNCLEAR, and CLEAR is valid in both.

## Closest prior work (strictly weaker: one 14-point set only)
- The omega thread, the-omega-institute/trureturing issue #9804 (https://github.com/the-omega-institute/trureturing/issues/9804), re-fetched today. Body states [community]: for any two distinct reals x,y outside A_0 (= A_base) with A_0 ∪ {x,y} a (4,5)-set, the max Sidon subset has size ten; the certificate covers 6,609 compatible extensions. It adds that "these results do not rule out other sixteen-point configurations". No comments in the Activity section. It concerns only the Ma-Tang block A_base, not other extremal 14-point sets, and not the census of 2,910 classes (the thread has no census of 14-point sets at all). The same fact is recorded in kb/notes/omega_issue_9804.md and kb/literature/part2_supplement.md lines 178-179, and was independently re-proved here as L001 (ACCEPTED). L005 generalizes it from 1 class to all 2,910 saturated classes (141,153 single extensions, 4,970,208 two-point extensions, vs 6,609 for A_base), so it is stronger, not equal.
- The thread also states "a 16-point set has at most 14 AP edges" (equals m <= n-2, K3-K6) and discusses a 16-point power-of-ten set with ratio 3/4; neither is related to L005.

## Sources checked (all 2026-10-16 unless noted)
| Source | URL / query | Result |
|---|---|---|
| erdosproblems.com problem page | https://www.erdosproblems.com/757 | Lists 9/17 <= c <= 4/7 (Ma-Tang); last edited 10 Apr 2026; no mention of computations, 14-/16-point sets or f(16) |
| erdosproblems.com forum | https://www.erdosproblems.com/forum/thread/757 | 7 comments (Lin 8 Jan, Bloom 8 Jan, Tang 27 Feb, Tao 27 Feb, Sothanaphan x2, Tang): nothing on extensions, 16-point sets or f(n) |
| Problem history / LaTeX pages | https://www.erdosproblems.com/history/757 , /latex/757 (surfaced by web search, not fetched in full) | no sign of extension results in snippets |
| arXiv, Ma-Tang | https://arxiv.org/abs/2602.23282v2 (v1 html https://arxiv.org/html/2602.23282v1) | The only paper on the problem; contains A_base and the gluing lemma; no two-point-extension result, no census (also per kb/notes/ma_tang_2026.md) |
| arXiv API | http://export.arxiv.org/api/query with abs:Sidon AND abs:"weak Sidon" (sorted by date) | Only Ma-Tang (2602.23282) and unrelated papers (2609.12546, 1910.08377) |
| arXiv API | all:Sidon AND all:"distinct differences" AND all:four | 0 results |
| arXiv API | all:Gyárfás AND all:Lehel AND all:Sidon | only Ma-Tang |
| Semantic Scholar | https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23282/citations | empty data (index lag or none); no citing paper found. Earlier baseline scan (results/reviews/baseline__scout__20261013T230359Z.md) also found only Ma-Tang citing Gyárfás-Lehel 1995 and Henning-Yeo 2021 |
| Web search x5 | "Erdős problem 757 Sidon subset (4,5)-set two-point extension 14-point 16-point"; "Largest Sidon subsets in weak Sidon sets Ma Tang citing"; "weak Sidon (4,5) Erdős 757 extremal sets exhaustive enumeration f(16)"; "mathoverflow every four points five distinct distances largest Sidon subset 3-term progression free hypergraph" | Only Ma-Tang, Tao #135 (arXiv:2409.01343), Riblet (arXiv:2605.03181), erdosproblems pages; nothing on 14-point extensions, f(16), or "every 14-point subset of a 16-point record is non-saturated" |
| MathOverflow | via web search only (no direct query possible) | no thread found |
| GitHub | api.github.com issue search for "Erdős 757" / "Erdos 757" | returned 94,676 unrelated hits (the query was tokenized loosely; first 20 all unrelated numbered issues); effectively no usable hit beyond the known omega issue #9804. Other known repos (QuanyuTang/ep757-45set-base-block-verification, formal-conjectures 757.lean, JSP-000621 #49, MATH-PROGRAMME #2028) were not re-fetched; the earlier scout (L002) found no extension/census content there |
| Local digests | kb/notes/*.md, kb/literature/*.md (grep for 16-point, two-point, extension) | Only the A_base extension (omega thread) appears; kb/notes/extension_lemmas.md is project-internal [derived-here] |

## Limits
- Google Scholar and MathOverflow cannot be queried programmatically (web-search snippets only). Semantic Scholar returned an empty citation list. GitHub issue search syntax was too loose to be informative; the omega thread was read directly.
- The omega thread is a live, unrefereed document; it may be updated after this scan. Its present text contains no census-wide extension statement.
- Novelty is for the statement as phrased (all 2,910 saturated classes of L004, two-point extensions). It depends on the project's own census L004, which no outside source reproduces.
