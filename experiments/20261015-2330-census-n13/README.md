# Exact census of saturated extremal 13-point sets (n=13, m=11, alpha<=8)

Question: how many affine classes of saturated (m = n-2 = 11) 13-point (4,5)-sets with h = f(13) = 8 exist? This fills the
gap in the sequence of saturated extremal classes 1, 4, 66, 1262, 6644, 466961, 54243, ?, 2910 (n = 6..14; K41, K43, K45).

Method: the certified pipeline of L002/L004: exhaustive prefix-split C DFS over class O (linear, F7-free, injective midpoints,
K30) with alpha <= 8 and exactly 11 edges, then postprocess.py (K31/core pre-filters, exact realization, affine classes,
judge spot check). Henning-Yeo allows m >= 7 at (13, tau=5); the non-saturated cases m = 7..10 are NOT enumerated here (for
n <= 11 they always contain realizable patterns, giving infinitely many classes; the saturated count is the meaningful finite number).

Command (launched 2026-10-15 23:33 UTC, 3 workers, resumable):
`python3 -m e757.ordered_dfs_split 13 8 11 3 3 experiments/20261015-2330-census-n13/results --refl --nice 10 --tag n13_m11`
then `python3 experiments/20261014-1005-census-dfs/postprocess.py 13 8 11 experiments/20261015-2330-census-n13/results n13_m11 3`.

Result (2026-10-15 23:50 UTC): STOPPED as infeasible after 8 of 1,811 prefixes (45 CPU-min). Those 8 prefixes alone
contain 54,717,717 class-O patterns (partial_summary.json; the pattern streams, 263 MB, were deleted; the .done summaries
are kept). The constraint alpha <= 8 at n = 13 has Henning-Yeo slack 13 (17*5 = 85 <= 65 + 33 = 98), far looser than the
slack-4 case n = 14 (205,529 patterns in total), so the full pattern count is of the order 10^9 and the exact realization
step (about 1 ms per pattern at best) is out of reach in this run. The saturated class count at n = 13 stays open (Q12) and
needs a different method (e.g. realizability-aware pruning inside the DFS, or counting classes via canonical augmentation
of realizable 12-point classes). [verified-here: partial counts; heuristic: the 10^9 projection]
