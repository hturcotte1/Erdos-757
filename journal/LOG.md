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

## 2026-10-14T04:50Z P1/L container restart; harvest of the night's results
- event: the container restarted ~04:40 UTC; all background jobs died (n=16 CP-SAT decision m=13/m=14, realizable-CEGAR, sweep at n=18) with no results saved. Three workflow agents died on a session usage limit (reset 03:50 UTC). Lesson: every long job must write per-case JSONs and be resumable.
- harvested [verified-here]: (1) n=8 forbidden library: 46,281 ordered patterns = 16,568 realizable + 28,697 order-infeasible + 498 forced extra AP + 518 forced repeated difference; 243 new minimal cores (287 total for n<=8); catalogue of all 11 connected linear configurations with <=4 edges on <=8 vertices, 145 labelings, every order checked (experiments/20261014-0005-forbidden-n8, K33); independently recomputed by a verifier with its own oracle: ACCEPT, all verdicts match. Triangle: of 7 labelings, 2 shared-midpoint and 1 medial are forbidden, 4 realizable. Pasch: realizable in exactly one labeling/order, e.g. {0,4,7,8,9,14}. New: the medial 4-cycle (Varignon) is forbidden in every order.
  (2) Q8 falsifier (7 tau(K) <= 3|R| + 2e_2 + 4e_1): NONE-FOUND over all 3^n states of the 7 record sets (A_base: 3,253,568 valid states), 1800 random saturated sets at n=12,14,16 (~560M states), 752 gluings + 300 amalgams (~11.5M states). Q8 is tight on A_base with D empty (7*6 = 42 = 3*14) and on each 12-point set after avoiding one point. D4 violations reproduce. [heuristic]
  (3) LP fit over 1,333,217 realizable AP hypergraphs (all induced subsets of records + random saturated sets n<=20): HY slack >= 0 everywhere, min slack 3 for n>=10; best fitted inequality tau <= 3n/7, tight only at A_base; exact frontier tau <= (33/119)n + (3/17)m valid on all rows. No row with D/n < 5/7. [heuristic]
  (4) Independent DFS engine e757/ordered_dfs.py (+C): agrees with CP-SAT for n=5..12 (n=12 in ~55 s, 30M nodes), but its n=16 estimate is ~1e14 nodes: not a certificate engine; small-n cross-check only.
- observation: Q8 with D empty is exactly h >= 4n/7. The community candidate is an inductive strengthening of "c* = 4/7"; all our data is consistent with c* = 4/7 (which would force f(16)=10).
- decision: relaunch n=16 as a resumable case split; verify Q8 independently; Track L to target an inductive inequality of Q8 type.

## 2026-10-14T04:55Z L Q8 independently confirmed; n=16 case split and second encoding under way
- result: independent C re-implementation reproduces every Q8 count (A_base 3,253,568 valid states / 0 violations / 94,544 equalities; all seven records; 18 pool sets). Recorded as K34.
- running: n=16 resumable case split (30 cases; experiments/20261014-0450-n16-cases), slack landscape n<=14 (experiments/20261014-0500-slack-landscape), independent pysat encoding of class O' (e757/sat_indep.py) for the certificate.
- decision: Track L target = an inductive inequality of Q8 type; pick constants after the slack landscape.

## 2026-10-14T05:50Z U/P1 n=16 case split abandoned; layered n=15 -> n=16 extension search
- tried: 30-case CP-SAT split (vertex-1 edge x m) with K30/K31/cores; first 4 cases all TIMEOUT at 3000 s (experiments/20261014-0450-n16-cases/results/*.json).
- observation [verified-here]: f(n) = ceil(n/2)+1 for 6 <= n <= 15 and n=17, which equals the Henning-Yeo bound exactly for 6 <= n <= 23 (python3 -m e757.fn_bounds); and in the abstract class O' the saturated extremal value is tau = n/2 - 1 at every even n <= 14, i.e. the trivial Gyarfas-Lehel bound h >= ceil((n+1)/2) is tight at even n <= 14 in both classes (experiments/20261014-0500-slack-landscape). So no lower-bound improvement exists for n <= 15; whether the wall appears at n=16 is exactly the open question.
- decision: deletion-of-maximum lemma reduces the n=16 search to the n=15 extremal structures (alpha <= 9, m' = 9..13) plus a small extension step; dispatched to the CP-SAT worker as a resumable job. Sweep n=18..25 postponed.

## 2026-10-14T06:55Z L Q8 falsified on the abstract class; structure lemmas survive
- result [verified-here]: Q8 fails for abstract class O (+K30, K31, <=4-edge cores) at n=12 (K38: 60 of 18,180 census members, all at |D|=2, slack -1); every violator contains a >=5-edge forbidden core and is non-realizable. GL-tight structure lemmas (kb/notes/gl_tight_structure.md) survive ~80k flip instances. Census: >= 25,484 abstract (12,10,alpha<=7) solutions, D-empty Q8 slack exactly 1 for all of them (tau = 5 = floor(36/7)).
- meaning: the 4/7 conjecture (Q8) needs the deeper forbidden cores; it is not an abstract linear/F7/midpoint statement. The n=15 streams m'=9,10 have found no solution in 50 min (UNSAT not yet proven); m'=11 has 2,282+ solutions.
- decision: Track L = inductive Q8-type inequality WITH cores as the lemma source; Track U at n=16 awaits the census trend and the stream outcomes; final report is a living document.

## 2026-10-14T07:35Z L inductive-inequality fit: abstract vs realizable
- result: K39. Realizable data: b = 3/7 exactly at Q8 weights; abstract census needs b = 31/70, and every abstract violator contains a 5/6-edge core. Hard local type (3,0,0) dominates in both classes; what differs is frequency (7,456 abstract hypergraphs with irreducible tight states at |R|=11 vs 3 realizable states).
- meaning: an abstract (core-free) proof can at best reach b = 31/70 on this data (and likely worse at larger n); a proof of Q8 itself must discharge the (3,0,0) type using 5- and 6-edge cores.
- evidence: experiments/20261014-0700-inductive-fit/
- decision: no prover attempt yet (no proof idea for the (3,0,0) discharge); continue harvesting exact data; after the n=15 streams end, run witness-mode sweeps at n=18, 20, 22.
