# c_hyp(n): abstract ordered-midpoint-hypergraph engine and table

Question: for ordered midpoint hypergraphs on 0..n-1 (midpoint injective, linear, optionally F7-free)
what is c_hyp(n) = min independence number alpha?  (c_hyp(n) <= f(n); realizability is NOT imposed.)
Is c_hyp(16) = 9 or 10; is c_hyp(13) = 8 or 7?

## Method [verified-here for everything marked so]
Engine: `e757/cpsat_model.py` (OR-tools CP-SAT).  Boolean e[i,j,k]; (a) at-most-one edge per midpoint,
(b) at-most-one edge per vertex pair, reflection lex-leader, lazy F7 no-goods (find all F7 copies in
each solution, forbid them).  alpha <= T is encoded EAGERLY: every (T+1)-subset of vertices contains an
edge (C(n,T+1) clauses).  This was ~15x faster than the lazy alpha-cut CEGAR loop that the spec suggested
(n=14, T=8: 5 s vs 81-89 s; n=16, T=9 lazy did not converge in 10 min).  The lazy alpha-cut CEGAR
loop is still in the module (`eager=False` in `solve_min_alpha` / `feasible_alpha_le`).
T is decreased from n; each SAT answer gives T = alpha - 1.
`use_hy=True` additionally imposes m >= ceil((17(n-T)-5n)/3) (consequence of the PUBLISHED Henning-Yeo
inequality, valid only for F7-free): rows labelled "HY-assisted" depend on that theorem; "solver-only" rows do not.
Tests (`tests/test_cpsat_model.py`): solver min alpha equals exhaustive DFS for n=5..9 (F7 on/off),
enumeration of all (n=7,T=5,m=5) hypergraphs equals brute-force enumeration (with/without reflection),
the 12- and 14-point record sets give valid hypergraphs with alpha 7 and 8.

## Commands
    PYTHONPATH=. python3 experiments/20261013-2257-chyp-table/table.py 5 12 1 1200 40   # solver-only, n=5..12
    PYTHONPATH=. python3 experiments/20261013-2257-chyp-table/table.py 13 14 2 1500 40   # solver-only n=13,14 (see status below)
    PYTHONPATH=. python3 experiments/20261013-2257-chyp-table/run_n.py N 1 3000 4 1       # HY-assisted (n=13,14,15 done with the older lazy-cut code)
    PYTHONPATH=. python3 experiments/20261013-2257-chyp-table/run_feas.py 16 9 1 1 6000 4 # n=16, T=9, F7-free, HY-assisted
    PYTHONPATH=. python3 experiments/20261013-2257-chyp-table/aggregate.py ; python3 experiments/20261013-2257-chyp-table/check.py
Seeds: CP-SAT random_seed=0, sampling rng seed 0.  Machine was shared (load ~10 on 4 cores), so wall-clock
numbers are inflated by roughly 2-3x.

## Results (see table.md, witnesses.json, results/)
SOLVER-ONLY (no Henning-Yeo), n=5..12, wall-clock per n (both F7 modes) in table.md.
c_hyp with F7-freeness: 4,4,5,5,6,6,7,7 for n=5..12; without F7-freeness: 4,4,4,5,6,6,7,7.
F7-freeness matters only at n=7 so far (F7 itself has alpha 4; F7-free min is 5 = f(7)).
For n=5..12, c_hyp(n) = n - floor((8n-6)/17) = HY bound = f(n): the abstract relaxation loses nothing there.
"min m" column = fewest edges in a hypergraph with alpha <= c_hyp (found by tightening m_max; "<=" means
the top-down tightening hit its 40 s limit unproven).  It is small because alpha >= n - m (not informative
for the HY question; HY's m_need is the informative number, see below).

HY-ASSISTED (F7-free): c_hyp(13)=8, c_hyp(14)=8, c_hyp(15)=9 (witnesses re-verified).  The UNSAT
steps (13: T=7, 14: T=7, 15: T=8) are immediate consequences of Henning-Yeo (m_need > n-2), i.e. not
independent solver proofs.  Since f(13)=8, f(14)=8, f(15)=9 are known, c_hyp(n)=f(n) there: c_hyp(13)=8 not 7.

SOLVER-ONLY n=13 (no HY input): F7-free upper bound 8 found; the T=7 infeasibility was NOT proved in 1500 s
(shared machine) -- so the solver alone cannot yet certify c_hyp(13)=8; HY does it instantly.  n=13 no-F7 and n=14
solver-only were not completed.

n=16, T=9 (F7-free, m >= 13 forced by HY): STATUS at hand-back: the run
`run_feas.py 16 9 1 1 6000 4` was still running (log run.log; result file
results/feas_n16_T9_f71_hy1_mNone.json appears when it finishes: result SAT => c_hyp(16)=9 and the witness
is a candidate abstract hypergraph for a 9/16 set (must then be realized with
e757.saturated.solve_midpoint_map / ordered LP); UNSAT => c_hyp(16)=10 (modulo HY) and f(16)=10).
No conclusion on c_hyp(16) is claimed here.

## Conclusion
Engine works and agrees with brute force for n<=9 and with the known f(n) up to n=15.  Eager alpha
encoding is the right design.  c_hyp(16) is undecided at hand-back.

## Table (solver-only n=5..12; time columns are wall-clock s on a loaded machine)
| n | c_hyp (F7-free) | c_hyp (no F7) | min m (F7-free) | min m (no F7) | HY lower | f(n) known | time F7 / noF7 (s) |
|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | <=1 | <=1 | 4 | 4 | 0.0 / 0.0 |
| 6 | 4 | 4 | 2 | 2 | 4 | 4 | 0.0 / 0.0 |
| 7 | 5 | 4 | 2 | 5 | 5 | 5 | 0.3 / 0.0 |
| 8 | 5 | 5 | 5 | 5 | 5 | 5 | 0.0 / 0.0 |
| 9 | 6 | 6 | 3 | 3 | 6 | 6 | 0.8 / 0.8 |
| 10 | 6 | 6 | <=7 | 6 | 6 | 6 | 0.4 / 0.5 |
| 11 | 7 | 7 | <=6 | <=6 | 7 | 7 | 10.6 / 10.1 |
| 12 | 7 | 7 | <=10 | <=10 | 7 | 7 | 6.3 / 6.4 |

Jobs still running at hand-back: n=16 T=9 (pid in experiments/20261013-2257-chyp-table/job.pid; result file results/feas_n16_T9_f71_hy1_mNone.json) and the m_exact=14 sub-case (results/feas_n16_T9_f71_hy1_m14.json). To finish: run aggregate.py and check.py after they complete.


Follow-up (2026-10-14): the unconstrained n=16 jobs above were killed. The constrained n=16 decision (monotone K30, medial K31, forbidden cores) is in experiments/20261014-0030-n16-decision/; the sweep of other record-feasible sizes is in experiments/20261014-0030-feasible-sizes/.
