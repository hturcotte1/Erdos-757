# Research plan

**Principle.** Get data first. Then alternate between the upper-bound track (U) and the lower-bound track (L) in blocks of about 3 hours, and record every outcome.

Both tracks study the same objects: **realizable AP hypergraphs that are (nearly) tight for Henning–Yeo**. In terms of the excess $D(A)=17h-9n$ from `kb/00_START_HERE.md` §3:
- U looks for $D/n<5/7$;
- L tries to prove $D\ge\varepsilon n-C$.

## Phase 0: orientation (at most 1 hour)

- Run `bash scripts/preflight.sh` and confirm that it prints `PREFLIGHT OK`.
- Run `bash scripts/fetch_papers.sh`. For anything that fails, send the `scout` (in the background of later work) to fetch and digest it, starting with Gyárfás–Lehel 1995 into kb/notes/gyarfas_lehel_1995.md.
- Dispatch a `worker` to build the CP-SAT/CEGAR engine from kb/methods/search_engineering.md, and validate it on n=12 and 14 (it must rediscover h=7 and h=8).
- Write START_TIME (UTC) into `journal/STATE.md`.
- Read `kb/00_START_HERE.md`, this file and `kb/dead_ends.md`.

## Phase 1: exact small cases (target 6–12 hours; data for both tracks)

**P1.1 Census.** [Status 2026-10-16: DONE in a restricted form, and extended beyond the original $n\le10$–$12$ target. What was enumerated is not every abstract candidate but the class-O patterns (linear, injective midpoints, K30-monotone, $F_7$-free) with $\alpha\le f(n)$, each realized exactly. Results, as affine classes of extremal sets [verified-here]: saturated classes for $n=6..11$ are 1, 4, 66, 1262, 6644, 466961 (K43/L003; `experiments/20261014-1430-small-counts/results/`); $n=12$ has 54,243 classes, which is every extremal 12-point set (K41/L002; `experiments/20261014-1005-census-dfs/results/realized_n12.json.gz`); $n=14$ has 2,910 saturated classes (K45/L004; `data/census_n14_m12_classes.jsonl.gz`). The output name `data/census_n{n}.jsonl.gz` stated below was not used; see `data/README.md` for the actual files. $n=13$ was not completed: the pattern-first pipeline is infeasible there (D22, Q12) [verified-here for the partial counts]. The non-saturated $(14,11)$ case is closed (Q11; certificate L007, K51, 2026-10-17): no 14-point (4,5)-set with $h=8$ has $m=11$, so 2,910 is the total number of extremal 14-point classes (modulo the L004 completeness caveat); the exhaustive DFS was stopped after 1,081 of 3,437 depth-3 prefixes were logged done with 0 patterns and is superseded [verified-here].] Enumerate the abstract candidates on $n\le10$–$12$ vertices: 3-uniform hypergraphs that are linear and $F_7$-free, satisfy $e(S)\le|S|-2$ for every $S$, and admit an injective midpoint labeling.
- For each one, decide realizability with `e757.core.realize` or `e757.saturated`.
- Use canonical forms to remove isomorphic copies (networkx, pynauty or your own canonical labeling).
- Store the results as `data/census_n{n}.jsonl.gz`.

**P1.2 (done before launch):** $f(8)=5$, $f(10)=6$ via `e757/ordered_search.py`. Next exact target: **$f(16)$**, which needs a faster search (see Track U). [Status 2026-10-17: DONE: $f(16)=10$ (certificate L008, K52; computer-assisted, referee ACCEPT x3) [verified-here]. The direct CP-SAT, SAT and CaDiCaL decisions (CP-SAT and CaDiCaL also with the Henning–Yeo deletion constraints, 3.5 h per case at $m=13$ and $m=14$) ended UNKNOWN or TIMEOUT and annealing found no set with $h\le9$ (Q1, D15, D16, D24; `experiments/20261016-0850-n16-deletion-cpsat/results.json`, `experiments/20261016-1240-n16-cnf-witness/results.json`) [verified-here for the recorded run statuses], so the decision did not come from a solver: it came from the computer-assisted window-cell induction proving I11 ($11\tau\le3n+2m$) on the abstract class of linear $F_7$-free 3-graphs with $e(S)\le|S|-2$ (kb/notes/i11_conjecture.md; I11 itself remains [conjecture] for general (4,5)-sets). The same induction gave $f(18)=11$, $f(20)=12$, $f(22)=13$ (L009–L011, K53–K55; referee ACCEPT x3 each) [verified-here]; hence no (4,5)-set with at most 22 points beats $4/7$. Closed in Q1.]

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

**U4 Lattice/Freiman constructions** in $\mathbb Z^2$ and $\mathbb Z^3$: AP structures with long-range edges, projected generically. One-dimensional periodic chains have independence density $\ge3/5$ in every case tested (D5: single-class $a+b\le11$, 2-class span $\le8$, 3-class span $\le6$; not a theorem), so long-range structure is the working hypothesis. [Status 2026-10-16: U4 untested, never started; see kb/ideas_backlog.md idea 2.]

**U5 Amalgamation.** Combine records by sharing 2 or more vertices or an edge. One-vertex amalgams and disjoint unions cannot lower the ratio. Always re-check (4,5) exactly, with generic parameters.

**U milestone.** Any judged set with ratio $<4/7$ meets goal clause (A). Secondary milestone: decide $f(16)$. [Status 2026-10-16: clause (A) is not met: no set with ratio $<4/7$ has been found or judged (`bash scripts/status.sh`, re-run 2026-10-17: claims_total 2 (pass 2, fail 0; C001 and C002, the judged 15-point examples of K50 with ratio 3/5, both NO-IMPROVEMENT), new_record_claims none, upper_bound_success NO) [verified-here]. As of 2026-10-17, $f(16)=10$ is decided (Q1 closed, L008, K52), and so are $f(18)=11$, $f(20)=12$ and $f(22)=13$ (L009–L011, K53–K55): no (4,5)-set with at most 22 points beats $4/7$ [verified-here]. Hence sizes $n=16,18,20,22$ need no further U1/U2 searching (a planning consequence of these certificates, not a separate claim). U1 (annealing, D16) never reached $\alpha\le9$ at $n=16$. U2 (SAT/CP-SAT/CEGAR witness searches, D15, D18, D24) returned neither a witness nor a refutation in any instance run (TIMEOUT or UNKNOWN), so these runs are inconclusive, not nonexistence results [heuristic]. U3 was not run: no LLM-written generator programs were run (kb/ideas_backlog.md idea 10; the annealing in D16 is U1, not U3). U4 was never started (see U4 above and kb/ideas_backlog.md idea 2).]

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
