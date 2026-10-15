# LEDGER: verified results only

Add a row only after the verify-claim skill completes. Each row needs an evidence path.

| Date (UTC) | ID | Result | Tag | Evidence |
|---|---|---|---|---|
| 2026-03-06 | baseline-upper | $c_*\le4/7$: $A_{\rm base}$, $n=14$, $h=8$ | [published] Ma–Tang | tests/fixtures/C000-abase.json, `test_abase` |
| 2026-03-06 | baseline-lower | $c_*\ge9/17$ | [published] Ma–Tang + Henning–Yeo | kb/00_START_HERE.md §2 |
| 2026-10-13 | small-f | Exact $f(n)$ for $n\in\{1..7,9,11..15,17,24,26,28\}$ | [derived-here] | e757/fn_bounds.py, `test_fn_bounds` |
| 2026-10-13 | hy-feasible | Beating 4/7 impossible for $n\le15$ and $n\in\{17,19,21,24,26,28\}$ | [derived-here] | e757/fn_bounds.py, `test_hy_feasibility` |
| 2026-10-13 | f8-f10 | $f(8)=5$, $f(10)=6$; so $f(n)$ is exact for all $n\le15$ | [verified-here] | data/small_records.json, `test_small_records` |
| 2026-10-13 | chains | Periodic chain constructions have density ≥ 3/5 (all tested cases) | [verified-here] | e757/chains.py, `test_chain_densities` |

| 2026-10-14 | K30-K31 | Monotone midpoints; no medial triangle (exact lemmas with one-line proofs) | [verified-here] | kb/known_results.md, experiments/20261013-2257-forbidden-library |
| 2026-10-14 | K32-K33 | Census of ordered midpoint patterns n<=8 (46,281 at n=8) and 287 minimal forbidden cores; catalogue of all <=4-edge configurations; independently re-derived (ACCEPT) | [verified-here] | data/forbidden_ordered_n7.json, data/forbidden_ordered_n8.json, experiments/20261014-0005-forbidden-n8, experiments/referee/catalogue-n8 |
| 2026-10-14 | K34 | Q8 inequality holds on all 3^n states of the 7 records and ~570M sampled states; two independent implementations agree | [verified-here] (evidence, not proof) | experiments/falsify/q8-omega-inequality, experiments/referee/q8 |
| 2026-10-14 | K35-K36 | f(n)=ceil(n/2)+1 for 6<=n<=15,17 (= HY bound for n<=23); abstract class O' GL-tight at even n<=14 and equal to the realizable extremal values in all resolved cells | [verified-here] | experiments/20261013-2257-chyp-table, experiments/20261014-0500-slack-landscape |
| 2026-10-14 | L001 | No 2-point (4,5) extension of A_base has h <= 9 (all 1,743 non-generic (4,5) extension pairs and all generic cases have h = 10); K13 upgraded from [community] | [verified-here] (certificate; referee ACCEPT after 4 rounds, 4 independent methods) | results/proofs/L001-abase-two-point-extensions.md; results/reviews/L001-abase-two-point-extensions__referee__20261014T095734Z.md |
| 2026-10-14 | K41/L002 | Exactly 54,243 twelve-point (4,5)-sets with h=7 up to affine equivalence (exhaustive C-DFS over class O, 2,226,490 patterns at m=10, none at m=9; exact realization; judge spot check) | [verified-here] (certificate L002, referee ACCEPT after 3 rounds, 4 independent pipelines) | experiments/20261014-1005-census-dfs/README.md; results/proofs/L002-census-12-point-extremal-sets.md |
| 2026-10-14 | K43/L003 | Up to affine equivalence: saturated extremal classes for n=6..11 are 1, 4, 66, 1262, 6644, 466961; infinitely many extremal sets for 4<=n<=11 (non-saturated families), one class for n<=3, and n=12 is the smallest n>=4 with finitely many (54,243) | [verified-here] (certificate L003, referee ACCEPT after 3 rounds) | experiments/20261014-1430-small-counts/README.md; tests/test_small_counts.py |
| 2026-10-15 | K45/L004 | Exactly 2,910 saturated 14-point (4,5)-sets with h=8 up to affine equivalence (A_base among them); m=11 case open | [verified-here] (certificate L004, referee ACCEPT; realization fully independent, completeness re-checked by sampling plus consistency checks) | experiments/20261014-1005-census-dfs/n14/results/post/summary.json; results/proofs/L004-census-14-point-extremal-sets.md |
