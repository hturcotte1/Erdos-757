NOVELTY: CLEAR

# Novelty check: L007 (every 14-point (4,5)-set with h = 8 has exactly 12 three-term APs; the 2,910 saturated classes of L004 are all extremal 14-point classes)

Scan date: 2026-10-17 (UTC). Claim file: results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md. Label note: results/reviews/README.md allows CLEAR / PRIOR-WORK / UNSURE; the task text said CLEAR / KNOWN / UNCLEAR. CLEAR is valid in both vocabularies and means: a careful search found nothing equal or stronger.

## Verdict in two parts

1. The claim itself (Theorem 2 / Corollary 3: no 14-point (4,5)-set with h <= 8 and exactly 11 APs; hence all 14-point (4,5)-sets with h = 8 are midpoint-saturated, and the count 2,910 is the total number of extremal 14-point classes) has no prior statement anywhere I could reach. Nothing in the literature or community material mentions a census of extremal 14-point sets, the number of APs of an extremal 14-point set, or even f(14) as a stated value. Ma-Tang give only the single example A_base. CLEAR.
2. The inequality 11 tau <= 3n + 2m (Lemma A, Lemma "I11") and any hereditary-sparse variant: NOT found in any accessible source. See the separate section below ("What is known about 11 tau <= 3n + 2m"). The limit is that the full text of Henning-Yeo 2021 and the 2020 Henning-Yeo book is closed access and was not read.

## Quoted prior work (all strictly weaker, unrelated, or different in form)

- Ma-Tang, arXiv:2602.23282v2 (https://arxiv.org/abs/2602.23282, abs page re-fetched today; versions v1 26 Feb 2026, v2 6 Mar 2026, no v3; comments "15 pages. This is the submitted version."). Abstract (as summarized by the fetch): g(n) = ceil((n+1)/2) for weak Sidon sets; 9/17 <= c* <= 4/7; "explicit 14-point set", "computer-verified" (emergentmind summary). No exact f(n), no classification of 14-point sets, no AP counts. The PDF text streams could not be decoded by the fetch tool (compressed); the project's own digest is kb/notes/ma_tang_2026.md (section "What the paper does NOT do").
- Henning-Yeo, Graphs Combin. 37 (2021) 867-890 (https://link.springer.com/article/10.1007/s00373-021-02285-x ; UJ portal https://pure.uj.ac.za/en/publications/affine-planes-and-transversals-in-3-uniform-linear-hypergraphs/). Abstract quoted by the search tool: "Tuza ... and Chvatal and McDiarmid showed that 4 tau(H) <= n_H + m_H. Chvatal and McDiarmid also showed that 6 tau(H) <= 2 n_H + m_H. ... We show that if H does not contain a subhypergraph isomorphic to the affine plane AG(2,3) of order 3 with two vertices deleted, then 17 tau(H) <= 5 n_H + 3 m_H." Only constants 4/1/1, 6/2/1, 17/5/3 appear. No 11/3/2.
- Henning-Yeo, DAM 304 (2021) 12-22, "Lower bounds on Tuza constants for transversals in linear uniform hypergraphs" (https://pure.uj.ac.za/en/publications/lower-bounds-on-tuza-constants-for-transversals-in-linear-uniform/): about the best q_k in tau <= q_k (n+m) for k-uniform linear hypergraphs, large-k lower bounds. Not 3-uniform with extra hypotheses.
- Henning-Yeo, arXiv:1802.01825 (digest in kb/notes/henning_yeo_transversals.md): tau <= (n+m)/(k+1) for k = 2, 3 linear connected with equality iff E_k, AG(2,k) minus one or two points; 5 tau <= n + m for linear 4-uniform. Equality hypergraphs for k = 3 are F7, F8 (and the edge), i.e. exactly the obstruction removed in the 17/5/3 bound.
- Henning-Yeo, EJC 24(2) P2.50 (https://www.combinatorics.org/ojs/index.php/eljc/article/view/v24i2p50): Delta <= 2, k = 3: 18 tau <= 4n + 4m + 2. Different hypothesis (max degree 2).
- Strong transversals (Henning-Yeo, SIAM J. Discrete Math 2010, https://pure.royalholloway.ac.uk/files/6351130/090777001.pdf): 7 tau_s <= 4n + 2m. A different parameter (strong transversal number) and constants.
- Omega thread, the-omega-institute/trureturing issue #9804 (https://github.com/the-omega-institute/trureturing/issues/9804), re-fetched today (opened 24 Sep 2026 by @AlyciaBHZ, no comments visible, 0 votes). It contains: the refuted 21 tau(K) <= 9|R| + 5 e2 + 12 e1; the open candidate 7 tau(K) <= 3|R| + 2 e2 + 4 e1; the HY bound 17 tau <= 5n + 3m; A_0 = A_base with "12 AP edges and independence number 8"; "In a 16-point set, midpoint injectivity allows at most 14 APs"; "tight" sets e(S) = |S| - 2. It says: "The text does not contain an inequality of the exact form 11 tau <= 3n + 2m" (my reading of the fetch result; I also searched the digest in kb/notes/omega_issue_9804.md, which has none). Nothing on f(14), a census, or non-saturated 14-point sets. Its "tight set" language (e(S) = |S| - 2, closure under union/intersection when |U cap V| >= 2) is the same hereditary condition as (P3) of L007 but is used for a different purpose.
- erdosproblems.com/757 (https://www.erdosproblems.com/757): bounds 9/17 <= c <= 4/7 only, last edited 10 Apr 2026 (history page https://www.erdosproblems.com/history/757 shows two revisions, 2025-10-20 and 2026-04-10, both formatting/bounds only). Forum https://www.erdosproblems.com/forum/thread/757: 7 comments (Lin 8 Jan, Bloom 8 Jan, Tang 27 Feb, Tao 27 Feb, Sothanaphan x2 27 Feb, Tang 27 Feb); nothing on f(n), 14-point sets or transversal inequalities.

## Sources checked (2026-10-17)

| Source | URL / query | Result |
|---|---|---|
| erdosproblems 757 page | https://www.erdosproblems.com/757 | bounds only; "0 proof claims" |
| erdosproblems 757 history | https://www.erdosproblems.com/history/757 | two revisions, no new math |
| erdosproblems forum | https://www.erdosproblems.com/forum/thread/757 | 7 comments, none relevant |
| omega GitHub issue | https://github.com/the-omega-institute/trureturing/issues/9804 | see above; no 11/3/2 inequality, no 14-point classification |
| arXiv abs Ma-Tang | https://arxiv.org/abs/2602.23282 | v1, v2 only |
| arXiv PDF Ma-Tang | https://arxiv.org/pdf/2602.23282 | text streams not decoded by fetch tool (binary saved); cannot grep the body; relied on abs page, emergentmind summary and kb/notes/ma_tang_2026.md |
| emergentmind | https://www.emergentmind.com/papers/2602.23282 | no citing papers listed; no 11 tau inequality |
| arXiv author page Q. Tang | https://arxiv.org/a/tang_q_1 | 42 papers in 2026; only 2602.23282 is on Sidon subsets of (4,5)-sets; others (2605.02064, 2606.07428 multiplicative Sidon gaps) unrelated; no follow-up on #757 |
| arXiv API | export.arxiv.org/api/query | HTTP 301 / 429 (rate limited); not usable. Replaced by web search and listing/abs fetches |
| Semantic Scholar citations of 2602.23282 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23282/citations | empty data list (index lag or no citers) |
| arXiv 2609.23922 (Woo, Renyi stability of B_h sets) | https://arxiv.org/abs/2609.23922 | cited in the omega thread; about B_h sets, no (4,5)-sets, no transversals |
| arXiv 2005.07918 | https://arxiv.org/abs/2005.07918 | linear Turan number of 3-uniform hypergraphs; no tau inequality |
| arXiv 2512.24850 | https://arxiv.org/abs/2512.24850v1 | tau-critical 3-uniform hypergraphs, tau = 3 and at most 10 edges; unrelated to linear/F7 or Sidon |
| arXiv 2608.02667, 2604.25214, 2606.17487 | search results | Sidon subsets of multinomial coefficients; Sidon-extension counterexamples; large sieve for Sidon sets: unrelated |
| Web search (standard) x5 | "transversal linear 3-uniform 11 tau 3n+2m F7-free"; "Erdos problem 757 (4,5)-set 14-point exactly 12 three-term progressions extremal classification"; "Henning Yeo ... 5n+3m 17 tau 2022-2025"; "mathoverflow transversal ... |S|-2 edges"; "Henning Yeo book 3-uniform linear n-2 edges AP hypergraph 11 tau" | no source states 11 tau <= 3n + 2m; no source with the hereditary hypothesis e(S) <= |S| - 2; nearest hits are HY 2021 (17/5/3), HY 2018 (1802.01825), HY EJC 2017 (Delta <= 2), HY DAM 2021 |
| Web search (extended) | "arXiv 2026 Sidon subsets weak Sidon Ma Tang follow-up exact values extremal (4,5)-sets computer search f(n)" | only Ma-Tang, omega issue, unrelated Sidon papers; "no follow-up paper that computes exact values for (4,5)-sets" |
| Web search | "Gyarfas Lehel linear sets with five distinct differences cited by 2026" | nothing relevant (linear sets in PG(1,q^5) noise) |
| GitHub search (code/issues/repos for "ep757", "Erdos 757", "Sidon (4,5)-set") | gh search / gh api search | blocked by the sandbox (HTTP 403, repository-scoped only); only the omega issue and the Ma-Tang repo (https://github.com/QuanyuTang/ep757-45set-base-block-verification, A_base verification only, per earlier scouts L005/L006) were reached |
| MathOverflow | web search only (no direct query possible) | no thread found |
| Local digests | kb/notes/henning_yeo_2021_affine.md, henning_yeo_transversals.md, omega_issue_9804.md, ma_tang_2026.md, gyarfas_lehel_1995.md, kb/open_questions.md (Q6, Q8, Q11), earlier scouts L002/L005/L006 | consistent with the above; no digest mentions an 11/3/2 inequality; Q11 is the question L007 answers |

## What is known about 11 tau <= 3n + 2m (separate from the claim)

Published (what exists):
- [published] 4 tau <= n + m (Tuza 1990; Chvatal-McDiarmid 1992) and 6 tau <= 2n + m (Chvatal-McDiarmid), 3-uniform; equality cases for linear H by Henning-Yeo (JGT 59 (2008); DM 313 (2013)).
- [published] 17 tau <= 5n + 3m for linear 3-uniform H with no F7 (Henning-Yeo 2021, Thm 7 as cited by Ma-Tang Thm 5.3).
- [published] 18 tau <= 4n + 4m + 2 for linear connected 3-uniform with Delta <= 2 (EJC 2017).
- I found NO published or community statement of 11 tau <= 3n + 2m, in any hypothesis class, and no published transversal bound that uses a hereditary sparsity hypothesis e(S) <= |S| - 2. This hypothesis arises from the midpoint injectivity of AP hypergraphs (Ma-Tang Lemma 2.5); it is natural only in the #757 setting, which the Henning-Yeo reference list does not touch (kb/notes/henning_yeo_2021_affine.md: no reference to Gyarfas-Lehel, Sidon sets or AP hypergraphs).

Relation to the published bounds (derived from the L007 file and START_HERE, [derived-here], arithmetic only):
- I11 is NOT implied by 17 tau <= 5n + 3m: on the line m = n - 2 it reads 11 tau <= 5n - 4 against 17 tau <= 8n - 6, i.e. tau <= 0.4545n versus tau <= 0.4706n. If I11 held for all n on the class O it would give h >= (6n + 4)/11, i.e. c* >= 6/11 = 0.5454 > 9/17 = 0.5294, which would be goal (B). L007 proves I11 only for n <= 13 (Lemma A, computer-assisted) and only claims a consequence at n = 14; the claim does not assert the general inequality.
- I11 is tight on A_base ((n, m, tau) = (14, 12, 6): 66 = 66) and on a single edge (3, 1, 1: 11 = 11), so a general proof could not be improved at n = 14.
- Hypotheses are needed: per L007 Step 9.3, F7 itself violates I11 (21 + 10 = 31 < 33), and a linear F7-free (9, 8, 4) hypergraph with m > n - 2 violates it (43 < 44), so I11 fails on the plain Henning-Yeo class (linear, F7-free); it is a statement about the smaller class with (P3). Hence it cannot be a corollary of any theorem phrased for linear F7-free 3-graphs alone.
- Status: [conjecture] in general (only checked n <= 13 by L007, plus falsifier data on realizable sets); unproved in the literature.

## Related but different (not prior work)
- Tuza-type conjectures (triangle packing/covering; Tuza constants q_k in tau <= q_k (n + m)) concern different parameters (k-uniform, large k) or different objects (graphs, triangles); no 3-uniform linear bound with coefficients 3 and 2 appears.
- Chvatal-McDiarmid gives only 1/2 for #757 (kb/dead_ends.md).

## Limits and caveats
- Full text of Henning-Yeo 2021 (Graphs Combin.) and of the 2020 Springer book was not obtainable (closed access; see kb/notes/henning_yeo_2021_affine.md). A sharper lemma for restricted classes could sit inside them. Probability judged low: neither abstract mentions it, and the AP-hypergraph sparsity hypothesis is specific to #757.
- Google Scholar, MathSciNet and MathOverflow could not be queried directly; GitHub search and the arXiv API were blocked or rate-limited. Semantic Scholar returned no citers of Ma-Tang. Work citing Gyarfas-Lehel 1995 or Henning-Yeo 2021 was looked for via web search and the author page of Tang; none found. Also known (kb/notes/henning_yeo_2021_affine.md): only Ma-Tang and one 2022 paper on transversals of connected k-uniform hypergraphs (https://doi.org/10.1007/s40305-022-00445-1) cite HY 2021.
- The omega thread is live and can change after this scan.
- Novelty of the claim rests on the project's own censuses L004 and L005, which no outside source reproduces. The number 2,910 inherits the caveat of L004 (completeness re-checked only on 28% of prefixes). The weaker facts f(14) = 8 and "saturated 14-point sets with h = 8 exist" follow from Henning-Yeo plus A_base and are known (K24).
