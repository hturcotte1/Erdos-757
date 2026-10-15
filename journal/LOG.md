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

## 2026-10-14T08:00Z U/P1 census: thousands of 12-point extremal sets
- result [verified-here]: K40. 3,980 affine classes of 12-point (4,5)-sets with h=7 from a partial abstract census (26,974 solutions, TIMEOUT); ~15% of abstract extremal patterns are realizable; 33 random ones re-judged by judge/judge.py: all PASS h=7.
- meaning: the known records are a tiny sample; extremal sets at n=12 (and presumably 14) are abundant. The absence of any abstract alpha<=9 pattern at n=16 (three methods) is therefore the whole story for Track U.
- evidence: experiments/20261014-0610-extremal-census/results/
- decision: after the n=15 streams end (~08:00), run witness-mode sweeps at n=18,20,22; keep the (14,12) census running.

## 2026-10-14T08:10Z U n=15 layer-1 streams finished (2 h each); sweep launched
- result [heuristic]: class O' on 15 vertices with alpha<=9: m'=9 and m'=10 found NO solution in 2 h each (UNSAT not proven); m'=11 has >= 3,935 solutions (incomplete). So the degree bound deg(v)<=3 for a 16-point extremal hypergraph remains conditional (D15-type limitation).
- launched: realizability-CEGAR sweep n=18 (eager), 20, 22, 23, 25 (hybrid), 1 h per size, 3 workers, resumable (experiments/20261014-0030-feasible-sizes/results). Witness mode only: a SAT answer would be a record candidate; TIMEOUT adds to the heuristic picture.
- evidence: experiments/20261014-0550-n16-layered/results/n15_m*_progress.json, prod/run.log
- decision: Track U stays open only through these witness-mode runs; main effort on verified partial results and the final report.

## 2026-10-14T09:25Z U sweep: n=18 witness search UNKNOWN after 1 h
- result [heuristic]: realizability-CEGAR at (18, T=10, m=16) with K30/K31/cores found no witness and no refutation in 3600 s (3 workers). n=20 running. Census chain now on (14,12).
- evidence: experiments/20261014-0030-feasible-sizes/results/n18_T10_m16.json

## 2026-10-14T10:00Z result L001 ACCEPTED (2-point extensions of A_base)
- result [verified-here]: certificate L001 accepted at referee round 4 (rounds 1-3 verified the mathematics and demanded text fixes; round 4 added a Sidon-definition-only method over all of R^2). K13 and D6 upgraded; LEDGER row added. Scope: 2-point (hence 3-point) extensions only.
- evidence: results/reviews/L001-abase-two-point-extensions__referee__*.md

## 2026-10-14T10:40Z result exact census: 54,243 twelve-point extremal sets
- result [verified-here]: C DFS enumerates all class-O patterns at (12,10,alpha<=7): 2,226,490 labelled (1,113,245 up to reflection), 0 at m=9; after K31/4-edge-core filters 395,039; exact realization: 54,243 realizable (rigid) = affine classes of 12-point (4,5)-sets with h=7; all 5 known sets recovered; CP-SAT's 30,559 all present; judge passed 50. (14,12) estimated 55-70 h single-process: not launched.
- evidence: experiments/20261014-1005-census-dfs/, results/proofs/L002-census-12-point-extremal-sets.md
- decision: certificate L002 to referee; consider a prefix-split parallel DFS for (14,12).

## 2026-10-14T11:20Z U/P1 sweep n=18,20,22 UNKNOWN; 14-point extremal sets are plentiful too
- result [heuristic]: realizability-CEGAR witness searches at (18,10,16), (20,11,18), (22,12,20): UNKNOWN after 3600 s each (no record candidate, no refutation); n=23 running.
- result [verified-here]: partial CP-SAT census at (14,12,alpha<=8): 1,474 abstract solutions in 2 h, 146 exactly realizable = 146 affine classes of 14-point (4,5)-sets with h=8 (A_base is one of many); judge spot check on 40: see this entry's command output in the main session (all PASS, h=8). Sets saved in experiments/20261014-0610-extremal-census/results/n14_realizable_sets_partial.json.
- decision: (14,12) exact count via the prefix-split parallel DFS (worker); sweep continues at 23, 25 then ends.

## 2026-10-14T11:30Z P1 (14,12) exact census launched (prefix-split C DFS); CP-SAT census chain stopped
- launched: python3 -m e757.ordered_dfs_split 14 8 12 3 3 ... (2,537 depth-3 prefixes, 3 workers, resumable; est. 36-44 CPU-h; postprocess.py afterwards). Stopped the CP-SAT census chain (its (14,12) partial is harvested as K42; the (15,13) partial count was of marginal value).
- evidence: experiments/20261014-1005-census-dfs/README.md, n14/run.log

## 2026-10-14T13:00Z U census invariants: realizable and unrealizable extremal patterns are statistically alike
- result [verified-here]: over the 395,196 K31/core-filtered (12,10,alpha<=7) patterns (54,243 realizable), ~65 statistics: max degree <= 4, colour classes (k-1,k) and no reflection symmetry hold for ALL patterns; the only invariants separating realizable from unrealizable are weak (at most one degree-1 vertex; deg(0)+deg(n-1) >= 3). Realizability looks 'random-like' (~14%) with respect to local structure.
- launched: constrained (16,9,14) runs (glucose4, cadical153, CP-SAT x 2 tiers, 1 h each) -> experiments/20261014-1200-census-invariants/n16/*/run.log
- evidence: experiments/20261014-1200-census-invariants/{README.md,tables.md}

## 2026-10-14T13:25Z U sweep finished: all record-feasible sizes UNKNOWN in witness mode
- result [heuristic]: realizability-CEGAR witness searches with K30/K31/cores: n=18, 20, 22 (3600 s each), n=23 (m=19,20,21) and n=25 (m=21,22,23) (1200 s each): all UNKNOWN; no record candidate anywhere.
- evidence: experiments/20261014-0030-feasible-sizes/results/*.json
- decision: Track U witness searches exhausted for this run; remaining CPU to the (14,12) exact census and the constrained n=16 runs (results due ~13:40).

## 2026-10-14T14:25Z U constrained n=16 runs inconclusive; cadical killed
- result [heuristic]: with the census invariants (tiers 1 and 2) plus colour balance, (16,9,14) is UNKNOWN in CP-SAT and TIMEOUT in glucose4 (3600 s each); cadical153 runs killed after ~2 h (uninterruptible, outran their limit). D15 extended: invariants do not make n=16 tractable.
- evidence: experiments/20261014-1200-census-invariants/n16/*/run.log, README Outcomes
- decision: Track U closed for this run; CPU to the (14,12) exact census; next deliverables: L002 ACCEPT, L003 (14-point census), final report.

## 2026-10-14T15:30Z result L002 ACCEPTED: exactly 54,243 twelve-point extremal sets
- result [verified-here]: referee round 3 ACCEPT with a fourth independent pipeline (SAT enumeration + own C realizer); by-product: f(12) >= 7 without Henning-Yeo (alpha <= 6 UNSAT; every alpha <= 7 pattern saturated even with F7 allowed). K41/LEDGER/report updated.
- evidence: results/reviews/L002-census-12-point-extremal-sets__referee__20261014T152552Z.md

## 2026-10-14T15:30Z result L002 ACCEPTED: exactly 54,243 twelve-point extremal sets
- result [verified-here]: referee round 3 ACCEPT with a fourth independent pipeline (SAT enumeration + own C realizer); by-product: f(12) >= 7 without Henning-Yeo (alpha <= 6 UNSAT; every alpha <= 7 pattern saturated even with F7 allowed). K41/LEDGER/report updated.
- evidence: results/reviews/L002-census-12-point-extremal-sets__referee__20261014T152552Z.md

## 2026-10-14T17:00Z P1 exact counts of extremal sets for n<=11 (K43)
- result [verified-here]: saturated classes 1, 4, 66, 1262, 6644, 466,961 (n=6..11); non-saturated extremal patterns exist for all n<=11 (infinite families), none at n=12. n=13 skipped (CPU to the n=14 census).
- evidence: experiments/20261014-1430-small-counts/

## 2026-10-14T17:05Z P1 n=14 census relaunched with 4 workers
- the resumable prefix-split driver was restarted with P=4 after the small-counts job ended (235/2537 prefixes already done; nothing lost beyond partial prefixes). Command in experiments/20261014-1005-census-dfs/README.md (P=4 now).

## 2026-10-14T17:25Z kb novelty check of the census results: CLEAR
- scout: OEIS has no match for 1,4,66,1262,6644; no prior enumeration of (4,5)-set extremal classes; K30/K31 not in the digests or threads (arXiv API 429 today; baseline scan of 10-13 used).
- evidence: results/reviews/L002-census-12-point-extremal-sets__scout__20261014T171802Z.md

## 2026-10-14T21:05Z infra container restart (second); census relaunched
- the container restarted ~21:03 UTC; the n=14 census died at 427/2537 prefixes (resumable) and the L003 round-3 referee died on a session usage limit (reset 19:40 UTC). Census relaunched (P=4, skips done prefixes); referee round 3 relaunched.

## 2026-10-14T21:40Z result L003 ACCEPTED (saturated extremal counts n=6..11; infinite non-saturated families)
- referee round 3 ACCEPT (third independent enumerator; own non-saturated witnesses). Editorial points applied (title 'saturated', tags, 'near the given realization', n=7 clamp note in K43).
- evidence: results/reviews/L003-census-small-n-extremal-sets__referee__20261014T213511Z.md

## 2026-10-14T22:25Z infra third container restart; census relaunched (529/2537 done)
- restarts at 04:40, 21:03 and 22:20 UTC; the last two followed idle gaps of 40-90 min between turns. The census is resumable at prefix granularity (<= 4 partial prefixes lost per restart). Relaunched with the README command.

## 2026-10-15T07:25Z infra fourth container restart (07:22, after a usage-limit pause); census relaunched at 1440/2537

## 2026-10-15T16:30Z infra fifth container restart (16:29); census relaunched at 2316/2537

## 2026-10-15T16:42Z P1 n=14 census enumeration COMPLETE
- result: 205,529 class-O (14,12,alpha<=8) patterns up to reflection; 113,454,008,923 DFS nodes; 277,501 CPU-s across five relaunches (resumable prefix split). Post-processing (K31/core filters, exact realization, affine classes, judge spot check) launched.
- evidence: experiments/20261014-1005-census-dfs/n14/results/n14_m12_TOTAL.json

## 2026-10-15T18:45Z result n=14 census: 2,910 saturated extremal classes (K45, L004 submitted)
- 205,529 patterns -> 119,844 K31-free -> 46,419 after <=4-edge cores -> 2,910 realizable (rigid) = 2,910 affine classes; A_base present; judge 50/50. Open: the m=11 case (HY slack 1) - a CP-SAT decision run launched.

## 2026-10-15T20:45Z P1 (14,11) case: CP-SAT UNKNOWN after 7000 s; exhaustive DFS launched
- CP-SAT (K30/K31/cores, eager alpha, lazy F7) could not decide whether a class-O' pattern with (14, m=11, alpha<=8) exists. Launched the resumable prefix-split DFS at (14,11,alpha<=8) with 3 workers (experiments/20261014-1005-census-dfs/n14m11dfs); if it completes within the budget, the n=14 extremal count becomes complete (2,910 saturated + whatever m=11 realizable patterns yield).

## 2026-10-15T23:00Z result L004 ACCEPTED (2,910 saturated 14-point extremal classes)
- referee: independent realization of all 205,529 patterns (no pre-filters) reproduces 2,910 classes and the failure breakdown; completeness re-checked on 719 prefixes + all outside cubes refuted + reflection identity on all prefixes (no full second enumeration, ~34 CPU-h). Editorial fixes applied; K45/LEDGER state the completeness scope.
- evidence: results/reviews/L004-census-14-point-extremal-sets__referee__20261015T225426Z.md
