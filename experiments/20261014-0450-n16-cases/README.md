# n=16, T=9: resumable case split (monotone K30 + medial K31 + forbidden cores, F7-free)

Question: is there an ordered midpoint hypergraph on 16 vertices with alpha <= 9 (hence m in {13,14} by
Henning-Yeo) satisfying the exact realizability consequences?  UNSAT everywhere => no such abstract
hypergraph => f(16) = 10 modulo Henning-Yeo (to be certified later by the independent DFS).

## Method
30 sub-instances: m_exact in {13,14} x vertex 1 either not a midpoint (k=0) or the midpoint of (0,1,k),
k=2..15.  Each is one `enumerate_solutions` call (e757/cpsat_model.py: eager alpha<=9 clauses, lazy F7,
K30, K31, cores added by size up to a 2.5M-literal budget, blocking clauses sound because m is fixed),
workers=1, 3000 s limit, 4 sub-instances in parallel.  The reflection lex constraint is dropped inside
cases (the case split on vertex 1 is not reflection-invariant; dropping a symmetry-breaking constraint is
trivially sound, it only costs a factor <= 2).  A TIMEOUT case is automatically split by the edge of vertex 2
((0,2,k), (1,2,k), or none).  If SAT all solutions are enumerated, each goes through
e757.realizability.realize_exact, and realizable sets through scripts/new_claim.py immediately.
Each finished sub-instance writes results/case_m{M}_k{K}[_v2_..].json atomically; the driver skips
existing JSONs, so a restart resumes (an interrupted sub-instance restarts from scratch).

## Command (one line, resumable; also runs the feasible-size sweep afterwards)
    bash scripts/start_job.sh experiments/20261014-0450-n16-cases 14 bash experiments/20261014-0450-n16-cases/run_all.sh
Progress: `python3 experiments/20261014-0450-n16-cases/aggregate.py` (rewrites the block below), log run.log.
Sweep results: experiments/20261014-0030-feasible-sizes/results/n{N}_T{T}_m{M}.json.

<!-- RESULTS START -->
(no case finished yet)
<!-- RESULTS END -->
