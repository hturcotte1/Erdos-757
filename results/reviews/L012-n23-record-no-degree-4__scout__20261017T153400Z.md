NOVELTY: CLEAR

# Novelty check: L012 (a 23-point (4,5)-set with h = 13 has every AP-degree <= 3; the degree-4 case is excluded by exact realizability)

Scan date: 2026-10-17 (UTC). Claim file: results/proofs/L012-n23-record-no-degree-4.md (Theorems 1-3; computer-assisted; conditional on L011).
Label note: CLEAR means a careful search found nothing equal or stronger. Scope is novelty only; correctness is the referee's job.

## Verdict
1. No source states any structural constraint (degree bound, saturation, connectivity, tau, m) on a hypothetical 23-point (4,5)-set with h = 13, nor that such a set must have 21 AP-edges or only AP-degree <= 3. No source mentions the cell (23,21,10) or exact realizability of AP patterns as an exclusion tool.
2. The omega 23-point construction (A_2 = B ∪ 4096·B, glued at 0, B a 12-point set) does NOT contradict or pre-empt L012. Its largest Sidon subset has size h = 14 (alpha(H(A_k)) = 7k, tau = 4k+1 = 9), so h/n = 14/23 = 0.6087 > 4/7; it is a counterexample to an auxiliary inequality (avoidance of 0 gives 210 > 208), not a record set. In A_2 the point 0 has AP degree 2 (omega's text). It is not an h = 13 set (it would need tau = 10; it has tau = 9, and m is far below 21 so it is not saturated).
3. The published results on the structure of extremal sets are only: Gyarfas-Lehel (1995) Thm 3.2 proof ("vertices of AP-degree >= 3 are handled greedily; the rest has Delta <= 2"), Henning-Yeo (2021) 17 tau <= 5n + 3m, and Ma-Tang (2026) f(14) <= 8 via A_base (which itself has a degree-4 vertex, the point 0). None gives a max-degree constraint for any record set; none treats n = 23.
4. No paper, preprint, forum comment, GitHub issue or MathOverflow thread found citing Ma-Tang 2026, Gyarfas-Lehel 1995 or Henning-Yeo 2021 with small-n exact computations or degree restrictions on record sets.

## Sources checked (all 2026-10-17)
| Source | URL | Finding |
|---|---|---|
| erdosproblems.com/757 | https://www.erdosproblems.com/757 | Open; bounds 9/17 <= c <= 4/7 (Ma-Tang); last edited 10 Apr 2026; 7 comments, 0 proof claims. No mention of 23-point sets, AP degree, or small-n values. |
| erdosproblems.com forum thread | https://www.erdosproblems.com/forum/thread/757 | 7 comments: Lin and Bloom (8 Jan, positivity/translation invariance), Tang (27 Feb, announces arXiv:2602.23282), Tao (const. 5b), Sothanaphan x2, Tang. Nothing on 23 points, degrees, record structure, exact f(n). |
| erdosproblems.com history | https://www.erdosproblems.com/history/757 | Only the 10 Apr 2026 version (via search listing); no new content. |
| Omega GitHub issue #9804 | https://github.com/the-omega-institute/trureturing/issues/9804 (re-fetched; also kb/notes/omega_issue_9804.md) | The 23-point set is A_2 in the section "The failure persists under degree-two avoidance...": h = alpha = 14, tau = 9, ratio 14/23 > 4/7, "0 has AP degree two". Refutes an inequality, not the constant. No max-degree statement for record sets; the only degree claim is an unverified "Delta(G) <= 6 under maximum-independent-set hypotheses". Issue states the problem remains unresolved, no proof claims. |
| Ma-Tang arXiv abs/pdf/html | https://arxiv.org/abs/2602.23282 ; https://arxiv.org/html/2602.23282v1 | v1 26 Feb 2026, v2 6 Mar 2026. Only small-n content: f(14) <= 8. No n = 23, no degree bound on extremal sets (kb/notes/ma_tang_2026.md). |
| Gyarfas-Lehel 1995 (kb/notes/gyarfas_lehel_1995.md) | JCTB 64 (1995) 108-118 | Thm 3.2 proof structure only (greedy on degree >= 3, then Delta <= 2); no extremal-set degree bound. |
| arXiv API (export.arxiv.org): all:"weak Sidon"; Gyarfas+Lehel+Sidon; "Sidon subset"+"arithmetic progressions"; Sidon+"Erdos problem"+difference (date-sorted) | https://export.arxiv.org/api/query | Only Ma-Tang 2602.23282 is relevant. Others unrelated: 2609.xxxx Kneser-graph magic maps, 2608.02667 (multinomial coefficients Sidon subsets), Lean Singer-Sidon formalization (2605). Earlier scouts' queries (math.CO/math.NT, transversal+AP, F7/AG(2,3)) give the same. |
| Semantic Scholar citations of 2602.23282 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23282/citations | Today HTTP 429 (rate limited); earlier scout (L011) got HTTP 200 with an empty list. Not evidence either way. |
| Web search (standard) x4: "Erdos problem 757 ... 23 points"; "(4,5)-set Sidon five distinct differences Ma Tang"; "Erdos 757 github issue ... degree"; MathOverflow query | search tool | Only Ma-Tang, erdosproblems.com pages, emergentmind; "didn't turn up anything about 23 points". No MathOverflow thread found (direct MO search unavailable). |
| GitHub search for "Erdos 757" issues/code | GitHub search via web | No relevant hit besides omega #9804 and the formal-conjectures 757.lean (statement only), JSP-000621 #49, MATH-PROGRAMME #2028 (listed in bibliography; earlier scouts found no content on small n). |
| Earlier scouts | results/reviews/L011-f22-equals-13__scout__20261017T123223Z.md and L007-L010 scouts | Same conclusions: no exact f(n), no record-size bound, no inequality 11 tau <= 3n + 2m in the literature. |

## Caveats
- GitHub comment/search APIs and MathOverflow search were not directly reachable; coverage there rests on web-search snippets. Paywalled Henning-Yeo 2021 full text not read (same limitation as earlier scouts; its equality structure could in principle constrain degrees, but nothing in the abstract/zbMATH record suggests a 23-point statement).
- L012 is conditional on L011 and refereeing; this scout does not assess that.
- Bibliography: no new paper needed (nothing new found); no change to kb/literature/bibliography.md.
