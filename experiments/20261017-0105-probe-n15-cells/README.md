# Probe: cost of the class-O DFS census for n=15, alpha<=9, m=9 / m=10 (and m=11 / m=12)  [verified-here unless noted]

Question: can the exact C DFS (e757/c/ordered_dfs, prefix-split driver e757/ordered_dfs_split.py) exhaust (15, T=9, m=9) and
(15, 9, 10) on 4 cores in ~30 h? (If both cells are empty/unrealizable, a 16-point record would need m=14, max degree 3.)

## Method / commands (repo root, PYTHONPATH=.)
- `run_all.sh` -> `probe.py n T m nsample tl P`: lists depth-3 prefixes (`S.list_prefixes`), takes every k-th (k=N//nsample, offset k/2),
  runs `nice -n 5 ordered_dfs n=15 T=9 m_min=m m_exact=m f7=1 progress=0 refl=1 mode=enum pre=<prefix> tl=<s>`, 3 in parallel.
  Cells: m=9,10: 40 prefixes, tl=120 s; m=11,12: 10 prefixes, tl=60 s. Raw: raw_n15_T9_m*.json, log_m*.txt, probe_results.json.
  `tl` is WALL time under load (4 niced m=11 (14,8) DFS workers + this probe on 4 cores): measured 0.11-0.16 M nodes/s, vs 0.4-0.65 M/s unloaded.
- Whole-cell Knuth estimator (mode=estimate, 6000 probes, seeds 1,2; estimates_m9_m10.txt).
- Realizability of saved patterns: realize_samples.py (e757.realizability.realize_exact; n=15 with m<13 is not rigid so fastreal does not apply).

## Results
| cell | depth-3 prefixes | sampled | timed out | nodes (sampled, lower bound) | solutions | probe CPU-s | rate nodes/s |
|---|---|---|---|---|---|---|---|
| (15,9,9)  | 4592 | 40 | 40 (100%) | 6.3e8 | 0 | 4801 | 1.3e5 |
| (15,9,10) | 4592 | 40 | 40 (100%) | 5.4e8 | 0 | 4802 | 1.1e5 |
| (15,9,11) | 4591 | 10 | 10 (100%) | 7.9e7 | 870 | 600 | 1.3e5 |
| (15,9,12) | 4518 | 10 | 10 (100%) | 9.4e7 | 94,500 | 600 | 1.6e5 |

Not a single sampled prefix finished within the time limit, so per-prefix cost is only bounded below (>= 1.3e7 nodes at m=9, i.e. > 120 s loaded).
The naive extrapolation from timeouts (mean nodes x prefixes) is a LOWER bound of only 6-7e10 nodes; it is useless. The estimator is the
meaningful number:
- Knuth estimator, whole cell: (15,9,9): 8.4e13 +- 0.9e13 and 7.8e13 +- 1.2e13 calls; (15,9,10): 8.4e13 +- 0.9e13 and 7.1e13 +- 0.8e13 calls
  (surviving nodes ~7-8e12). [heuristic; for calibration it gave 1.04e11 for (14,12,8) vs actual 1.13e11, and 1.8e8 for (12,10) vs 1.87e8.]
- => about 8e13 nodes per cell. At 0.4-0.65 M nodes/s unloaded: 1.2-2e8 CPU-s = 35,000-55,000 CPU-h per cell (~9,000-14,000 h on 4 cores, 1-1.5 years).
  Extrapolated pattern count: unknown (0 observed in the 80 sampled prefixes, all unfinished).
- Cost vs (14,12,8) (277,501 CPU-s, 1.13e11 nodes): about 700-800x more nodes.

Growth with m: the m=11 and m=12 probes also time out on every prefix, with node counts per prefix similar to m=9/10 (same order, 1e7-1e8 per 60-120 s),
and the estimator gives essentially the same total for m=9 and m=10 (alpha<=9 is a weak prune at n=15; the cost is in the m-independent search over the staircase).
I did not run the estimator for m=11,12.

Patterns found in probes (partial, unfinished prefixes):
- m=9, m=10: none (0 of 80 prefixes' partial searches). Nothing to realize. This says nothing about exhaustiveness.
- m=11: 870 abstract patterns saved (samples/); 200 random ones tested with realize_exact: 84 REALIZABLE, 99 order-infeasible, 14 forced repeated difference, 3 forced extra AP.
- m=12: 94,500 saved; 200 tested: 11 realizable, 187 order-infeasible, 1 + 1 other.
  (realiz_m11.json / realiz_m12.json hold up to 20 realized sets each.) A realized pattern is a 15-point (4,5)-set with AP set equal to the pattern and h = alpha <= 9,
  hence h = 9 = f(15): extremal, not record-beating (15 -> 9 >= 4*15/7). These sets were not run through new_claim.py (they are not claims). So 15-point extremal sets
  with only 11 or 12 APs DO exist [verified-here by realize_exact, exact arithmetic; not independently refereed], which makes the m=9/10 cells not obviously empty:
  the hoped-for "no realizable pattern" is not supported or refuted by this probe.

## Conclusion
Feasible on 4 cores within 30 h? **NO for both cells** (m=9 and m=10): estimated ~8e13 nodes each, ~4-5e4 CPU-h, i.e. ~300-400x beyond a 120 CPU-h budget
(and 100% of sampled prefixes exceed 120 s even at depth 3). Needs ~400x pruning (a stronger bound than alpha look-ahead + Henning-Yeo deletion constraints,
e.g. imposing the max-degree/HY vertex-deletion constraints of Lemma Delta as DFS prunes, or a deeper split with an incremental realizability/order-LP prune) before the
cell approach is viable. Caveat: loaded-machine rates; timeouts are lower bounds; estimator variance ~10-15%.

Status update (2026-10-17, later the same day) [derived-here]: the question this probe asked is moot, and the remark above that the m = 9/10 cells are "not obviously empty" is superseded. Inequality I11 (11 tau <= 3n + 2m; slack s = 3n + 2m - 11 tau) holds for every 3-graph in the class O+ (linear, F7-free, e(S) <= |S| - 2 for all S with |S| >= 2; the AP hypergraph of every (4,5)-set lies in O+) with n <= 15: results/proofs/L008-f16-equals-10.md, Lemma A' (Step 1 window cells, Step 2.4), ACCEPTED by three referees. The two window cells that matter here, (n,m,tau) = (15,9,6) and (15,10,6) (I11 slack -3 and -1), are empty: conn_dfs2 finds no connected linear 3-graph there (2,459,440 and 186,011,577 nodes, found = 0; experiments/falsify/i11-inequality/README.md section 2), re-checked by enum_conn, nauty genbg and further generators in the L007/L008 referee rounds. These two cells were an uncertified remark of L007 (Step 9.1, computation C6) and are certified as part of L008 Lemma A'. Hence no 15-point (4,5)-set with h <= 9 has exactly 9 or 10 three-term APs, and the DFS cells (15, alpha <= 9, m = 9) and (15, alpha <= 9, m = 10) of this probe are empty even as abstract patterns, so they never needed to be exhausted; the cost estimates above remain only a record of what exhausting them by DFS would have cost [heuristic]. The m = 11 and m = 12 patterns realized here are instances of the non-saturated extremal 15-point sets recorded in K50 (kb/known_results.md; kb/dead_ends.md D25); K50's catalogue (data/ext15_sets.jsonl.gz) comes from the later experiments/20261017-0210-ext15-hunt, not from this probe.
