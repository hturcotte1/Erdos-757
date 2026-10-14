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

| 2026-10-14 | K30-K31 | Monotone midpoints; no medial triangle (exact lemmas with one-line proofs) | kb/known_results.md, experiments/20261013-2257-forbidden-library |
| 2026-10-14 | K32-K33 | Census of ordered midpoint patterns n<=8 (46,281 at n=8) and 287 minimal forbidden cores; catalogue of all <=4-edge configurations; independently re-derived (ACCEPT) | data/forbidden_ordered_n7.json, data/forbidden_ordered_n8.json, experiments/20261014-0005-forbidden-n8, experiments/referee/catalogue-n8 |
| 2026-10-14 | K34 | Q8 inequality holds on all 3^n states of the 7 records and ~570M sampled states; two independent implementations agree | experiments/falsify/q8-omega-inequality, experiments/referee/q8 |
| 2026-10-14 | K35-K36 | f(n)=ceil(n/2)+1 for 6<=n<=15,17 (= HY bound for n<=23); abstract class O' GL-tight at even n<=14 and equal to the realizable extremal values in all resolved cells | experiments/20261013-2257-chyp-table, experiments/20261014-0500-slack-landscape |
