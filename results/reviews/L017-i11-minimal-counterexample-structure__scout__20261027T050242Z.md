NOVELTY: KNOWN

# Scout report: novelty of L017 (structure of a minimal I11 counterexample; Theorem 7 = I11 for Delta <= 2)

Checked 2026-10-27 (UTC, about 05:00-05:15). Scope: results/proofs/L017-i11-minimal-counterexample-structure.md, Theorem 7 and the Hall-lemma / Hall-deficient-pattern device. I11 means 11 tau <= 3n + 2m.

Verdict by item:
- (1) Theorem 7 (I11 for linear 3-graphs with max degree <= 2): KNOWN as a statement. The method (tau(H) = m - nu(dual graph), then a lower bound on the matching number of a graph of bounded degree) is the published method of Henning-Yeo EJC 24(2) P2.50. The special bound 11 nu >= 3|E| for subcubic graphs also follows from Chvatal-Hanson (1976). What may be new is only the self-contained Tutte-Berge proof and the slack identity s(H) = 3 n_0 + 11 nu(G) - 3|E(G)|. I found no source stating I11 itself, so the form "11 tau <= 3n + 2m" is not in the literature I could reach.
- (2) Structure theorem, Hall lemma for low-slack blocks: the device is STANDARD and modelled on Henning-Yeo arXiv:1802.01825 Section 7 (Claims D-F). The application to this inequality and class C is new, but it is not a new technique. (I read only the saved Section 7 excerpt for this; I did not find any paper applying it to I11.)
- (3) Nothing new on Erdos #757 since 2026-10-20 that I could find. The only post-Ma-Tang item is the anonymous reader's 5/9 page, which this project already knows (C003, K59/K60). Nothing about 6/11 or I11 anywhere.

## 1. Theorem 7 versus the literature

### 1a. What L017 states
For a linear 3-graph H with Delta(H) <= 2 and n_0 isolated vertices, with G its dual graph (vertices = edges of H, one edge of G per degree-2 vertex of H): tau(H) = m - nu(G); s(H) = 3n + 2m - 11 tau = 3 n_0 + 11 nu(G) - 3|E(G)|; every simple G with Delta(G) <= 3 has 11 nu(G) >= 3|E(G)|, with equality only if E(G) is empty. So I11 holds for Delta <= 2 (L017 Step 4, 4.1-4.5).

### 1b. Henning-Yeo, EJC 24(2) (2017) P2.50: the method and the k = 3 case
Source (full text obtained and read, pdftotext copy only in the scratchpad): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v24i2p50 , PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i2p50/pdf . DOI 10.37236/6160. Henning and Yeo, "Transversals and Independence in Linear Hypergraphs with Maximum Degree Two", Electron. J. Combin. 24(2) (2017), #P2.50.

Quotes from the paper:
- Abstract: "Let H_k be the class of all connected, linear, k-uniform hypergraphs with maximum degree 2. It is known [European J. Combin. 36 (2014), 231-236] that if H in H_k, then (k + 1) tau(H) <= n + m ... if k >= 3 is odd and H in H_k has n vertices and m edges, then we prove that k(k^2 - 3) tau(H) <= (k - 2)(k + 1) n + (k - 1)^2 m + k - 1".
- Section 3.1 defines exactly L017's dual graph: "Let the vertices of G_H be the edges of H and let the edges of G_H correspond to the n_2(H) vertices of degree 2 in H ... By the linearity of H, the multigraph G_H is indeed a graph, called the dual graph of H."
- Proposition 9: "If H in H_k and G_H is the dual graph of H, then alpha'(G_H) = |E(H)| - tau(H)." The paper says it is "well-known (see, for example, [7])" and gives a short proof. This is L017's identity tau = m - nu(G) (L017 4.2). The paper cites [7] (reference list item 7 is not identified here; I did not check it).
- Theorem 14 (proof): from Prop. 9 and a matching-number bound for connected graphs of maximum degree <= k ("Theorem 3 ([19])", Henning-Yeo, "Tight lower bounds on the matching number in a graph with given maximum degree", arXiv:1604.05020), they get, for k odd, k^2 (k^2-3) tau <= k(k-2)(k+1) n + k(k-1)^2 m + k(k-1).

For k = 3 this is 18 tau <= 4n + 4m + 2 for connected linear 3-graphs with Delta <= 2. This matches the K10 entry already in kb/known_results.md and L017 Remark 4.6(a).

Does I11 for Delta <= 2 follow from this known theorem? Yes [derived-here, checked now]:
- Take a component H' of H. If H' is a single edge (n = 3, m = 1, tau = 1) then 11 <= 9 + 2 holds with equality. If H' is one vertex, then 0 <= 3. Otherwise a linear component with at least 2 edges has n >= 5 and 3m = n_1 + 2 n_2 <= 2n, so m <= 2n/3. Then 8m + 22 <= 10 n holds (16n/3 + 22 <= 10n iff n >= 4.7), and 11(4n + 4m + 2) <= 18(3n + 2m) iff 8m + 22 <= 10n, so 11 tau <= (11/18)(4n + 4m + 2) <= 3n + 2m.
- tau, n, m are additive over components, so I11 follows for every linear 3-graph with Delta <= 2. This agrees with L017 Remark 4.6(a).

Conclusion: Theorem 7 is KNOWN as a statement (a corollary of HY EJC 2017, Theorem 14 with k = 3, plus a two-line component computation). Stronger known bound: for Delta <= 2 the HY inequality 18 tau <= 4n + 4m + 2 is sharper at the relevant ratios than I11. L017's proof is a different, self-contained proof of the weaker I11, via Tutte-Berge. The identification tau = m - nu(dual graph) is explicitly "well-known" in the paper.

### 1c. Chvatal-Hanson: the subcubic matching inequality is classical
L017 4.4 proves 11 nu(G) >= 3|E(G)| for simple G with Delta(G) <= 3 by Tutte-Berge. The Chvatal-Hanson theorem (V. Chvatal, D. Hanson, "Degrees and matchings", J. Combin. Theory Ser. B 20 (1976) 128-138) gives, for a graph with maximum degree Delta >= 1 and matching number nu >= 1, |E| <= f(nu, Delta) = nu*Delta + floor(Delta/2) * floor(nu / ceil(Delta/2)). This is as quoted in a secondary source (arXiv:1610.00815, found by web search; I did NOT check it against the 1976 paper itself, and the original is paywalled). For Delta = 3: |E| <= 3 nu + floor(nu/2) <= 3.5 nu. Then 2|E| <= 7 nu, and 7/2 < 11/3, so 3|E| <= 11 nu follows [derived-here, assuming the quoted formula]. Equality 11 nu = 3|E| forces |E| = 0. The extremal value 3 nu + floor(nu/2) = 7 at nu = 2 matches L017 Remark 4.6(b) (K_4 with a subdivided edge, 7 edges, nu = 2, 11 nu - 3|E| = 1). Also: Balachandran and Khare, Discrete Math. 309 (2009) 4176-4180 (named as the second source for the general-graph case in the search snippet). So the graph-theoretic core of Theorem 7 is classical.

### 1d. Other Delta <= 2 results
- Dorfling and Henning, "Linear hypergraphs with large transversal number and maximum degree two", European J. Combin. 36 (2014) 231-236: (k+1) tau <= n + m for Delta <= 2 (per the HY abstract and arXiv:1802.01825 Thm 3 in kb/notes/henning_yeo_transversals.md). For k = 3 this is 4 tau <= n + m, which does NOT imply I11: it would need 3m <= n, false for Delta = 2 (3m <= 2n only). The HY 2017 bound is the relevant one.
- Chvatal-McDiarmid (Combinatorica 12 (1992) 19-26): 4 tau <= n + m and 6 tau <= 2n + m for 3-uniform; not accessed (paywalled; known from kb). Not implying I11 for Delta <= 2 either.
- No source I found states "11 tau <= 3n + 2m" for any class.

## 2. The structure theorem (Hall lemma, Hall-deficient patterns)
- Source checked: kb/literature/sources/henning_yeo/henning_yeo_1802.01825_sec7_deficiency.txt (excerpt of Henning-Yeo, "Transversals in Uniform Linear Hypergraphs", arXiv:1802.01825, https://arxiv.org/abs/1802.01825 , Section 7). Quotes:
  - Section 7.3 sets up the bipartite graph G_X between the special sets X and the outside edges E*(X) ("An edge joins e in E*(X) and H' in X in G_X iff the edge e intersects the subhypergraph H' of X in H").
  - Claim D (proof): "Suppose there exists a matching, M, in G_X that matches E*(X) to a subset of X. Then, by Observation 1(g), there exists a minimum X-transversal, T, that intersects every edge in E*(X), contradicting Claim B. Therefore, no matching in G_X matches E*(X) to a subset of X. By Hall's Theorem, there is a nonempty subset S in E*(X) such that |N_{G_X}(S)| < |S|. We now consider the special H-set X' = X \ N_{G_X}(S) ...".
  - Claims E and F then give def(H) = 0 by a minimal-counterexample count |E*(X)| - |X| minimum.
- L017's Lemma H (Step 3, 3.1-3.2) is the same device: a bipartite graph between blocks W_i / F_i and outside edges E*, an injective map from E* ruled out by "each block has a minimum transversal containing the chosen vertex", so Hall yields a deficient set. The role of "Observation 1(g)" is played by L017's condition (U). L017 adapts it from 4-uniform special hypergraphs to low-slack induced blocks of I11. The same "Hall's theorem plus minimal counterexample" pattern also appears in Thomasse-Yeo (Combinatorica 27 (2007) 473-487, saved text kb/literature/sources/henning_yeo/thomasse_yeo_2007_combinatorica.txt) and Henning-Yeo arXiv:1504.02650 (saved).
- Verdict: L017 should say explicitly that Lemma H and the Hall-deficient patterns are modelled on Henning-Yeo arXiv:1802.01825 Section 7 (Claims D-F). The specific lemmas (U), (R+), the pair-distribution patterns in Theorem 4/5 are specific to I11 and I found no prior statement of them. I did not have access to the 2021 HY Graphs Combin. paper (17 tau <= 5n + 3m), which presumably uses a similar technique (kb/notes/hy_proof_technique.md says its full text is not obtained), so overlap with that paper's internals cannot be excluded.

## 3. Anything new on Erdos #757 since 2026-10-20
Checked:
- https://www.erdosproblems.com/757 : fetched 2026-10-27; still lists only Erdos-Sos c >= 1/2, Gyarfas-Lehel [GyLe95], Ma-Tang [MaTa26] 9/17 <= c <= 4/7; "last edited 10 April 2026"; no 5/9, no 6/11, no I11. 7 comments.
- https://www.erdosproblems.com/forum/thread/757 : fetched 2026-10-27; 7 comments, all 8 Jan 2026 to 27 Feb 2026 (Lin, Bloom, Tang, Tao, Sothanaphan). Nothing on 5/9, self-similar constructions, linear hypergraphs, Henning-Yeo, or any later date.
- https://www.erdosproblems.com/history/757 : appeared in search results (not fetched separately).
- https://erdosproblemaday.com/day/757-reader-five-ninths-refereed : fetched 2026-10-27. Dated 19 Oct 2026; anonymous reader submission of 17 Oct (ID 7bkzb8); page status PARTIAL; "Unreviewed by humans"; claims c <= 5/9 via an 11 + 9K point family with Sidon number 7 + 5K, K = 6 gives 37/65; states the lower bound 9/17 is unchanged. No mention of I11 or 6/11. (Already known to this project.)
- arXiv: Ma-Tang https://arxiv.org/abs/2602.23282 (v2 6 Mar 2026). Web search for follow-ups, "5/9", "6/11", "weak Sidon", "(4,5)-set": nothing newer. Search "citing Ma-Tang / Gyarfas-Lehel": no citing work found (the search engine returned no hits; Semantic Scholar API citations endpoint for arXiv:2602.23282 returned an empty list, which may only mean the paper is not indexed). An arXiv API query returned nothing usable.
- Henning-Yeo 2021 (Graphs Combin. 37, 867-890), web search for follow-ups to "17 tau <= 5n + 3m" and "3n + 2m" / "11": only the 2021 paper and its UJ record https://pure.uj.ac.za/en/publications/affine-planes-and-transversals-in-3-uniform-linear-hypergraphs/ ; nothing citing it with an improvement. arXiv:2512.24850 (R. Li, 3-critical 3-graphs of minimum degree 7) came up and is unrelated.
- MathOverflow: web search for the combination (transversal, linear 3-uniform, F7 / AG(2,3), Sidon, five distinct differences): no MathOverflow thread found.
- GitHub: BLOCKED. `gh search issues` (GraphQL) and `gh search code` were refused by the agent proxy (403, "sessions are bound to their configured repositories"). The previously known GitHub items (the-omega-institute/trureturing #9804, TheJustinSunPrize/awards #49, grandchallenge/MATH-PROGRAMME #2028, formal-conjectures 757.lean) are listed in kb/literature/bibliography.md; their current state was NOT re-checked in this run, so a recent GitHub issue mentioning "Erdos 757" cannot be excluded.
- Semantic Scholar / Google Scholar snippets: only the web-search snippets above; no Google Scholar page was fetched.
- Not accessed: Springer page for HY 2021 and the 2020 book, Chvatal-Hanson 1976 and Chvatal-McDiarmid 1992 originals (paywalled), the saved-text caveat above.

## 4. Recommendations for L017 (for the orchestrator)
1. State in L017 that Theorem 7 is a corollary of HY EJC 2017 Thm 14 (k = 3) after the component computation, and that tau = m - nu(G) is HY Prop. 9 ("well-known"); present the Tutte-Berge proof as a self-contained alternative, and mention Chvatal-Hanson (|E| <= 3 nu + floor(nu/2) for Delta <= 3) as the classical source of 4.4. Currently 4.6(a) mentions only K10 as a "cross-check", which undersells the overlap.
2. Add the HY arXiv:1802.01825 Section 7 attribution for the Hall lemma (Claim D) and for the "minimal counterexample with |E*(X)| - |X| extremal" pattern.
3. Label the novelty precisely: the new content is the application to I11 on class C (the structure results of Theorems 1-6), not Theorem 7.
4. Add this paper to kb/literature/bibliography.md (HY EJC 2017 is already there; the Chvatal-Hanson entry already exists; Dorfling-Henning 2014 too). Nothing needs adding except the Balachandran-Khare 2009 reference and arXiv:1604.05020 (HY, "Tight lower bounds on the matching number in a graph with given maximum degree"), which underpins HY EJC Thm 14.
