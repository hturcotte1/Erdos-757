# n=16, alpha<=9: CNF/CDCL (CaDiCaL) variant of the D24 deletion-constraint model

Question: does CaDiCaL decide the class-O' abstract problem (n=16, alpha<=9, m in {13,14}) plus the Henning-Yeo deletion constraints
of experiments/20261016-0850-n16-deletion-cpsat (D24) where CP-SAT (2 workers, 3.5 h) returned UNKNOWN?

## Method (build_cnf.py)
- Base = `e757.sat_indep.Encoding(16, 9, m)` (linear, injective midpoints, K30, K31, alpha<=9 as all 8008 10-subsets, cores v<=7 eager and v=8 lazy,
  F7 lazy, exactly m edges by seqcounter; for m=14 also the Gyarfas-Lehel LR colouring constraints, which are consequences of the definition and only valid for m=n-2)
  + reflection lex-leader (as in cpsat_model).
- Deletion constraints, same semantics as model16.add_deletion_constraints: (b) deg p <= m-9 (HY on 15 vertices), a 9-set independent witness avoiding p for every p (witness (a) implied by (b));
  (c) for each pair p<q a selector b_pq: b_pq -> witness (sum 9, zero at p,q, no edge inside; pysat seqcounter guarded by -b_pq);
  NOT b_pq -> (number of edges meeting {p,q}) == m-11. This count equals deg p + deg q - eps_pq, so the eps variable is not needed (the union of the edge variables is counted once). Same caveat as D24: "==11" relies on census completeness (K45).
- Lazy part: F7/8-vertex cores no-goods, then realizability CEGAR as in model16 (RZ.order_feasible / iis / forced_relations / realize_exact; plain no-goods, not generalised to all embeddings). Any realizable hit would go to scripts/new_claim.py (never triggered).
- Solver: pysat Cadical195, one process per instance, `nice -n 5`, hard `timeout 12600` (cadical not interruptible through pysat; the first solve call never returned, so there are no log lines after "built").

## Verification before the run [verified-here]
- encoding_test.json: with the edge variables fixed, the CNF deletion part and the direct computation `check_conditions` (model16) agree in all 145 comparisons
  (A_base n=14 T=8 ge9; 12 random 16-vertex class-O patterns x T in {9,10} x modes eq11, ge9, ge10, eq11, eq12, none); 65 feasible, 80 infeasible. Command: `python3 build_cnf.py enctest`.
- fullcheck.json (n=14, T=8, m=12, mode ge9, full CNF incl. GL LR, cores, lex): A_base is rejected, its reflection accepted (lex-leader picks one); incremental add_clause after solve works with cadical195.

## Runs (started 12:40:17 UTC)
`bash scripts/start_job.sh experiments/20261016-1240-n16-cnf-witness 4.5 bash -c "run_instance.sh 13 m13 & run_instance.sh 14 m14 & wait"`; each: `python3 build_cnf.py solve 16 9 M TAG cadical195`.
| instance | vars | clauses | result |
|---|---|---|---|
| m=13 | 134,077 | 840,722 | TIMEOUT at 12,600 s (no answer, no abstract solution) |
| m=14 (+GL LR) | 182,785 | 940,476 | TIMEOUT at 12,600 s (no answer, no abstract solution) |
(machine load ~4 from the concurrent (14,11) DFS; both cadical processes at ~94% CPU)

## Conclusion [heuristic]
Neither SAT nor UNSAT within 3.5 h per instance; no 16-point set, nothing judged. CDCL with the witness-vector CNF does not decide n=16 either (consistent with D15, D20, D24). f(16) remains undecided.
Not tried: cube-and-conquer / prefix split (D15) with these constraints, other seeds, kissat, proof logging.
