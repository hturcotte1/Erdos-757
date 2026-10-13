# LEDGER: verified results only

Add a row only after the verify-claim skill completes. Each row needs an evidence path.

| Date (UTC) | ID | Result | Tag | Evidence |
|---|---|---|---|---|
| 2026-03-06 | baseline-upper | $c_*\le4/7$: $A_{\rm base}$, $n=14$, $h=8$ | [published] Ma–Tang | tests/fixtures/C000-abase.json, `test_abase` |
| 2026-03-06 | baseline-lower | $c_*\ge9/17$ | [published] Ma–Tang + Henning–Yeo | kb/00_START_HERE.md §2 |
| 2026-10-13 | small-f | Exact $f(n)$ for $n\in\{1..7,9,11..15,17,24,26,28\}$ | [derived-here] | e757/fn_bounds.py, `test_fn_bounds` |
| 2026-10-13 | hy-feasible | Beating 4/7 impossible for $n\le15$ and $n\in\{17,19,21,24,26,28\}$ | [derived-here] | e757/fn_bounds.py, `test_hy_feasibility` |
| 2026-10-13 | chains | Periodic chain constructions have density ≥ 3/5 (all tested cases) | [verified-here] | e757/chains.py, `test_chain_densities` |
