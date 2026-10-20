# Search engineering for Track U (and exact f(n))

## The search space [derived-here]
- Rank the points $x_0<\dots<x_{n-1}$ and work with the gaps $g_t=x_{t+1}-x_t>0$. An AP with
  ranks $i<j<k$ is the linear equation $\sum_{t=i}^{j-1}g_t=\sum_{t=j}^{k-1}g_t$. So a labeled
  AP pattern is realizable in order iff a homogeneous linear system has a strictly positive
  solution (a cone condition). By Gordan/Stiemke duality, infeasibility has a certificate $y$.
  Infeasibility certificates are reusable no-goods.
- Midpoint injectivity and linearity are combinatorial and cheap to enforce. $F_7$-freeness is
  implied by realizability.
- Extra conditions at a leaf:
  - no unintended coincidences (distinct points; no extra APs, unless you accept them and
    recompute);
  - the (4,5) property.

  Both are disequalities, so a generic point of the solution cone satisfies them unless they are
  forced. Check exactly with Fractions.
- Henning–Yeo pruning: to beat 4/7 at size $n$ you need $m\ge m_{\rm need}$
  (`e757.fn_bounds.beat_feasibility`). For $n=16$ that means at most one interior point that is not a midpoint ($m\ge13$; the two extreme points never are midpoints); for $n=18,
  20, 22$ every interior point is a midpoint. [verified-here] These four sizes are now closed: $f(16)=10$, $f(18)=11$, $f(20)=12$, $f(22)=13$ (L008-L011, K52-K55, each referee ACCEPT x3), and with Henning-Yeo (K8) for the other sizes no (4,5)-set with at most 22 points beats $4/7$. The first record cells not excluded by I11 are $(23,21,10)$, $(25,23,11)$, ... (kb/notes/i11_conjecture.md, L011 Remark 5); at $n=23$ the degree-4 case is excluded (L012, K56) and the degree-3 case is open (Q14). I11 is proved on the abstract class only for $n\le22$ (computed, not yet certified, for $n=23$-$26$; [conjecture] beyond), so for $n\ge24$ this list is conditional on I11.

## Baseline (in repo)
`e757/ordered_search.py`: DFS over midpoint choices in rank order, pruning by linearity, an LP
order check (scipy HiGHS) and an alpha bound near the leaves. Measured speed (13 Oct 2026, one CPU; these timings are not recorded in any log or experiment README on disk [heuristic]):
- finds f(n) witnesses for n=8, 10, 11 in under 1 s, and n=12 in about 12 s;
- exhaustively refutes n=13, h=7 only slowly (timed out after 3 min);
- did not find a 14-point h=8 set within 3 min.

## CEGAR with CP-SAT (built: e757/cpsat_model.py, e757/realizability.py; no decision reached)

**Status [verified-here for the facts; heuristic for the interpretation].** This engine is implemented and was run, with K30/K31 and the forbidden cores. It has not decided any open case. Variants of the procedure below (eager alpha clauses, lazy F7 cuts; also a separate pysat encoding) never reached SAT or UNSAT for the $n=16$, $\alpha\le9$ decision: every sub-case timed out (D15), and so did the later runs with the census invariants (D20; $m=14$, 3600 s: CP-SAT UNKNOWN, glucose4 TIMEOUT) and with the Henning–Yeo deletion constraints of Lemmas Δ/Δ′ (CP-SAT, 3.5 h each for $m=13$ and $m=14$: UNKNOWN; CaDiCaL on a CNF with a reflection lex-leader and, for $m=14$, the Gyárfás–Lehel colouring: TIMEOUT after 3.5 h; D24). The witness-mode searches at $n=18,20,22,23,25$ all returned UNKNOWN. In those nine runs the realizability half of the loop (step 5) was never exercised, because the solver returned no candidate hypergraph within the time limit (D18). The $(14,11,\alpha\le8)$ case was UNKNOWN after 7000 s and was replaced by the prefix-split DFS, which was stopped at 1,081 of 3,437 prefixes (0 patterns) once certificate L007 decided the case by a computer-assisted slack argument (K51; D21, Q11 closed). UNKNOWN is not a refutation. Do not repeat these runs without a stronger engine: reflection symmetry breaking, the Gyárfás–Lehel colouring constraints (valid only for $m=n-2$, so used at $n=16$ only for $m=14$) and the census invariants have all been tried at $n=16$ (K37, D20, D24) without a decision. What remains untried is cube-and-conquer on the first midpoint edges with the D24 constraints (the earlier case split of D15 did not use them), or a compiled search far stronger than the existing C class-O DFS (`e757/c/ordered_dfs.c`), whose direct $n=16$ enumeration is estimated at $6\times10^{13}$ to $1.2\times10^{14}$ calls (see "Faster alternatives"). The decision procedure for $f(16)=9$ at the end of this section was never completed (it was never run to UNSAT). Q1 was closed by a different route, the I11 window-cell induction (certificate L008, $f(16)=10$, K52; kb/notes/i11_conjecture.md; likewise L009 to L011, K53 to K55), so the procedure is moot for $n\le22$. At the open record sizes ($n\ge23$; Q2, Q14) the same loop was only run in witness mode and every run returned UNKNOWN (D18), so a decision there remains a plan (kb/ideas_backlog.md idea 4).
Variables: $e_{ijk}\in\{0,1\}$ for $i<j<k$, meaning $j$ is the midpoint of $\{i,j,k\}$.
1. **Midpoints:** $\sum_{i,k}e_{ijk}\le1$ for each $j$ (and $=1$ for the saturated sizes);
   $\sum e\ge m_{\rm need}$.
2. **Linearity:** for each pair $\{a,b\}$, the sum of $e$ over triples containing both is $\le1$.
3. **Symmetry:** reflection $j\mapsto n-1-j$; add a lexicographic constraint on the reversed
   pattern.
4. **Lazy alpha cuts:** solve. Compute $\alpha$ of the solution exactly. If $\alpha>T$, take a
   maximum independent set $I$ and add $\sum_{e\subseteq I}e\ge1$ (some AP must lie inside $I$).
   Repeat. Store all cuts; they are reusable across runs of the same $n$.
5. **Lazy realizability cuts:** solve the gap LP. If it is infeasible, extract an irreducible
   infeasible subset of edges (deletion filter, or the dual certificate) and add the no-good
   "not all of these". These minimal infeasible patterns are also the forbidden-configuration
   library for Track L (RESEARCH_PLAN P1.3).
6. **Leaf:** take an exact generic point, check (4,5) and compute $h$ exactly, then
   `scripts/new_claim.py`.

Decision procedure for $f(16)=9$ (superseded: $f(16)=10$ was proved by certificate L008 via I11, not by this procedure): run steps 1–5 to UNSAT with $T=9$, $n=16$ and $m\ge13$. If it
is UNSAT, that is a certificate that no 16-point set reaches 9. Getting a referee to accept it
requires logging every cut and re-checking the cuts independently. Remember the leaf-level
caveats: forced coincidences and (4,5) need their own no-goods.

## Faster alternatives
- [verified-here] DONE 2026-10-14 for the combinatorial class-O DFS (`e757/ordered_dfs.py`, which
  has no LP step): C port `e757/c/ordered_dfs.c` (wrapper `e757/ordered_dfs_c.py`, bitmask edge
  tests), about 50x faster than the Python version at $n=10$ with identical node counts for
  $n\le10$, plus the resumable prefix-split driver `e757/ordered_dfs_split.py`. It produced the
  censuses K41, K43 and K45 (K45: 113,454,008,923 nodes, 277,501 CPU-s at $(14,12,\alpha\le8)$).
  [heuristic] A direct $n=16$ enumeration is estimated at $6\times10^{13}$ to $1.2\times10^{14}$
  DFS calls (two estimator runs a factor 2 apart), so it was not attempted; see
  `experiments/20261014-0005-ordered-dfs`. The LP-based `e757/ordered_search.py` was not ported,
  and realizability is checked after the DFS (exact realization), not inside it. Still open:
  prune inside the DFS with incremental Gaussian
  elimination over rationals (or mod a large prime, then verify) can replace the LP for saturated
  patterns, since the solution is unique.
- **Saturated patterns are random-walk harmonic functions.** With $x_0=0$ and $x_{n-1}=1$ the
  values are hitting probabilities. Computing them mod $p$ gives a fast order-free pre-filter for
  coincidences; order needs the real values.
- **Local search** (annealing or tabu) over saturated patterns at $n=16$–$30$: rewire one
  midpoint's endpoints; score = (realizable?, alpha, HY slack). Seed from known records.
- **Program search** (FunSearch/AlphaEvolve style): evolve generators of patterns; score by exact
  $h/n$.

## Pitfalls
- Floats decide nothing. Every hit goes through `scripts/new_claim.py`, which runs the frozen
  judge.
- Gluing needs a generic scale. Scales like 7 or 1000 often create parallelograms.
- Long runs go through `scripts/start_job.sh`, with checkpointing of partial results (resumable
  state files).
