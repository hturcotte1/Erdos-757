# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: final checkpoint (budget ends 2026-10-16 23:06 UTC); PR #1 merged into main at about 18:25 UTC
Last updated (UTC): 2026-10-16 18:20
Phase/track: endgame complete; research closed for this run (results/FINAL_REPORT.md is the deliverable)
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results (details: results/LEDGER.md, kb/known_results.md K30-K49)
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]; Lower: c* >= 9/17 [published, via Henning-Yeo 2021]. Neither improved.
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L006 ACCEPTED (K13, K41, K43, K45, K46, K48): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes; no 16-pt record contains a saturated extremal 14-pt set; no extremal 14-pt set contains an extremal 12-pt set.
- K30 monotone midpoints, K31 no medial triangle, K44 degree bound; K47 structure of the 2,910 classes; K49 extremal (n-2)-subset trend (100% -> 99.7% -> 49.5% -> 0%).
- kb/notes/extension_lemmas.md: Lemmas E, U, Δ, Δ' [derived-here; falsifier HOLDS-ON-DATA].

## Running jobs / agents
- (14,11,alpha<=8) DFS, 4 workers, 706/3437 prefixes done at 18:20, 0 patterns; resumable (relaunch command in experiments/20261014-1005-census-dfs/README.md); Q11 stays open.
- No agents running. All documentation audited three times (last: 18:10 UTC, 114 verified fixes).

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by any solver, even with the Henning-Yeo deletion constraints (D15, D16, D24); a record would need a (14,11) extremal subset containing no extremal 12-subset (K48), or no extremal 14-subset at all.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35). (H1) HY tight at even n<=22 vs (H2) wall at 16.
- [verified-here] Q8 holds on realizable data (K34) but fails abstractly without >=5-edge cores (K38/K39); Track L has no proof idea.

## Next 3 actions (for a future run)
1. Cube-and-conquer at n=16 with the deletion constraints of D24, or a distributed exact DFS (~10^14 nodes); finish the (14,11) DFS (resumable).
2. Four-point extensions of the 2,910 classes (18-point records; one new point must be a new extreme) and two-point extensions of any (14,11) classes.
3. Realizability-aware enumerator for the n=13 census (D22); obtain Henning-Yeo 2021 for its equality structure (Lemma U).
