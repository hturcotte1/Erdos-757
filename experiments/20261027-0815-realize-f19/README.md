# f(19): exact realizability of cell (19,16,8,Delta<=4)   [verified-here, unrefereed computation]
Result: **f(19) = 11.** Of the 956 classes of cell(19,16,8,4) (list of experiments/20261027-0340-induction-n28-n29-f25), 778 are realizable and 178 are not
(complete sweep, no node cap hit; results_19_16_8.json). Each realizable class has a 1-parameter family (dim 1 after affine normalisation).
The first 40 realizable classes were re-verified on integer sets (verify_19_16_8.json): all (4,5) (e757.core.is_45_set), exactly 16 APs (= m), h = 11 (e757.core.alpha).
Claim C008 (results/claims/C008-f19-h11.json; set_19pt_h11.json = class 40 of the list; other sets in sets_19_16_8_realizable.json): frozen verifier output
"PASS NO-IMPROVEMENT C008-f19-h11 n=19 h=11 ratio=11/19" (new_claim_19pt.log). An independent brute force over all 4-subsets and a DFS for the maximum Sidon subset also give (4,5) True, h = 11.
Henning-Yeo gives h >= ceil((9*19+6)/17) = 11, hence f(19) = 11 (11/19 > 4/7: not a record).
The (19,17,8) saturated cell (785,127 classes) was therefore not needed and NOT run (results_19_17_8_partial.json).
## Method and completeness
rexact.c is a C port of rexact.py (experiments/20261027-0400-realize-21-18-9, whose README has the full statement): exhaustive backtracking over all injective midpoint labellings,
exact solution space (RREF mod 2^61-1; all minors < p so rank and zero-tests equal those over Q), cuts only on forced EQ / weak-Sidon / non-linear forced APs, all necessary for a (4,5)-set.
NOT = no (4,5)-set whose AP hypergraph contains the class exists. REAL = a labelling with no forced event; the integer point is rebuilt over Q (verify_lab.py) and checked.
Added here: optional env NODECAP (unset, no CAP outcomes).
Cross-check rexact.py vs rexact_c on 12 classes (6 REAL, 6 NOT; sample12.txt): identical outcomes and node counts (16,16,87,18,18,18; 2478,622,669,652,1096,622).
Controls (A_base, (10,7,4), (14,12,6), (17,13,7), route-4 negatives): see the 21-18-9 folder.
## Commands
```
gcc -O2 -o rexact_c rexact.c
grep '^FOUND' <list> > c19_16_8.txt; nice -n 10 ./rexact_c 19 < c19_16_8.txt > out_19_16_8.txt     # 3.6 min wall
python3 verify_lab.py c19_16_8.txt out_19_16_8.txt 19 verify_19_16_8.json 40
python3 scripts/new_claim.py --slug f19-h11 --set-file experiments/20261027-0815-realize-f19/set_19pt_h11.json --notes '...'
ALL=0 python3 run_cell.py sample12.txt 19 xcheck
```
