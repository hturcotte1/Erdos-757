# Research plan

**Principle.** Get data first. Then alternate between the upper-bound track (U) and the lower-bound track (L) in blocks of about 3 hours, and record every outcome.

Both tracks study the same objects: **realizable AP hypergraphs that are (nearly) tight for Henning–Yeo**. In terms of the excess $D(A)=17h-9n$ from `kb/00_START_HERE.md` §3:
- U looks for $D/n<5/7$;
- L tries to prove $D\ge\varepsilon n-C$.

## Phase 0: orientation (at most 1 hour)

- Run `bash scripts/preflight.sh` and confirm that it prints `PREFLIGHT OK`.
- Write START_TIME (UTC) into `journal/STATE.md`.
- Read `kb/00_START_HERE.md`, this file and `kb/dead_ends.md`.

## Phase 1: exact small cases (target 6–12 hours; data for both tracks)

**P1.1 Census.** Enumerate the abstract candidates on $n\le10$–$12$ vertices: 3-uniform hypergraphs that are linear and $F_7$-free, satisfy $e(S)\le|S|-2$ for every $S$, and admit an injective midpoint labeling.
- For each one, decide realizability with `e757.core.realize` or `e757.saturated`.
- Use canonical forms to remove isomorphic copies (networkx, pynauty or your own canonical labeling).
- Store the results as `data/census_n{n}.jsonl.gz`.

**P1.2 Decide $f(8)$ and $f(10)$ exactly.** Acceptance: either a judged construction, or an exhaustive certificate (script plus counts) accepted by the `referee`.

**P1.3 Two libraries** that feed both tracks:
- *special pieces*: realizable configurations with high $\tau$;
- *forbidden pieces*: minimal NON-realizable linear $F_7$-free configurations, the analogues of $F_7$.

**P1.4 The abstract constant.** Compute $c_{\rm hyp}(n)=\min\alpha/n$ over the abstract class in P1.1 and compare it with the realizable minimum. A gap already at small $n$ means arithmetic matters.

## Track U: beat 4/7 (find a set with $D(A)/|A|<5/7$)

**U1 Hypergraph-first local search** at the feasible sizes only: $n=16$ ($h=9$), 18 ($h=10$), 20, 22, 23, 25, 27, 29, 30.
- State: a midpoint map, either saturated or missing at most 1–2 midpoints.
- Move: rewire one midpoint's endpoints, keeping linearity and $F_7$-freeness.
- Score: compute $\alpha$ first (cheap), then solve for the values and check (4,5).
- Methods: simulated annealing, tabu search or evolutionary search.
- Seed with $A_{\rm base}$, the two 12-point sets, and their amalgams.

**U2 SAT/ILP with realizability CEGAR.**
1. A SAT/ILP model proposes a labeled hypergraph with the required $\alpha$ (python-sat cardinality constraints, or OR-Tools).
2. Linear algebra (`realize`) either accepts it or returns the forced bad relation.
3. If rejected, add a blocking clause and repeat.

**U3 Program search.** Evolve generator programs that output sets or midpoint maps, scored by exact $h/n$, in the FunSearch / AlphaEvolve style. All scoring must go through exact code.

**U4 Lattice/Freiman constructions** in $\mathbb Z^2$ and $\mathbb Z^3$: AP structures with long-range edges, projected generically. One-dimensional periodic chains are capped at 3/5 (see dead ends), so long-range structure is required.

**U5 Amalgamation.** Combine records by sharing 2 or more vertices or an edge. One-vertex amalgams and disjoint unions cannot lower the ratio. Always re-check (4,5) exactly, with generic parameters.

**U milestone.** Any judged set with ratio $<4/7$ meets goal clause (A). Secondary milestone: decide $f(16)$.

## Track L: beat 9/17 (prove $D(A)\ge\varepsilon|A|-C$)

**L1 Equality structure.** Find linear $F_7$-free hypergraphs with $m\approx n$ that attain or nearly attain $17\tau=5n+3m$. Use search, plus the Henning–Yeo 2021 paper and book if you can get them. Test each one for realizability; if none is realizable, aim for a **stability** theorem.

**L2 Forbidden families.** From P1.3, find a small family of non-realizable configurations that every near-tight hypergraph must contain.

**L3 Discharging on $D=\delta+3\cdot\#\text{non-midpoints}$.**
- Design local charging rules.
- **Before** trying to prove any weighted inequality, test it by LP or exhaustive check on every enumerated realizable configuration, including all induced subconfigurations. The omega issue shows that untested inequalities fail fast.
- Imitate Henning–Yeo's deficiency method (`kb/literature/part2_supplement.md` §3.2).

**L4 Degree split.** When the maximum AP-degree is at most 2, Henning–Yeo (EJC 24(2) P2.50) already gives $h\ge(5n+3)/9$. Concentrate the charging on vertices of degree $\ge3$.

**L5 Hereditary sparsity.** Prove a transversal bound stronger than $17\tau\le5n+3m$ for linear $F_7$-free hypergraphs with $e(S)\le|S|-2$ for every $S$.

**L milestone.** A proof of $c_*\ge r>9/17$ meets goal clause (B). Secondary milestones:
- prove or refute omega's candidate $7\tau(K)\le3|R|+2e_2+4e_1$;
- classify the Henning–Yeo equality cases.

## Allocation and rhythm

- Spend roughly the first 10 hours on Phase 0 and Phase 1.
- Then alternate U and L blocks of about 3 hours each.
- After every block, run the `e757-checkpoint` skill, write a LOG entry, and decide whether to continue or pivot.
- If a block produces a candidate result, stop and run the `verify-claim` skill.
- Run heavy computations in the background with logs, timeouts and checkpoints, and work on the other track meanwhile.
- Prefer Python with exact arithmetic for anything that decides a claim. Use C/Rust/numpy only for search, and re-check the hits exactly.

## Partial results worth recording

These do not meet the goal on their own, but log them in `results/LEDGER.md`:
- exact values of $f(n)$;
- $c_{\rm hyp}(n)$;
- new forbidden configurations;
- refuted or proved auxiliary inequalities;
- the realizable-hypergraph census;
- an OEIS-ready sequence $f(1),f(2),\dots$
