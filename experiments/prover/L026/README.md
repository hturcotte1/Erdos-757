# experiments/prover/L026: the E1-hub (b-configuration) lemma (KT form and I11 form)

Certificate: results/proofs/L026-e1hub-lemma-kt-form.md (submitted 2026-10-27; unrefereed).

## Question
The panel synthesis (experiments/prover/panel-synthesis/SYNTHESIS.md, Sections 0, 3, 4) names the E1-hub
(b-configuration) lemma as the missing lemma on every route to c* > 9/17. Prove its KT form (L021 potential)
or reduce it to a finite computation; examine the I11 form structurally.

## Result (details and proofs in the certificate)
- PROVED [derived-here, unrefereed]: the I11 form when the outer graph G is tight (Theorem 13: fold +
  pair lemma; in C, given I11 at n(G) +- 2). Corollary 14: in a minimal counterexample to I11, pattern (b)
  occurs only with s(H) = -1, one side a single edge (an E1-hub) and the other side of slack 1; if s(H) = -2
  every degree-3 vertex has pattern (a) (with L022 Theorem 2(ii),(iii)). This removes Conjecture P2' from
  the pattern-(b) part of L022 Corollary 3 and gives the conclusion of L018 Proposition 6.2 without P2.
- PROVED: the merge lemma (Lemma 11: identifying an NC pair keeps tau, slack -3, A -27; NC pairs of graphs
  with slack <= 2 are blocked), the structure of positive deficiency (Lemma 9: a connected graph with DEF > 0
  is a member of L* or a p-piece tree, p odd <= 11) and the boundary count (Lemma 10, from Claim E).
- KT form reduced to Case 1* (Theorem 12): connected outer graph, DEF(G') = 0, -8 <= A(H) <= -1,
  8 <= A(G') <= 15, not all outer pairs adjacent, every fold deficiency-free, merges blocked; every outer
  vertex of G'-degree 2 is a cut vertex of G' with a pendant member K of L* (uses C10: no member of L* has
  a hub triangle), with a blocked replacement edge when both its edges leave K; corner pattern only in the
  empty cell (24,19,10); if a degree-2 outer vertex has non-adjacent partners then n(H) <= 73 (Theorem
  12(i), via the replacement M = Q + w + {w,a,b}, A(M) = A(C_hub) - 19, and Claim E); otherwise the outer
  triple has shape (j1) (all outer degrees 1) or (j2) (Theorem 12(j)).
- NOT proved: GAP A (KT form in shapes (j1), (j2)), GAP B (I11 form with s(G) = 1; L025, written in
  parallel, reduces it further to pendant triples). Neither is reduced to a finite computation; the finite
  family A1 (n(H) <= 73) is stated, not computed.
- Overlap: Lemma 11 = L025 Lemma 4 and Theorem 13 is contained in L025 Corollary 11(a); found independently.

## Files and exact commands (all run with nice -n 10, one process, under timeout; own code only)
`ownlib.py` (first draft, reviewed): exact tau / all minimum transversals, induced copies, exact DEF, C_3 test.
`$I` = /home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs

| check | command (from the folder named) | output | result |
|---|---|---|---|
| C1 pieces | `timeout 600 nice -n 10 python3 pieces_check.py > pieces_check_output.txt` (here) | pieces_check_output.txt | 32 pieces, weights 16,5,13,2,10; (L1) for all; no b-triple in any piece; only E_1 has an edge with two degree-1 vertices |
| C2 judge's hubs (draft) | `cd ../L017/out && python3 ../../L026/check_hubs.py <cells>` | check_hubs_part1/2/3.txt | 186 hubs, all P = 0 |
| C3 random lemmas (draft) | `python3 check_lemmas.py 7 1500 14` | check_lemmas_output.txt | 0 failures |
| C4, C5 (draft) | `python3 pieces_with_hubs.py`; `python3 hub_families.py 4 <cells>` | pieces_with_hubs_output.txt, hub_families_output.txt | E1-hubs inside pieces; hub in every optimal family |
| C6 merge lemma | `cd $I && timeout 3000 nice -n 10 python3 /home/user/Erdos-757/experiments/prover/L026/merge_check.py cell_3_1_1.txt cell_6_3_2.txt cell_8_5_3.txt cell_9_4_3.txt cell_10_7_4.txt cell_10_8_4.txt cell_12_10_5.txt cell_13_9_5.txt cell_14_12_6.txt cell_15_11_6.txt cell_16_10_6.txt cell_17_13_7.txt cell_22_17_9.txt cell_23_16_9.txt cell_26_22_11.txt cell_19_16_8.txt cell_20_15_8.txt cell_17_14_7.txt cell_23_21_10.txt` | merge_check_output.txt | 5,066 graphs, 8,118 NC pairs, 144 non-adjacent: tau identity 144/144, all blocked (43 common nbr, 10 saturated set, 91 F7), 0 violations |
| C7 stored hubs | `cd /home/user/Erdos-757/experiments/prover/L017/out && timeout 5400 nice -n 10 python3 /home/user/Erdos-757/experiments/prover/L026/hub_analysis.py ./L012/cells/cell_6_3_2_D3.txt ./L012/cells/cell_11_7_4_D3.txt ./L012/cells/cell_12_6_4_D3.txt ./L012/cells/cell_13_9_5_D3.txt ./L013/cells/cell_18_9_6_D3.txt ./L013/cells/cell_19_12_7_D3.txt /home/user/Erdos-757/experiments/20261027-0730-kt-cells/out/cells/cell_24_12_8_D3.txt` | hub_analysis_output.txt | 311 hubs (P = 0 each); Lemma 9 on 1,837 graphs ok; DEF(G') = 0 always; 443 large folds all DEF-free; A(H) in {-7,-4} for n(H) >= 22 |
| C8 Theorem 13 | `timeout 1500 nice -n 10 python3 i11_form_check.py $I/cell_3_1_1.txt $I/cell_10_7_4.txt $I/cell_14_12_6.txt $I/cell_17_13_7.txt <(zcat ../../20261027-0300-tight-cells-d4/lists/cell_17_13_7_D4.txt.gz) <(zcat ../../20261027-0300-tight-cells-d4/lists/cell_21_18_9_D4.txt.gz) ../L023/cell_25_23_11_D4.txt $I/cell_8_5_3.txt $I/cell_12_10_5.txt $I/cell_15_11_6.txt $I/cell_19_16_8.txt $I/cell_22_17_9.txt $I/cell_26_22_11.txt $I/cell_23_21_10.txt` (the run used decompressed copies of the two .gz lists in the session scratchpad) | i11_form_check_output.txt | 51 tight graphs: 0 b-triples; 2,039 slack-1 graphs: 0 b-triples |
| C10 hub triangles | `timeout 300 nice -n 10 python3 hubtriangle_check.py > hubtriangle_check_output.txt` (here) | hubtriangle_check_output.txt | no member of L* has a hub triangle (TOTAL 0); positive controls find them in the triangle, (12,6,4), (18,9,6) |
| A_base | `timeout 300 nice -n 10 python3 abase_check.py > abase_check_output.txt` (here) | abase_check_output.txt | tight, 143 min transversals, no NC pair, no b-triple |
| C11 replacement identities | `cd /home/user/Erdos-757/experiments/prover/L017/out && timeout 2400 nice -n 10 python3 /home/user/Erdos-757/experiments/prover/L026/replacement_check.py <the 7 cells of C7>` | replacement_check_output.txt | 385 degree-2 outer vertices: tau(C_hub) - tau(Q) rule ok; 281 replacements M in C_3 with A(M) = A(C_hub) - 19 |
| C12 shape (j1) | `cd /home/user/Erdos-757/experiments/prover/L017/out && timeout 1800 nice -n 10 python3 /home/user/Erdos-757/experiments/prover/L026/j1_check.py <the 7 cells of C7>` | j1_check_output.txt | 37 (j1) hubs: bounds on tau(R) ok; 34 disjoint with tau drop 2 and W avoided; 3 shared with R an (8,5,3) piece |
| C9 Lemma 9 | `cd /home/user/Erdos-757/experiments/prover/L017/out && timeout 3000 nice -n 10 python3 /home/user/Erdos-757/experiments/prover/L026/lemma9_check.py $(cat ../../panel-synthesis/checks/probe_cells.txt) /home/user/Erdos-757/experiments/20261027-0730-kt-cells/out/cells/cell_24_12_8_D3.txt` | lemma9_check_output.txt | 2,920 connected graphs, 327 with DEF > 0, 0 failures |

Inputs are read-only: the refereed tarball extracts in experiments/prover/L017/out/ (L012-L016 lists), the
near-tight inputs of experiments/20261027-0300-transversal-richness, the unrefereed lists
experiments/20261027-0300-tight-cells-d4/lists/*.gz, experiments/prover/L023/cell_25_23_11_D4.txt and
experiments/20261027-0730-kt-cells/out/cells/cell_24_12_8_D3.txt (unrefereed), and the 32 piece edge lists of
experiments/prover/L021/closure_results.json.

## Conclusion
The decisive missing step is unchanged in kind but sharpened: in Case 1* every constraint proved here is met by
the stored (non-counterexample) hubs, which escape only because the hub lies in a member of a positive-deficiency
family. A proof of the KT form needs exactly that statement (or a reduction with gain >= 9 in A); the I11 form
needs the slack-1 case. Computations that would help: N1-N4 of the certificate (pendant-piece table; finite family A2; a Case-1*
falsifier at 25 <= n <= 40; b-configurations in the complete slack-1 cells at n = 27..30).
