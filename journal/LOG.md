# LOG (append-only)

Format for each work block:

    ## <UTC timestamp> <track: P0|P1|U|L|infra> <short title>
    - tried: ...
    - result: ... (tag: [verified-here], [heuristic], ...)
    - evidence: <paths to experiments/, data/, commits>
    - decision: continue / pivot / dead end (and why)

## 2026-10-13T00:00Z infra repository prepared
- tried: built the knowledge base, toolkit, frozen judge, status script, hooks, subagents and tests.
- result: all known facts reproduced by tests/test_known_facts.py [verified-here].
- evidence: tests/, kb/known_results.md
- decision: hand over to the autonomous run.

## 2026-10-13T22:30Z infra pre-launch additions
- tried: ordered midpoint-map search (e757/ordered_search.py); sources and paper digests; orchestration subagents (worker, summarizer, prover).
- result: f(8)=5 and f(10)=6 [verified-here], so f(n) is exact for all n<=15. Found a third, inequivalent 12-point set with h=7. The Python search is too slow beyond n=12.
- evidence: data/small_records.json, tests/test_known_facts.py::test_small_records, kb/methods/search_engineering.md
- decision: the first Track U task is a CP-SAT/CEGAR or compiled search engine aimed at f(16).

## 2026-10-13T23:20Z P1 exact realizability oracle and forbidden-core library (n<=7)
- tried: worker built e757/realizability.py (exact Fraction simplex for order feasibility with Farkas certificates, forced-relation detection by row-space membership, deletion-filter cores) and enumerated all ordered midpoint patterns on n<=7.
- result: counts and 44 minimal cores (<=5 edges) [verified-here]; two clean structural lemmas extracted and verified: monotone midpoints (K30) and no medial triangle (K31). Scout: Gyarfas-Lehel has nothing beyond F7; Henning-Yeo 2021 full text unobtainable (closed access, no preprint), so HY-tight structures must be found computationally. Novelty baseline: CLEAR.
- evidence: data/forbidden_ordered_n7.json, experiments/20261013-2257-forbidden-library/README.md, kb/notes/gyarfas_lehel_1995.md, kb/notes/henning_yeo_2021_affine.md, results/reviews/baseline__scout__20261013T230359Z.md
- decision: continue; add K30/K31 and the cores as explicit SAT constraints in the n=16 CEGAR; waiting for the c_hyp table.

## 2026-10-13T23:30Z U1 midpoint-map annealing at n=16 (first 25 min)
- tried: e757/anneal.py, 4 processes (n=16 saturated x2, n=16 with one free vertex, n=18), cost = log2(1 + #independent (T+1)-sets) + collision penalties; exact re-check of every candidate.
- result [heuristic]: ~680 states/s per process at n=16; 20.8% of 2500 random linear saturated maps at n=16 are exact (4,5)-sets (float and exact agree), so realizability is NOT the bottleneck; alpha is. Best exact h at n=16 is 10 (n=18: 11). Pure hypergraph annealing never reached alpha 9 at n=16.
- evidence: experiments/20261013-2257-anneal16/README.md, best.json, logs/
- decision: continue the job in the background; the decisive question is abstract (does class O admit alpha<=9 at n=16?), now running in experiments/20261013-2257-chyp-table (run_feas.py 16 9).

## 2026-10-14T00:15Z P1 abstract constant c_hyp(n) for n=5..15
- tried: worker built e757/cpsat_model.py (CP-SAT, eager alpha clauses per (T+1)-subset; lazy loop kept but 15x slower; lazy F7 no-goods); c_hyp with/without F7-freeness.
- result [verified-here]: c_hyp(n) = 4,4,5,5,6,6,7,7 for n=5..12 (solver-only), = HY bound = f(n); F7-freeness matters only at n=7 (4 -> 5). n=13,14,15: 8,8,9 modulo Henning-Yeo (solver finds the witness; UNSAT below comes from HY). n=16 T=9 undecided after >1 h without K30.
- evidence: experiments/20261013-2257-chyp-table/{table.md,witnesses.json,check.py}
- decision: add K30/K31/cores as explicit clauses (sound: proved consequences of realizability) and rerun n=16; sweep n=18..25.

## 2026-10-14T00:50Z U1 annealer stopped (superseded by exact methods)
- tried: 4 annealing processes for ~95 min (n=16 saturated x2, n=16 one free vertex, n=18).
- result [heuristic]: n=16: ~4.0M states evaluated, 28,589 genuine (4,5)-sets reached, exact h distribution 10/11/12 only, never 9; n=18: 3,196 genuine sets, best h=11. Realizability is cheap (~0.6-1.5% of visited states, ~20% of random linear maps), alpha is the obstacle.
- evidence: experiments/20261013-2257-anneal16/best.json, README.md
- decision: stop (load 15 on 4 cores); CPU goes to the exact CP-SAT decision at n=16 (experiments/20261014-0030-n16-decision) and the sweep n=18..25.
