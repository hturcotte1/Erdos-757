# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: EXTENSION (+48 h granted by the user 2026-10-17 00:5x UTC; ends about 2026-10-18 23:06 UTC); GOAL.md unchanged (protected), status.sh shows clause C
Last updated (UTC): 2026-10-17 01:00
Phase/track: extension plan: (1) conjecture I11 11tau<=3n+2m falsify+document; (2) degree-3 route to f(16) via the (15,9,6)/(15,10,6) cells; (3) f(16) if (2) allows; (4) Q11 background; (5) hedge 4-point extensions
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results (details: results/LEDGER.md, kb/known_results.md K30-K49)
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]; Lower: c* >= 9/17 [published, via Henning-Yeo 2021]. Neither improved.
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L006 ACCEPTED (K13, K41, K43, K45, K46, K48): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes; no 16-pt record contains a saturated extremal 14-pt set; no extremal 14-pt set contains an extremal 12-pt set.
- K30 monotone midpoints, K31 no medial triangle, K44 degree bound; K47 structure of the 2,910 classes; K49 extremal (n-2)-subset trend (100% -> 99.7% -> 49.5% -> 0%).
- kb/notes/extension_lemmas.md: Lemmas E, U, Δ, Δ' [derived-here; falsifier HOLDS-ON-DATA].

## Running jobs / agents
- (14,11,alpha<=8) DFS, 4 workers at nice 19, 1041/3437 prefixes at 00:57, 0 patterns; resumable (relaunch: python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 19 --tag n14_m11).
- falsifier: I11 on all data + abstract class (experiments/falsify/i11-inequality); worker: CP-SAT (14,11) with deletion constraints (experiments/20261017-0100-n14m11-deletion-cpsat); worker: DFS cost probe for cells (15,9,alpha<=9), (15,10,alpha<=9) (experiments/20261017-0105-probe-n15-cells).
- Documentation audited three times in the first 72 h (last 2026-10-16 18:10 UTC); main = merge 414628a.

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by any solver, even with the Henning-Yeo deletion constraints (D15, D16, D24); a record would need a (14,11) extremal subset containing no extremal 12-subset (K48), or no extremal 14-subset at all.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35). (H1) HY tight at even n<=22 vs (H2) wall at 16.
- [verified-here] Q8 holds on realizable data (K34) but fails abstractly without >=5-edge cores (K38/K39); Track L has no proof idea.

## Next 3 actions
1. Read the probe: if the (15,9)/(15,10) cells cost <= ~60 CPU-h, run them with the existing engine (prefix split) and realize survivors; else build the unordered degree-bounded generator (nauty) with validation on (12,10) -> 54,243 and (14,12,Δ<=3) -> 700.
2. Record I11 as [conjecture] with its data coverage and implications (c* >= 6/11, f(16) = 10) in kb/; if the CP-SAT (14,11) run is INFEASIBLE, certificate L007 + referees.
3. Checkpoint every 2-3 h; final report/merge again before 2026-10-18 23:06 UTC.
