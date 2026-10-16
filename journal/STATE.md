# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-16 03:05
Phase/track: endgame (budget ends 2026-10-16 23:06 UTC): L005 ACCEPTED x2 at 01:37 (K46) and K47 recorded; documentation audit, final checkpoint, merge PR #1 to main
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L004 ACCEPTED (K13, K41, K43, K45): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes
- K30 monotone midpoints, K31 no medial triangle [verified-here]; K44 degree bound [derived-here]; K32-K39 census/abstract facts
- L005 ACCEPTED x2 (01:37; K46): no 16-point (4,5)-set with h<=9 contains a saturated extremal 14-point set (all 2,910 classes, 4,970,208 (4,5) 2-extensions, all h=10); scout CLEAR.
- L006 ACCEPTED x2 (08:31; K48): no 14-point (4,5)-set with h<=8 contains an extremal 12-point set (54,243 classes; 51,264,727 T1b pairs all h=9); scout CLEAR.
- K49 extremal (n-2)-subsets: 100% (n<=9, 11), 99.7% (n=10), 49.5% (n=12), 0% (n=14) of extremal classes contain one [verified-here counts; trend heuristic].
- K47 structural census of the 2,910 classes [verified-here]: degrees in {2,3,4}, 3 degree sequences, 137-150 max Sidon subsets, no mirror symmetry, no extremal 12-point subset, GL balance everywhere.
- kb/notes/extension_lemmas.md [derived-here, falsifier HOLDS-ON-DATA]: Lemma E (one-edge extension, h+1 iff universal vertex), Lemma U (HY obstruction to universal vertices), Lemma Δ (16-point record: deg <= m-9; exactly 2 new APs in a 2-pt extension).

## Running jobs / agents
- (14,11,alpha<=8) DFS, 4 workers, restarted 02:26:29 UTC after the 7th container restart (max 20 h; relaunch: python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11); 150/3437 prefixes done at 02:26, 0 patterns; about 36 prefixes/h (LOG 02:02Z), so it will not finish in the run (Q11 open).
  - Documentation-audit workflow (missing experiment READMEs, index READMEs, kb consistency audit with proposed edits verified by independent agents; LOG 23:15Z) relaunched 02:02 and resumed 02:26 UTC (LOG); apply its accepted edits before the final checkpoint.
- STOPPED: n=13 saturated census (infeasible: 54.7M patterns in 8/1811 prefixes; D22, Q12).
- PR #1 (claude/intelligent-pasteur-22z06m -> main) open; merge at ~21:00 UTC after the final checkpoint.

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by CP-SAT/SAT/annealing (D15, D16); L005 removes all saturated extremal 14-subsets as seeds; a record would need a (14,11) extremal subset (Q11) or none.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35).
  - [conjecture] (H1) HY stays tight at even n<=22 (records at 16..22) vs (H2) wall at 16 (f(16)=10); the data lean to H2 [heuristic].
- [verified-here] Q8 holds on every tested realizable state (every valid (S,D) state of the 7 record sets, about 570M sampled states; K34: evidence, not proof) but fails in the abstract class unless >=5-edge cores are used (K38/K39); Track L has no proof idea.

## Next 3 actions
1. Apply the accepted fixes of the running documentation audit (workflow relaunched LOG 02:02Z, resumed 02:26Z; proposals and verifier corrections in experiments/20261015-2310-kb-audit/README.md and experiments/20261015-2310-doc-verify/), including FINAL_REPORT section 4, which still says 79 prefixes done on 2 cores (now 4 workers); run python3 -m pytest -q if e757/ changed.
  2. Keep the (14,11) DFS running (4 workers, nice 10, all 4 cores; about 36 prefixes/h, so it cannot finish before the 23:06 UTC budget end; check the rate at each checkpoint; relaunch after any container restart). Re-arm the background waiter, which is a shell loop: `timeout 7000 bash -c 'until [ $(ls experiments/20261014-1005-census-dfs/n14m11dfs/results/*.done | wc -l) -ge 3437 ]; do sleep 120; done'`. It started 02:26 UTC and expires about 04:23 UTC; it is documented only here. If the DFS ever finishes, postprocess and certify the m=11 case (completes L004/L005).
3. ~21:00 UTC: final checkpoint (STATE, LOG, FINAL_REPORT), merge PR #1 into main, run status.sh. Budget end 23:06 UTC.
