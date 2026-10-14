NOVELTY: CLEAR

# Novelty check for the census results (L002, L003) and lemmas K30, K31

Scan date: 2026-10-14 (UTC). Claims checked: (1) 54,243 twelve-point (4,5)-sets with h=7 up to affine equivalence; (2) saturated extremal counts 1, 4, 66, 1262, 6644, 466961 for n=6..11; (3) K30 (monotone midpoints) and K31 (no medial triangle). No source found containing any of them. "CLEAR" means nothing equal or stronger was found; the search is limited as noted.

## Searches performed
| Source | URL / query | Result (2026-10-14) |
|---|---|---|
| OEIS | https://oeis.org/search?q=1,4,66,1262,6644 | "terms do not match anything in the table" |
| OEIS | https://oeis.org/search?q=1,4,66,1262 | no match |
| OEIS | https://oeis.org/search?q=54243 | 8 hits (A266969, A293294, A032922, A332736, A372904, A050191, A054243, A318169), none about Sidon or difference sets; 54243 is an incidental term |
| OEIS | query "Sidon weak three-term progression largest subset" | no match |
| erdosproblems.com forum | https://www.erdosproblems.com/forum/thread/757 | 7 comments (Tang, Tao, Sothanaphan, Lin, Bloom); no counts, no monotone-midpoint or medial-triangle remarks |
| Web search | "enumeration of sets where every four points determine at least five distinct differences, largest Sidon subset, computer census" | found only Erdos #135 (Tao, arXiv:2409.01343) and #757 pages; no census |
| Web search | "weak Sidon" classification extremal sets census OR enumeration | found only Ma-Tang arXiv:2602.23282 (https://arxiv.org/abs/2602.23282v2) and unrelated Sidon papers; no census |
| Web search | github "Erdos 757" exhaustive search 12-point | no repository; only unrelated gcd-Sidon repo (AllenGrahamHart/gpt_problems) |
| Web search | Ma-Tang follow-up exact f(n) small n | no follow-up paper |
| Local notes | grep of kb/notes/gyarfas_lehel_1995.md, ma_tang_2026.md, omega_issue_9804.md for monotone/medial/census/enumerat | no mention of K30, K31, or counts; the omega thread (https://github.com/the-omega-institute/trureturing/issues/9804) gives only a few explicit 12-point examples and no enumeration |
| Baseline scan | results/reviews/baseline__scout__20261013T230359Z.md (2026-10-13) | Semantic Scholar citations of Gyarfas-Lehel 1995 and Henning-Yeo 2021: only Ma-Tang 2026 and unrelated; Erdos Problem a Day log 12 Aug 2026 gives the small table only |

## Limits
- arXiv API (export.arxiv.org) and Semantic Scholar search returned HTTP 429 during this session, so the arXiv keyword listings were not re-run today; the 2026-10-13 baseline scan did run arXiv API queries (Sidon + distinct differences; weak Sidon; (4,5)-set) with no relevant hit, and the web searches above surfaced no newer paper.
- Google Scholar and MathOverflow cannot be queried programmatically; covered only via web-search snippets.
- Ma-Tang and Gyarfas-Lehel were checked through the repo digests (kb/notes), not re-read in full today. K30 and K31 are elementary consequences of the AP equations and weak-Sidon; their absence from the digests does not exclude an implicit use in the papers.
- Counts (1)-(2) depend on the project's own definitions of "saturated" and "affine equivalence"; any outside enumeration would need matching conventions.
