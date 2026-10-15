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

Result: (pending)
