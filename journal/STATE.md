# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: EXTENSION (+48 h granted by the user 2026-10-17 00:5x UTC; ends about 2026-10-18 23:06 UTC); GOAL.md unchanged (protected), status.sh shows clause C
Last updated (UTC): 2026-10-17 15:54
Phase/track: extension: the I11 induction chain is complete and refereed: L007 (Q11 closed, K51), L008 (f(16)=10, K52), L009 (f(18)=11, K53), L010 (f(20)=12, K54), L011 (f(22)=13, K55) ACCEPTED x3 each; no (4,5)-set with <= 22 points beats 4/7. L012 (n=23 record cell: all AP-degrees <= 3) SUBMITTED, referee #1 + scout running; the degree-3 case is open (Q14).
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results (details: results/LEDGER.md, kb/known_results.md K30-K49)
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]; Lower: c* >= 9/17 [published, via Henning-Yeo 2021]. Neither improved.
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- L001-L006 ACCEPTED (K13, K41, K43, K45, K46, K48): A_base 2-pt extensions; 54,243 extremal 12-pt classes; saturated counts n=6..11; 2,910 saturated extremal 14-pt classes; no 16-pt record contains a saturated extremal 14-pt set; no extremal 14-pt set contains an extremal 12-pt set.
- K30 monotone midpoints, K31 no medial triangle, K44 degree bound; K47 structure of the 2,910 classes; K49 extremal (n-2)-subset trend (100% -> 99.7% -> 49.5% -> 0%).
- kb/notes/extension_lemmas.md: Lemmas E, U, Δ, Δ' [derived-here; falsifier HOLDS-ON-DATA].
- I11: 11 tau <= 3n + 2m holds on ALL data (0 violations; equality at (3,1,1),(10,7,4),(12,4,4),(13,8,5),(14,12,6)) and on the abstract class for n<=15 via window cells [computer-assisted]; implies c* >= 6/11 if true in general [conjecture]. L007 SUBMITTED+ACCEPT#1: no (14,11) extremal set (Q11 closed; 2,910 complete). (16,14,7) EMPTY and (16,13,7) impossible => f(16) = 10 [derived-here, certificate L008 in preparation]. K50: non-saturated extremal 15-point sets exist (judged C001/C002).

## Running jobs / agents
- (14,11,alpha<=8) DFS, 4 workers at nice 19, 1041/3437 prefixes at 00:57, 0 patterns; resumable (relaunch: python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 19 --tag n14_m11).
- workflow: L012 referee #1 + scout. DONE: falsifier agent (I11, n=16..23 cells); e757/fn_bounds knows f(16)=10, f(18)=11, f(20)=12, f(22)=13; L007 x3 ACCEPT; I11 falsifier; CP-SAT (14,11) UNKNOWN (D21); probe (D25); record hunt (D26, K50); (16,14,7) decision; (14,11) DFS stopped at 1,081/3,437 (superseded by L007).
- Documentation audited three times in the first 72 h (last 2026-10-16 18:10 UTC); main = merge 414628a.

## Live hypotheses
- [heuristic] Wall at n=16 (f(16)=10): no abstract alpha<=9 pattern found by any solver, even with the Henning-Yeo deletion constraints (D15, D16, D24); a record would need a (14,11) extremal subset containing no extremal 12-subset (K48), or no extremal 14-subset at all.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17 (K35). (H1) HY tight at even n<=22 vs (H2) wall at 16.
- [verified-here] Q8 holds on realizable data (K34) but fails abstractly without >=5-edge cores (K38/K39); Track L has no proof idea.

## Next 3 actions
1. L012: referee #1 + scout -> fixes -> referees #2/#3 (fable) -> K56, LEDGER, START_HERE, FINAL_REPORT.
2. Final documentation audit workflow (find/verify/apply + safety review), FINAL_REPORT final version, STATE; then PR to main and merge (extension ends 2026-10-18 23:06 UTC; merge with margin, target <= 20:00 UTC on 10-18, earlier if everything is done).
3. Optional if time remains: the degree-3 case of (23,21,10) (Q14) needs a new idea (K30/K31 inside the unordered engine, or a realizability prune); record ideas in kb/ideas_backlog.md.
