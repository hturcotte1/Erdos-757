# L019 work folder: Conjecture C1 (triple coverage at a degree-3 vertex)

Question: can Conjecture C1 of experiments/20261027-0300-transversal-richness be proved (it would exclude case (a) of
L017 Theorem 4 for a minimal counterexample to I11)? Result: PARTIAL, see results/proofs/L019-triple-coverage-C1.md
(Theorems 1-6, Lemma 7, Propositions 8, 9; GAP 1 = slack(F)=1, GAP 2 = slack(F)=0).

All scripts: Python 3, exact integers, one process, run under `nice -n 10` and `timeout`; inputs are the stored class
lists experiments/20261027-0300-transversal-richness/inputs/cell_*.txt (format: n m tau followed by the edges).
`bash reproduce.sh` regenerates every `*_output.txt` (about 10 minutes plus about 10-60 minutes for the (26,22,11) C8 run, depending on machine load).

| file | what it checks | output |
|---|---|---|
| hg.py | exact transversal routines (all minimum transversals), class-C tests (wraps L014's pyverify.py), saturated-set search | - |
| check_folding.py | C1: folding lemma (Theorem 5(a)-(c)) on random linear 3-graphs and stored lists | check_folding_output.txt |
| fold_block_stats.py | C2: why folds leave C; P3 criterion of Theorem 5(d) (saturated sets), 0 mismatches | fold_block_stats_output.txt |
| fold_violators.py | C3: folds of F7 and the two (9,8,4) linear violators | fold_violators_output.txt |
| fold_allblocked.py, fold_pergraph.py | C4/C5: degree-2 vertices / graphs with all folds blocked | fold_allblocked_output.txt, fold_pergraph_output.txt |
| fold_reasons_graph.py | C6: fold-by-fold blocking reasons for chosen classes | fold_reasons_graph_output.txt, fold_reasons_10_8_4_output.txt |
| blocked_and_6b.py | C7: classes satisfying Theorem 6(b) at every degree-2 vertex and with all folds blocked | blocked_and_6b_output.txt |
| nbhd_cover.py | C8: cover number of the closed neighbourhood of v for uncoverable data triples (Remark 10.3) | nbhd_cover_output.txt |
| unc_detail.py | exploratory: local structure of the uncoverable linear triples of a cell | (not used in the certificate) |

Conclusions (all [verified-here as computations, not refereed], illustrative only):
- The folding lemma is exact on every instance (23,000+ folds).
- Folds of tight / slack-1 graphs often stay in C (about 1/3 of all folds), but "all folds blocked" occurs
  (cell (14,12,6) classes #4, #8; four classes of (12,10,5)), and together with Theorem 6(b) it occurs in three
  classes of (10,8,4) (slack 2), always blocked by adjacency / common neighbours: GAP 2 needs reductions beyond folding.
