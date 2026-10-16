# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-16 00:10
Phase/track: endgame (budget ends 2026-10-16 23:06 UTC): verify L005, document everything, merge PR #1 to main
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L004 ACCEPTED (K13, K41, K43, K45): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes
- K30 monotone midpoints, K31 no medial triangle, K44 degree bound [verified-here]; K32-K39 census/abstract facts
- L005 SUBMITTED (00:07): no 16-point (4,5)-set with h<=9 contains a saturated extremal 14-point set (all 2,910 classes, 4,970,208 (4,5) 2-extensions, all h=10). Referee #1 + brute-force cross-check + scout running (workflow).
- kb/notes/extension_lemmas.md [derived-here, falsifier HOLDS-ON-DATA]: Lemma E (one-edge extension, h+1 iff universal vertex), Lemma U (HY obstruction to universal vertices), Lemma Δ (16-point record: deg <= m-9; exactly 2 new APs in a 2-pt extension).

## Running jobs / agents
- Workflow verify-l005-round1: referee#1 (Opus), bruteforce_sample worker (Sonnet), scout. Then: address findings, referee #2 (fresh), LEDGER/K46/report.
- (14,11,alpha<=8) DFS, 2 workers (relaunch: python3 -m e757.ordered_dfs_split 14 8 11 3 2 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 12 --tag n14_m11); 79/3437 prefixes, 0 patterns; will not finish (Q11 open).
- STOPPED: n=13 saturated census (infeasible: 54.7M patterns in 8/1811 prefixes; D22, Q12).
- PR #1 (claude/intelligent-pasteur-22z06m -> main) open; merge at ~21:00 UTC after the final checkpoint.

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by CP-SAT/SAT/annealing (D15, D16); L005 removes all saturated extremal 14-subsets as seeds; a record would need a (14,11) extremal subset (Q11) or none.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35). (H1) HY tight at even n<=22 vs (H2) wall at 16.
- [verified-here] Q8 holds on realizable data (K34) but fails abstractly without >=5-edge cores (K38/K39); Track L has no proof idea.

## Next 3 actions
1. Workflow result: fix L005 per referee #1, run referee #2 (fresh) if needed, then LEDGER row, K46 in known_results, tests/test_ext14_all.py, FINAL_REPORT R9 status.
2. Keep the (14,11) DFS running on spare cores; re-arm the session waiter; relaunch after any container restart.
3. ~21:00 UTC: final checkpoint (STATE, LOG, FINAL_REPORT), merge PR #1 into main, run status.sh. Budget end 23:06 UTC.
