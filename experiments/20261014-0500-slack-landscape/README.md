# HY slack landscape of O' and of the realizable class, n <= 14

Question: for each n and each exact edge count m, what is the maximum tau (= n - min alpha) in the abstract
ordered class O' (linear, F7-free, monotone K30, medial-triangle-free K31, forbidden cores of
data/forbidden_ordered_n7.json + _n8.json) and in the realizable class, and hence the Henning-Yeo slack
s(n,m) = 5n + 3m - 17 tau_max (>= 0 by K8)?  Note D = 17h - 9n = s + 3(n-m).

Method [verified-here for exact cells]: `driver.py`. For each (n,m) start at T = max(HY bound, n-m) (both valid lower
bounds on alpha) and increase T until `feasible_alpha_le(n,T,m_exact=m, monotone, medial, cores)` is SAT
(class O') or `solve_realizable(...)` is SAT (realizable; started at the O' optimum; every SAT carries an
exactly verified integer set). UNSAT = proved by CP-SAT for the stated class; UNKNOWN = time limit
(120-300 s per call) -> cell reported as a range ("lo-hi", from the proved lower bound on alpha and the SAT witness).
Cores: n <= 12 used a 500k-literal budget (sound: witnesses are re-checked against ALL cores in check.py; UNSAT in a
relaxation implies UNSAT in the full class). n = 13, 14 used the FULL core library (budget None), because the
500k budget truncates cores there (two n=13 witnesses violated omitted cores; those truncated results are kept
in results_op_n13_14_truncated_cores.jsonl and are NOT used).

Commands: `BUDGET=0 MOFF=3 python3 driver.py op 13 14 120`, `python3 driver.py op 6 12 600`, `python3 driver.py real 6 11 120`,
`MOFF=4 python3 driver.py real 12 12 120`, `BUDGET=0 MOFF=0 python3 driver.py real 13 14 150`; then `python3 analyze.py; python3 check.py`.
(Orchestration: run_all.sh, run2.sh.) MOFF=k restricts to m >= n-2-k. Seeds: solver default seed 0.

Coverage: O' complete for n=6..11 (all m=1..n-2) and n=12 except (12,9)[range]; n=13: m=8..11 (m<=7 not computed in the
final run); n=14: m=9..12 ((14,11) is a range; m<=8 not computed). Realizable: complete n=6..11 (same m), n=12 m=6..10,
n=13 m=11 only (range), n=14 m=12 only. Cells marked "." were not computed (not "infeasible").
Independent re-verification: `check.py` re-checks every witness (57 O', 46 realizable) by brute-force alpha over all
2^n subsets, linearity, unique midpoints, F7-freeness, its own K30 and K31 tests, `constraint_violations` with all cores,
slack bookkeeping, and for the realizable ones the exact integer set (strictly increasing, AP set == edge list, (4,5)-set).
All passed (output: "op verified 57 witnesses / real verified 46 witnesses").

## Tables: entries are tau_max/slack (bold = minimum slack in the row among exact cells). Ranges "a-b/c-d" are unresolved cells.

### O' (abstract ordered class): tau_max/slack for each (n, m)

| n \ m | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | min slack (m), exact cells | min slack, m>=n-4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1/16 | **2/2** | 2/5 | 2/8 |  |  |  |  |  |  |  |  | 2 (m=2) | 2 (m=2) |
| 7 | 1/21 | **2/7** | 2/10 | 2/13 | 2/16 |  |  |  |  |  |  |  | 7 (m=2) | 10 (m=3) |
| 8 | 1/26 | 2/12 | 2/15 | 2/18 | **3/4** | 3/7 |  |  |  |  |  |  | 4 (m=5) | 4 (m=5) |
| 9 | 1/31 | 2/17 | **3/3** | 3/6 | 3/9 | 3/12 | 3/15 |  |  |  |  |  | 3 (m=3) | 9 (m=5) |
| 10 | 1/36 | 2/22 | 3/8 | 3/11 | 3/14 | 3/17 | **4/3** | 4/6 |  |  |  |  | 3 (m=7) | 3 (m=7) |
| 11 | 1/41 | 2/27 | 3/13 | 3/16 | 3/19 | **4/5** | 4/8 | 4/11 | 4/14 |  |  |  | 5 (m=6) | 8 (m=7) |
| 12 | 1/46 | 2/32 | 3/18 | **4/4** | 4/7 | 4/10 | 4/13 | 4/16 | 4-5/2-19 | 5/5 |  |  | 4 (m=4) | 5 (m=10) |
| 13 | . | . | . | . | . | . | . | **5/4** | 5/7 | 5/10 | 5/13 |  | 4 (m=8) | 7 (m=9) |
| 14 | . | . | . | . | . | . | . | . | 5/12 | 5/15 | 5-6/1-18 | **6/4** | 4 (m=12) | 4 (m=12) |

### Realizable class: tau_max/slack for each (n, m)

| n \ m | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | min slack (m), exact cells | min slack, m>=n-4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1/16 | **2/2** | 2/5 | 2/8 |  |  |  |  |  |  |  |  | 2 (m=2) | 2 (m=2) |
| 7 | 1/21 | **2/7** | 2/10 | 2/13 | 2/16 |  |  |  |  |  |  |  | 7 (m=2) | 10 (m=3) |
| 8 | 1/26 | 2/12 | 2/15 | 2/18 | **3/4** | 3/7 |  |  |  |  |  |  | 4 (m=5) | 4 (m=5) |
| 9 | 1/31 | 2/17 | **3/3** | 3/6 | 3/9 | 3/12 | 3/15 |  |  |  |  |  | 3 (m=3) | 9 (m=5) |
| 10 | 1/36 | 2/22 | 3/8 | 3/11 | 3/14 | 3/17 | **4/3** | 4/6 |  |  |  |  | 3 (m=7) | 3 (m=7) |
| 11 | 1/41 | 2/27 | 3/13 | 3/16 | 3/19 | **4/5** | 4/8 | 4/11 | 4/14 |  |  |  | 5 (m=6) | 8 (m=7) |
| 12 | . | . | . | . | . | 4/10 | 4/13 | 4/16 | 4-5/2-19 | **5/5** |  |  | 5 (m=10) | 5 (m=10) |
| 13 | . | . | . | . | . | . | . | . | . | . | 4-5/13-30 |  | - | - |
| 14 | . | . | . | . | . | . | . | . | . | . | . | **6/4** | 4 (m=12) | 4 (m=12) |

### Gaps: (n,m) with strictly smaller tau_max in the realizable class

| n | m | tau_max O' | tau_max real | slack O' | slack real |
|---|---|---|---|---|---|
(none)
## Minimum-slack witnesses (slack <= 5; one solver-chosen witness per cell, so structure is not claimed unique)

Raw data: structures.json (degree sequence, non-midpoints = n-m, per-vertex role string over incident edges in {L,M,R}, component sizes,
`realizable` = `realize_exact` on that very pattern). Selected rows (cls, n, m, tau, slack | nonmidpoints | degrees | components | realizable):

| cls | n,m | tau | s | n-m | degree seq | components | realizable (this pattern) |
|---|---|---|---|---|---|---|---|
| O',real | 6,2 | 2 | 2 | 4 | 1^6 | 3+3 | yes |
| O',real | 9,3 ; 12,4 | 3 ; 4 | 3 ; 4 | 6 ; 8 | 1^n | disjoint edges | yes |
| real | 10,7 | 4 | 3 | 3 | 3^2 2^7 1 | connected | yes |
| O' | 10,7 | 4 | 3 | 3 | 3,2^9 | connected | NO (another O' witness is realizable) |
| O',real | 8,5 | 3 | 4 | 3 | 3,2^5,1^2 | connected | yes |
| O',real | 13,8 | 5 | 4 | 5 | 3,2^9,1^3 | 10+3 | yes |
| O',real | 6,3 ; 11,6 | 2 ; 4 | 5 | 3 ; 5 | mostly 2 and 1 | 6 ; 8+3 | yes |
| O' | 12,10 | 5 | 5 | 2 | 3^6 2^6 | connected | NO |
| real | 12,10 | 5 | 5 | 2 | 3^6 2^6 | connected | yes (verified set) |
| O' | 14,12 | 6 | 4 | 2 | 3^8 2^6 | connected | NO |
| real | 14,12 | 6 | 4 | 2 | 4,3^6,2^7 | connected | yes (a degree-4 vertex, 2 non-midpoints) |

Recurring features: (i) slack <= 3 is attained only by (a) unions of disjoint edges (n = 3m, s = m: trivial, the HY bound is
not tight there) and (b) the single connected case n=10, m=7 (tau=4, 3 non-midpoints); (ii) in every saturated minimum
(12,10), (14,12) all roles occur LM / MR / LMR with the two extreme points of degree 3-4 purely L resp. R (LLL..., ...RRR), no vertex of
role pattern M alone, one component, no isolated vertex; (iii) the O' witnesses chosen by the solver are often NOT
realizable (10,7; 12,10; 14,12) although a realizable witness with the same (n,m,tau) exists, i.e. non-realizable patterns
of minimum slack exist but are not needed for the value.

## Conclusion
[verified-here for exact cells, [heuristic] where a time limit left a range]. In O' the minimum slack over exact cells is
2,7,4,3,3,5,4,4,4 for n = 6..14, but the small values come from disjoint-edge unions (non-midpoints 4-8), not from
HY-tight structures. Restricted to the saturated cell m = n-2 (the case relevant for beating 9/17, D = s + 6), the slack is
8-ish and oscillates with parity: n=6..14: 8,16,7,15,6,14,5,13,4, i.e. for even n tau_max = n/2 - 1 and s = 11 - n/2
(7,6,5,4 for n=8,10,12,14), for odd n tau_max = (n-3)/2 and s = (39-n)/2. So the saturated slack in O' DECREASES by 1 per 2 vertices
over the computed range (and the n=14 value 4 is attained by A_base, so the realizable class reaches it); [heuristic] if this
linear trend continued, slack 3 at n=16 would need alpha=9, which is exactly the open f(16) question, and HY-tightness would
occur around n=22; no evidence beyond n=14 here. The realizable class coincides with O' in every resolved cell
(no gaps for n <= 11, n=12 m=6,7,8,10, n=14 m=12), so the cores plus K30/K31 already capture the arithmetic of the extremal
values at these sizes. Unresolved cells (time limit): (12,9) tau_max in {4,5} for both classes (s = 2 if 5, which would be the
smallest connected slack seen), (13,11) tau_max real in {4,5} vs O' = 5, (14,11) O' tau_max in {5,6}. A longer run of
hard_12_9.py (480 s, alpha <= 7, m = 9, O') is in hard_12_9.log (see below).

Result of hard_12_9.py: UNKNOWN after 480 s (O', alpha<=7, m=9, full cores): the cell (12,9) stays a range, tau_max in {4,5} [heuristic].
