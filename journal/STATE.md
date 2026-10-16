# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-16 08:42
Phase/track: endgame (budget ends 2026-10-16 23:06 UTC): research closed at 16:12 UTC (last n=16 attempts D24 UNKNOWN/TIMEOUT, Q1 open; L001-L006 ACCEPTED, K46-K49 recorded); documentation audit, final checkpoint, merge PR #1 to main
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L004 ACCEPTED (K13, K41, K43, K45): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes
- K30 monotone midpoints, K31 no medial triangle [verified-here]; K44 degree bound [derived-here]; K32-K39 census/abstract facts
- L005 ACCEPTED x2 (01:37; K46): no 16-point (4,5)-set with h<=9 contains a saturated extremal 14-point set (all 2,910 classes: 141,153 (4,5) T1a single extensions, 4,970,208 (4,5) T1b pairs and 122,220 T2 lines, all h=10; the completeness of the 2,910 is inherited from the K45 census, re-checked independently by sampling plus consistency checks, not by a second full enumeration); scout CLEAR.
- L006 ACCEPTED x2 (08:31; K48): no 14-point (4,5)-set with h<=8 contains an extremal 12-point set (54,243 classes; 51,264,727 T1b pairs all h=9); scout CLEAR.
- K49 extremal (n-2)-subsets: 100% (n<=9, 11), 99.7% (n=10), 49.5% (n=12), 0% (n=14) of extremal classes contain one [verified-here counts; trend heuristic].
- K47 structural census of the 2,910 classes [verified-here]: degrees in {2,3,4}, 3 degree sequences, 137-150 max Sidon subsets, no mirror symmetry, no extremal 12-point subset, GL balance everywhere.
- kb/notes/extension_lemmas.md [derived-here, falsifier HOLDS-ON-DATA]: Lemma E (one-edge extension, h+1 iff universal vertex), Lemma U (HY obstruction to universal vertices), Lemma Δ (16-point record: deg <= m-9; a record extending one of the 2,910 classes would need exactly 2 new APs, and K46/L005 excludes it), Lemma Δ' (deletion version: if h(A) = f(n), A-p-q is extremal and f(n-2) = f(n)-1, then deg p + deg q - eps <= m - (17 tau - 5n - 7)/3, where tau = n - f(n) and eps = 1 iff p, q lie in a common AP; falsifier HOLDS-ON-DATA, 0 violations, experiments/falsify/deletion-lemma/README.md).

## Running jobs / agents
- (14,11,alpha<=8) DFS, 4 workers, started 12:34:17 UTC after the D24 solver runs, with `timeout 10h` (so it ends at about 22:34 UTC; relaunch, resumable: python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11); 558/3437 prefixes done at 16:12 UTC (FINAL_REPORT section 4), 646 at 16:40 and 678 at 17:32 UTC by .done markers, 0 patterns, 0 timeouts in all 678; the rate was about 35 prefixes/h from 12:34 to 16:12 (127 prefixes), but indices 558-645 were cheap (88 prefixes in 28 min, mean wall about 76 s each per worker) and that burst did not last: the 32 prefixes finished since 16:40 average about 384 s each, i.e. again about 35-40 prefixes/h on 4 workers (mean wall per 50-prefix block 154-573 s for indices 0-549), so the remaining about 2,760 prefixes would need roughly 70-80 h, far beyond the 22:34 UTC timeout and the 23:06 UTC budget end, and it will not finish in the run (Q11 open) [heuristic; re-measure at the checkpoint].
  - Documentation audit 2 was applied by 03:29 UTC (69 independently verified fixes in 30 files, commit a33e4a1, plus post-audit corrections ca70448; LOG 03:30Z); a final documentation audit of the results added or revised since then (L006/K48, K49, Lemma Δ', D23/D24 including the CNF variant, the DFS status) is the remaining endgame step (LOG 16:12Z); apply its accepted edits before the final checkpoint.
- STOPPED: n=13 saturated census (infeasible: 54.7M patterns in 8/1811 prefixes; D22, Q12).
- PR #1 (claude/intelligent-pasteur-22z06m -> main) open; merge at ~21:00 UTC after the final checkpoint.

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by CP-SAT/SAT/CaDiCaL/annealing (D15, D16); D24: with the Henning-Yeo deletion constraints (which use L005 and so the K45 census) CP-SAT and CaDiCaL were both UNKNOWN/TIMEOUT after 3.5 h at m=13 and m=14, no solution and no refutation. [verified-here, given the K45 census] L005 (K46, D23) removes all saturated extremal 14-point subsets as seeds; [verified-here] L006 (K48) shows that no 14-point (4,5)-set with h<=8 contains an extremal 12-point set. So a record would need a non-saturated (14,11) extremal 14-point subset (Q11; by K48 it has no extremal 12-point subset) or no extremal 14-point subset at all.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35).
  - [conjecture] (H1) HY stays tight at even n<=22 (records at 16..22) vs (H2) wall at 16 (f(16)=10); the data lean to H2 [heuristic].
- [verified-here] Q8 holds on every tested realizable state (every valid (S,D) state of the 7 record sets, about 570M sampled states; K34: evidence, not proof) but fails in the abstract class unless >=5-edge cores are used (K38/K39); Track L has no proof idea.

## Next 3 actions
1. Apply the accepted fixes of the final documentation audit once it has run (planned for the endgame, LOG 16:12Z; the previous audit was applied at 03:29 UTC, LOG 03:30Z); at the final checkpoint refresh the (14,11) DFS count and measured rate in FINAL_REPORT section 4 (it currently reads 558 prefixes at 16:12 UTC on 4 workers, 22 to 36 prefixes/h) and in this file, taking them from the .done files in experiments/20261014-1005-census-dfs/n14m11dfs/results; run python3 -m pytest -q if e757/ changed.
  2. Keep the (14,11) DFS running (4 workers, nice 10, all 4 cores; relaunched 12:34 UTC under `timeout 10h`, which ends it at about 22:34 UTC; 678/3437 prefixes done at 17:34 UTC, 0 patterns). The rate is bursty: about 44/h over 02:26-08:48 UTC and about 35/h over 12:34-16:12 UTC (17 to 75 per clock hour), then 112 in the 16:00-17:00 UTC hour (88 of them in 16:12-16:40) and 25 in 17:00-17:34 UTC. With 2,759 prefixes remaining it cannot finish before the 23:06 UTC budget end; check the rate at each checkpoint; relaunch after any container restart. The .done-count waiter of 02:26 UTC has expired (about 04:23 UTC); the waiter running now is `timeout 7000 bash -c 'until [ $(git status --short | wc -l) -ge 5 ]; do sleep 180; done'` (started 16:13 UTC, expires about 18:10 UTC); it is documented only here. If the DFS ever finishes, postprocess and certify the m=11 case (completes L004/L005).
3. ~21:00 UTC: final checkpoint (STATE, LOG, FINAL_REPORT), merge PR #1 into main, run status.sh. Budget end 23:06 UTC.
