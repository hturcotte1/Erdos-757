# n=16 abstract decision with Henning-Yeo deletion constraints (CP-SAT)

Question: is there a class-O' ordered midpoint hypergraph on 16 vertices with alpha <= 9 and m in {13,14}
that also satisfies the implied deletion constraints (a)-(c) of the spec? (UNSAT would give f(16)=10, provided the base model is sound.)

## Method (model16.py; reuses e757.cpsat_model Model/build_model/add_eager_alpha/_cegar_step/_learn_core and e757.realizability)
Base: linear, injective midpoints, F7 (lazy), K30, K31, cores from data/forbidden_ordered_n7/n8.json (budget 1M literals),
reflection lex symmetry breaking, eager alpha<=9 clauses (all C(16,10) 10-sets contain an edge).
Added (derived-here, from HY on vertex-deleted subhypergraphs + f(15)=9 + L005/K46):
- (a) implied by (b).
- (b) for each p: witness vector s_p (16 booleans, sum 9, s_p[p]=0, no edge inside); also m - deg p >= 9 (HY at (15, tau=6)).
- (c) for each pair p<q: boolean b_pq; b_pq => witness s_pq (sum 9, zero at p,q, independent); NOT b_pq => m - deg p - deg q + eps_pq == 11
  (HY at (14,tau=6) gives >= 11; K46/L005 excludes 12; eps_pq = 1 iff p,q lie on a common edge).
  Caveat: the "== 11" step relies on the completeness of the 2,910-class census (K45) for m=12.
- CEGAR over realizability as in solve_realizable (order_feasible / forced_relations / realize_exact; learnt cores generalised to all embeddings);
  a realizable hit would be written to RECORD_CANDIDATE.json and passed to scripts/new_claim.py (never triggered).

## Soundness checks [verified-here]
1. soundness.py (no solver): A_base and a random sample of 60 of the 2,910 census classes (data/census_n14_m12_classes.jsonl.gz, seed 1) all satisfy the
   n=14 conditions (b), (c) with T=8 (HY bound m-deg p >= 7; pair: witness OR m' >= 9). In all of them every one of the 91 pairs has an
   independent 8-set avoiding it (consistent with K47: no extremal 12-point subset), so the "m'" branch was not exercised on real data. -> soundness_n14.json
2. encoding_test.py: with edge variables fixed to a pattern, CP-SAT feasibility of the constraints equals the direct computation (check_conditions)
   in all 145 comparisons (A_base at n=14; 12 random 16-vertex class-O patterns with alpha<=10/11, T in {9,10}, pair modes eq11, ge9, ge10, eq11/eq12, none);
   both outcomes occurred (65 feasible, 80 infeasible), including the b_pq/m' branch. -> encoding_test.json
3. n=14 model (T=8, m=12, mode ge9, 3 workers, 600 s): STATUS UNKNOWN (time limit), but 4 abstract solutions of the constrained model were produced
   (each order-infeasible, 20,020 learnt no-goods), so the model is satisfiable in the abstract sense; A_base itself is accepted by the fixed-edge test above.
   The spec asked for a SAT answer within 10 minutes: only abstract-SAT was reached, no realizable 14-point set within 600 s. (solver_n14test.log, result_n14test.json)

## Runs (n=16, T=9, 2 workers each in parallel, 12,600 s each, CP-SAT; started 09:03 UTC)  [verified-here for the recorded statuses and times; the solver_*.log files, the only source of the LP-iteration and restart counts below, are git-ignored]
commands: bash scripts/start_job.sh experiments/20261016-0850-n16-deletion-cpsat 4.5 python3 .../model16.py solve 16 9 {14 14|13 13} 12600 2 {m14|m13} eq11
- m=14: UNKNOWN (CP-SAT status UNKNOWN at time limit, 9.2M LP iterations, 7.7k restarts); no abstract solution found.
- m=13: UNKNOWN (1.53M conflicts, 7.5M LP iterations); no abstract solution found.
No set was found, so nothing was judged; no INFEASIBLE proof either. (result_m13.json, result_m14.json, solver_m1*.log, results.json)

## Conclusion [heuristic]
The deletion constraints do not make CP-SAT decide n=16 in 3.5 h with 2 workers per case: both cases UNKNOWN, no solution, no refutation.
f(16) remains undecided. Pure feasibility with no objective gives little bound progress; presolve fixed only 1-11 of 3243 variables.
Suggested: a prefix split (as D15) combined with these constraints, or a SAT solver (cadical) with the witness vectors as a cardinality-encoded CNF. The CNF/CaDiCaL variant was run afterwards (experiments/20261016-1240-n16-cnf-witness; kb/dead_ends.md D24): TIMEOUT at 12,600 s for both m = 13 and m = 14, no answer. A prefix split / cube-and-conquer combined with these constraints is still untried.
