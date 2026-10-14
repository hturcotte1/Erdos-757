# LP fit of transversal inequalities on realizable AP hypergraphs (Track L preparation)

Question: on a large dataset of exactly realizable (4,5)-set AP hypergraphs, what are the best inequalities
tau <= a n + b m + c.f ? Which configurations are Henning-Yeo (HY) near-tight? (kb/methods/proof_and_inequality_testing.md steps 2-3)

## Method
- `generate.py` (seed 757; ~13 min; stats in `generate_stats.json`; its console log was overwritten by the later `fit.py` job in `run.log`).
  Rows are deduplicated up to affine equivalence (translate, scale by gcd, reflect). Each row stores the integer point set and exact features
  (alpha by `e757.saturated.alpha_of_edges`, tau = n - alpha, edge list recomputed inside the subset).
  - (a) ALL induced subsets with >= 6 points of A_base, the 12-point sets (3), and the n=8,10,11 records.
  - (b) random saturated (4,5)-sets (`e757.anneal.random_linear_map` + exact `evaluate`, is45 required): 500 each at n=10,12,14,16,18
    (acceptance 500/1184, 1632, 1989, 2521, 2716 tries) and 4496 at n=20 (600 s), plus <= 200 random induced subsets (6..n-1 points) of each.
  - Total 1,333,217 rows (35 MB, `dataset.jsonl.gz`). Keys: n m e tau alpha non_mid d0 d1 d2 d3 d4p mid_end2 edges_mid_deg1 parent_only slack D maxdeg comps saturated edges_list set src.
  - "mid_end2" = vertices that are the midpoint of an edge and endpoints of >= 2 edges.
- `fit.py` -> `fit_output.txt` (full text), `analysis.json`. LPs by scipy HiGHS (floats, [heuristic]); each fitted inequality re-verified on every row
  with Fractions after rounding coefficients to denominators <= 1000 (all violations = 0). Rows with identical (n,m,saturated,features) are compressed to max tau (same feasible set).
- Command: `python3 experiments/20261014-0020-lp-fit/generate.py` then `python3 experiments/20261014-0020-lp-fit/fit.py > fit_output.txt`.
- Caveat on interpretation: all features and tau are additive under the disjoint union (gluing makes the AP hypergraph a disjoint union), so a
  homogeneous inequality (no constant) valid on the rows is automatically valid on all glued sets. Saturation (m = n-2) is NOT preserved by gluing
  (non_mid = 2 per glued piece), so "a+b per vertex in the saturated regime" is only valid for connected pieces.
  Constant-term fits are not closed under gluing and carry no asymptotic information (n <= 20 only).

## 1. Henning-Yeo [verified-here]
- Rows with slack = 5n+3m-17tau < 0: **0** of 1,333,217. Also D = slack + 3(n-m) holds on every row. Global min slack 2 (only n=6 rows: two disjoint APs; trivial).
- Min slack by n (all rows / saturated rows): n=8: 4/7, n=9: 3/15, n=10: 3/6, n=11: 5/14, n=12: 4/5, n=13: 4/13, n=14: 4/4, n=15: 5/12, n=16: 11/20, n=17: 13/28, n=18: 16/19, n=19: 18/27, n=20: 35/35.
  (n >= 16 minima only reflect random sets, not extremal ones.)
- Near-tight rows with n >= 10: slack 3: 28 rows (all n=10, m=7, tau=4: induced 10-subsets of A_base and of the 11/12-point records);
  slack 4: 16 rows (including A_base itself n=14 m=12 tau=6, A_base minus its maximum-or-minimum point n=13 m=8 tau=5, and trivial disjoint-AP configurations);
  slack 5: 31 rows (the three 12-pt sets, two random 12-pt sets rand12, 11-subsets of A_base, ...). Full top-20 list with sets in `fit_output.txt` / `analysis.json`.
  Only 6 of the 75 rows with slack <= 5, n >= 10 are saturated. No row with n >= 16 has slack < 11.

## 2. LP fits [heuristic fits; inequality validity on all rows is verified-here]
(2a-2c in `fit_output.txt`; n.b. 'tight extremal' counts distinct feature keys, so the three 12-pt sets count once.)
- **Plain fit tau <= a n + b m (min a+b):** a=3/7, b=0, a+b=3/7, i.e. alpha/n >= 4/7. The single tight row is A_base (n=14,m=12,tau=6). I.e. the dataset is consistent with tau <= 3n/7 and nothing beats it. [verified-here for validity on the rows]
- **Exact frontier a(b) = max_rows (tau - b m)/n** (every row checked with Fractions):
  b=0: a=3/7 (A_base tight); b=1/17: 45/119; b=2/17: 39/119; b=3/17: **33/119** (< HY's 5/17 = 35/119; a+b = 0.4538 vs HY's 8/17 = 0.4706), still tight only at A_base;
  for b >= 1/4 the trivial rows (n=3k, m=k... two-AP pieces with tau=m) take over and a+b grows. So HY's constants have 2/119 headroom in `a` on this dataset, at b=3/17, with m <= n-2 giving alpha/n >= 0.5462.
- **Feature fits with non_mid, degrees, comps, mid_end2, parent_only, edges_mid_deg1** (homogeneous, all c_i >= 0): minimising the literal objective a+b is **degenerate**: with n <= 20 data, features such as non_mid (coefficient 3.5), d2/d1 (3,1), comps (7) absorb everything and give a=b=0, so the naive "1-a-b" ratio is meaningless (reported in 2a for completeness).
  Fits that do not collapse: `mid_edge_deg1` (a=3/7, coefficient 0: the feature does not help), `d3+d4p` (a=3/8, c=1/4,1/4; tight at 3 keys).
- **Tightest valid inequality** (objective: minimise total slack on the 7 full extremal sets, 2b): e.g. tau <= 0.2727 n + 0.1818 m (= 3n/11 + 2m/11), and with d-features tau <= (1/3) n + 0.065 d2 + 0.106 d3 + 0.244 d4p; at most 2 extremal keys tight simultaneously, none of the fits makes A_base and the 12-pt sets simultaneously tight except the plain one (3n/11+2m/11 is tight at 1/5).
- **non_mid family with an honest asymptotic readout (2e):** for tau <= a n + b m + c.non_mid and x = non_mid/n, worst case W = max_x min(a+b+(c-b)x, 1-x) (using tau <= m). Best over a grid: W = 3/7 at (a,b,c) = (3/7,0,0); every other grid point is worse (e.g. 0.4296 at (45/952, 13/34, 3/8)). So non_mid does not improve the fit.
- Conclusion: on this data no feature-augmented inequality beats tau <= 3n/7 (equivalently alpha >= 4n/7), and A_base is the unique tight row for slopes a+b <= 0.4538. The data cannot discriminate between candidate inequalities with slope in (3/7, 8/17) because every extremal piece is A_base-like; any proof must use the exact structure of A_base.

## 3. D = 17h - 9n on random saturated sets [verified-here]
| n | #sets | D min | D median | D max | min h | #D/n<5/7 | #h<4n/7 |
|---|---|---|---|---|---|---|---|
| 10 | 500 | 12 | 29 | 29 | 6 | 0 | 0 |
| 12 | 500 | 11 | 28 | 45 | 7 | 0 | 0 |
| 14 | 500 | 27 | 27 | 44 | 9 | 0 | 0 |
| 16 | 500 | 26 | 43 | 60 | 10 | 0 | 0 |
| 18 | 500 | 25 | 42 | 76 | 11 | 0 | 0 |
| 20 | 4496 | 41 | 58 | 75 | 13 | 0 | 0 |
Random saturated (4,5)-sets are far from extremal (D >= 25 for n >= 14; the n=10,12 minima 12 and 11 are the known extremal sets found at random).
No row in the whole dataset has D/n < 5/7 (min D/n = 5/7, attained only by A_base). No new claim was produced.

## 4. Local structure of near-tight rows (slack <= 5, n >= 10; 75 rows) [verified-here counts]
Roles at a vertex v of degree >= 3: L = left endpoint, M = midpoint, R = right endpoint of an edge through v.
- deg 3: LMR 32, LLM 25, MRR 21, LLL 13, RRR 7, LLR 1, LRR 1; deg 4: LLLL 2, LLMR 3, MRRR 2. No vertex has two M roles (midpoint map injective).
- By slack: slack 3: LLM 14, LMR 13, MRR 10, LLL 4, RRR 3, LRR 1, deg4 LLLL/LLMR/MRRR 1/1/2. slack 4: LLM 3, LMR 3, MRR 2, LLLL 1. slack 5: LMR 16, LLL 9, MRR 9, LLM 8, RRR 4, LLR 1, LLMR 2.
- Degree-profile (d0,d1,d2,d3,d4p) most common: (0,1,7,2,0) x21, (0,5,5,1,0) x17, (0,12,0,0,0) x14 (n=12: four disjoint APs, a trivial tight configuration with m=tau=4), (0,4,7,0,0) x8. No isolated vertices in any near-tight row; vertices of degree >= 3 usually have 0-1 or 4-5 neighbours of degree >= 3 (i.e. they come in clusters or alone).
- A_base (slack 4): deg-4 vertex 0 with roles LLLL (leftmost point, APs 0-136-272, 0-200-400, 0-298-596, 0-528-1056); degree-3 vertices 200, 246 (LLM), 249, 272 (LMR), 298, 400 (MRR). Edge list in `fit_output.txt`.
- Observation [heuristic]: in near-tight rows the high-degree vertices are the extremes of dilated families (all-L at the minimum, all-R at the max) and the LMR/LLM/MRR pattern shows high degree comes mostly from endpoint roles, one midpoint role at most.

## Files
`dataset.jsonl.gz`, `generate.py`, `generate_stats.json`, `fit.py`, `fit_output.txt`, `analysis.json`, `run.log`.
