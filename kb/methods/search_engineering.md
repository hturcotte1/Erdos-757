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
  (`e757.fn_bounds.beat_feasibility`). For $n=16$ that means at most one non-midpoint; for $n=18,
  20, 22$ every interior point is a midpoint.

## Baseline (in repo)
`e757/ordered_search.py`: DFS over midpoint choices in rank order, pruning by linearity, an LP
order check (scipy HiGHS) and an alpha bound near the leaves. Measured speed (13 Oct 2026, one CPU):
- finds f(n) witnesses for n=8, 10, 11 in under 1 s, and n=12 in about 12 s;
- exhaustively refutes n=13, h=7 only slowly (timed out after 3 min);
- did not find a 14-point h=8 set within 3 min.

## CEGAR with CP-SAT (recommended next engine)
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

Decision procedure for $f(16)=9$: run steps 1–5 to UNSAT with $T=9$, $n=16$ and $m\ge13$. If it
is UNSAT, that is a certificate that no 16-point set reaches 9. Getting a referee to accept it
requires logging every cut and re-checking the cuts independently. Remember the leaf-level
caveats: forced coincidences and (4,5) need their own no-goods.

## Faster alternatives
- Port the DFS to C/C++/Rust, or to numba. Bitset linearity checks plus incremental Gaussian
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
