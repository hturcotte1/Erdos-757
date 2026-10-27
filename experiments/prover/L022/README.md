# L022 work folder: I11 on the realizable class R (route "the realizable class only")

Prover run of 2026-10-27 (about 05:20-07:50 UTC). Certificate: results/proofs/L022-i11-realizable-route.md (submitted; unrefereed).
All scripts use exact integer / Fraction arithmetic; run from this folder with `nice -n 10` and a `timeout`.

## Question
Can the order structure of a (4,5)-set (midpoint map, extreme points, K30, K31, realizability of the pieces) prove I11
(11 tau <= 3n + 2m) on the class R of AP hypergraphs of finite (4,5)-sets, or reduce it to a finite computation, beyond
the minimal-counterexample theory of L017/L018 for the abstract class C?

## Answer (short)
No proof and no finite reduction. Proved instead (hand proofs, unrefereed):
- Theorem 1: the AP relations of any set with injective midpoints are linearly independent (maximum principle), hence R is
  closed under deleting edges as well as vertices (and under disjoint unions); the minimal-counterexample theory of C,
  including edge-criticality (L017 Thm 1(g)), transfers to R verbatim.
- Theorem 2 (valid for every linear vertex-critical violator, so in C and R): of the seven Hall-deficient patterns of
  L017 Theorem 4 only (a), (b), (f) survive: (c1), (c2), (d) die by L018 6(b') (re-proved), (e) dies by a sub-extension
  argument (H[V(F1) + v + f] has slack s(F1) - 1, symmetrically for F2, and the slacks add to <= 1), (f) forces
  s(F1) = 1, s(F2) = 0, s(H) = -1, and F2 is a single edge or d, f are two non-adjacent pendants of F2.
- Theorem 2(vii) (every pattern, including (a)): a degree-2 co-vertex w of v with edge {w,p,q} in its component F makes
  {w,p} and {w,q} non-co-transversal in F.
- Corollary 3: under Conjecture P2' (tight Delta<=3 graphs other than a single edge have <= 1 pendant), s = -2 forces
  pattern (a) at every degree-3 vertex; with L018 Theorem 5(vi) (unrefereed) also pattern (f) disappears, and the only
  non-(a) case is s = -1, pattern (b) with a single-edge side and a slack-1 side of >= 27 vertices.
- Corollary 3' (Theorem 2 + stored lists, unrefereed): for n <= 30 every degree-3 vertex v of a minimal counterexample
  has H - v connected; so the step n = 30 (given I11 below) needs only the connected cells (29,17,11,3) and (29,23,12,3).
- Theorem 4: the order facts O1-O7 (extreme points, distinct steps, K30 at a vertex, half-line, reflection relations, K31).
- Theorem 5 (computation): Q10 = (10,7,4)#0 = {012,034,157,268,379,489,569} is a minimal non-realizable configuration
  with maximum degree 3 (all its proper edge subsets are realizable); every stored (21,18,9) obstruction has a degree-4 vertex.
Computation (unrefereed): realizability barely prunes the stored low-slack Delta<=3 lists (Theorem 5), and the local
configurations of the surviving patterns (b), (f) are realizable, so the order and realizability give no local kill.
The obstruction to the route: the transversal conditions are invariant under relabelling, all surviving local
configurations have realizable labellings, and the relevant pieces (m <= n-4) are always realizable in the data.

## Files and commands (outputs in out/)
| script | command | output | result |
|---|---|---|---|
| lib22.py | (library) | - | AP triples, roles L/M/R, K30/K31 tests, tau via ../L017/hyp.py |
| realize_lists.py | `python3 realize_lists.py 3_1_1 10_7_4 14_12_6 17_13_7 8_5_3 15_11_6 26_22_11 22_17_9`; `python3 realize_lists.py 12_10_5 19_16_8 6_3_2 9_4_3 10_8_4 13_9_5 16_10_6 23_16_9 20_15_8 17_14_7` (this second run was stopped by hand during 19_16_8, after its classes 0-373; the slack-2 cells were not reached) | realize_<cell>.jsonl, realize_run.log, realize_run2.log | Theorem 5 table (L022 Step 5.2) |
| order_checks.py | `python3 order_checks.py` | order_checks.txt | O1-O7 and rank = m on every stored set (C2) |
| edge_delete_check.py | `python3 edge_delete_check.py 1 10` | edge_delete_check.txt | Theorem 1(c): all deletions realized (C3) |
| test_subext.py | `python3 test_subext.py 1 40000 7 12`, `... 3 20000 7 11`, `... 2 60000 9 13` | test_subext_1.txt, test_subext_3.txt, test_subext_2.txt | Theorem 2 on linear vertex-critical violators outside C: 0 failures (C4) |
| test_patterns_e_f.py | `python3 test_patterns_e_f.py 1 20000` | (printed; in L022 C6) | random (e)/(f) configurations on stored pieces: (*) never holds |
| test_ef_exhaustive.py | `python3 test_ef_exhaustive.py` | test_ef_exhaustive.txt | identities of Steps 2.2-2.3 wherever (*) holds (C6) |
| local_configs.py | `python3 local_configs.py` | local_configs.txt | local configurations of (b), (f) with an E_1 side realizable; F7 not (C5) |
| minimal_obstruction_10_7_4.py | `python3 minimal_obstruction_10_7_4.py` | minimal_obstruction_10_7_4.txt | Q10 = (10,7,4)#0 is a minimal non-realizable configuration (C7) |
| run_final_checks.sh | `bash run_final_checks.sh` | the files above, run sequentially | final reruns of C2-C5 |

Inputs: experiments/20261027-0300-transversal-richness/inputs/cell_*.txt (stored class lists, from the refereed tarballs of
L012-L016 and the n = 27 worker run); experiments/20261027-0400-realize-21-18-9/rexact.py (exact realizability tool,
unrefereed); data/small_records.json; results/claims/C001-C006 (C006 appeared during the run).

## Caveats
- rexact.py is an unrefereed tool; its pruning is sound (forced coincidences hold on the whole solution space), and every
  positive answer was re-checked by an explicit integer (4,5)-set with exactly the given APs.
- The random tests C4 are not deduplicated up to isomorphism and never produced pattern (f); C6 exercises the identities.
- Nothing here proves I11 on R for any n beyond the range already known on C (n <= 27, L016).
