# Q11: (n=14, m=11, alpha<=8) with Henning-Yeo / K48 deletion constraints (CP-SAT)   -- RESULT: UNKNOWN

Question: does a class-O' ordered midpoint hypergraph (linear, injective midpoints, F7-free, K30, K31, cores of n<=8) on 14 vertices with exactly 11 edges and
alpha<=8 exist that also satisfies the implied deletion constraints below? INFEASIBLE would show (modulo soundness) that no non-saturated extremal 14-point set exists.

## Constraints (model14.py) and derivations   [derived-here unless noted]
Let C be a 14-point (4,5)-set, h(C)=8, m=11, tau=6; H its AP hypergraph (linear, F7-free).
- (a) alpha(H)=8: eager clauses (all C(14,9) 9-sets contain an edge) + witnesses of (b).
- (b) for every p: H-p is a 13-point (4,5)-set, so 8=f(13)<=h(C-p)<=h(C)=8 [f(13)=8: START_HERE section 5]. Hence an independent 8-set avoiding p (witness vector,
  sum=8, s_p[p]=0, no edge inside). Henning-Yeo [published] on H-p (tau=5): 85<=65+3(m-deg p), i.e. m-deg p>=7, deg p<=4 (added as a linear constraint).
- (c) for every pair p<q: 7=f(12)<=h(C-p-q)<=8; h=7 would make C-p-q an extremal 12-point subset of the extremal 14-point set C, excluded by K48/L006 (ACCEPTED; its scope is
  every 14-point (4,5)-set with h<=8, saturated or not). So an independent 8-set avoids p,q (witness vector, unconditional, 91 of them). Relies on L006, i.e. on K41 (completeness of the 54,243 classes).
- (d) exactly 3 non-midpoints: automatic from m_exact=11 and injective midpoints (not added separately; the interior non-midpoint w has deg<=4 by (b)).
Base model: e757.cpsat_model.build_model(m_exact=11, monotone, medial, cores from data/forbidden_ordered_n7/n8.json (2M literal budget), reflection lex symmetry breaking), F7 forbidden eagerly (1,441,440 clauses).

## Soundness  [verified-here]
- soundness.py/soundness.json (no solver): A_base and 50 random (seed 7) of the 2,910 census classes satisfy (a)-(c) with T=8 (m=12; (c) holds there by K47). soundness_full.py: all 2,910 classes, 0 violations.
- encoding_test.py/encoding_test.json: edge variables fixed to 21 patterns (A_base + 20 random class-O' patterns with alpha<=8..10, m=9..12) and T in {7,8,9}: CP-SAT feasibility of the constraints equals the direct computation in all 63 comparisons (25 feasible, 38 infeasible).
- (14,12) sanity cell, 600 s, 3 workers, lazy F7 (result_m12test.json, solver_m12test.log): UNKNOWN, but 3 abstract solutions of the constrained model were produced (all order-infeasible, 758 learnt cores), so the constrained model is abstractly satisfiable at m=12; no realizable pattern within 600 s (the unconstrained census already shows 2,910 real ones exist).

## Commands
python3 experiments/20261017-0100-n14m11-deletion-cpsat/{soundness,soundness_full,encoding_test}.py
python3 .../model14.py solve 12 600 3 m12test
bash scripts/start_job.sh experiments/20261017-0100-n14m11-deletion-cpsat 4 nice -n 5 python3 .../model14.py solve 11 10800 2 m11     (F7MODE=eager default)
A first attempt with lazy F7 (54 solve rounds, ~1 min each, 0 abstract solutions in ~55 min, logs *_lazyf7_aborted.log) was killed and replaced by eager F7.

## Result  [heuristic for the statement of non-decision]
m=11: CP-SAT status UNKNOWN at 10,800 s (2 workers, nice 5, shared with the 4-worker DFS at nice 19): 1.36M conflicts, 3.46M branches, 5,440 restarts, 4.58M LP iterations, 1,993,421 constraints after the model build;
no abstract solution, no INFEASIBLE. Q11 is NOT decided by this run (result_m11.json, solver_m11.log, results.json). Nothing was realized, so new_claim.py was not run.

## Conclusion
The deletion constraints (b),(c) (the (c) witnesses are the new strong ones) did not let CP-SAT decide the (14,11) cell in 3 h with 2 workers, as for n=16 (D24). Q11 stays open; the DFS is unaffected.
Suggested: cube-and-conquer on the first midpoint-prefix (the DFS's 3,437 prefixes) with these constraints, giving each cube a short CP-SAT/CaDiCaL budget.
