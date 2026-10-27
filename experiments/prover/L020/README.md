# experiments/prover/L020: work folder of results/proofs/L020-joint-induction-i11.md

Question: can I11 (11 tau <= 3n + 2m on the class C) be reduced, by a joint induction with Conjecture T''
("connected, Delta <= 3, slack <= 1 implies n <= 26"), to one coverage lemma plus finite computations?
Answer: no. T'' is false at 29 vertices (Theorem 1 of L020); the proved parts and the corrected reduction are in L020.

All programs use exact integer arithmetic (Python 3, networkx for matchings/isomorphism only), one process, `nice -n 10`.
`I` below is experiments/20261027-0300-transversal-richness/inputs (the stored refereed cell lists, one file per cell,
format `n m tau a b c ...`); L017's `hyp.py` (exact transversal routines) is imported from experiments/prover/L017.

| file | what it does | command (from this folder unless stated) | output / what it shows |
|---|---|---|---|
| `roles.py` | non-co-transversal (NC) pairs among vertices of degree <= 2; b-, e-, f-configurations; Hall-type (P3) test `p3_ok_fast`, `in_C` | `python3 roles.py $I/cell_*.txt` (18 lists, see L020 C3) | `roles_output.txt`: e-configurations among slack <= 1 lists only in (8,5,3); in slack-2 lists in (6,3,2), (10,8,4), (13,9,5), (17,14,7), (20,15,8) |
| `roles_b_any.py` | b-configurations with edges allowed | `python3 roles_b_any.py <10 slack <= 1 lists>` | only E_1 (re-check of L017 C5) |
| `patterns.py` | Theorem 3 of L020 on every stored near-tight graph: tau(K-v) = tau(K)-1, isolated vertices, components, pattern of the co-vertex pairs, the pattern conditions, F1 + w(P1,{c,e}) not in C in pattern (f) | `python3 patterns.py $I/cell_10_7_4.txt $I/cell_14_12_6.txt $I/cell_17_13_7.txt $I/cell_8_5_3.txt $I/cell_12_10_5.txt $I/cell_15_11_6.txt $I/cell_22_17_9.txt $I/cell_19_16_8.txt $I/cell_26_22_11.txt` | `patterns_output.txt`: 482 graphs, 4,111 degree-3 vertices, patterns (a) 3223, (b) 145, (e) 183, (f) 506, (i1) 39, (i2) 15, FAILS 0 |
| `pattern_e_build.py` | builds every pattern-(e) gluing F + X + v (F with an e-configuration, X with one), checks C, Delta <= 3, tau | run in a scratch dir: `python3 pattern_e_build.py $I/cell_20_15_8.txt $I/cell_8_5_3.txt` | 120 labelled graphs (29,23,12), slack 1, all in C: `pattern_e_found_cell_20_15_8.json` |
| `classes_K29.py` | isomorphism classes (networkx, incidence graph) | `python3 classes_K29.py pattern_e_found_cell_20_15_8.json K29_classes.json` | 45 classes, `K29_classes.json` |
| `verify_K29.py` | independent verification: linear, F7-free (all 5-edge subsets, all vertex maps), (P3) by Hopcroft-Karp for all vertex pairs, explicit 12-transversal, exhaustive proof that no 11-transversal exists, connectivity, degrees | `python3 verify_K29.py K29_classes.json` | `verify_K29_classes_output.txt`: 45 of 45 OK, degrees 2^18 3^11 |
| `triples_K29.py` | all triples of disjoint pairs (not inside an edge) of each class: coverage by a minimum transversal (bit-parallel); `in_C` and tau for uncovered ones | `python3 triples_K29.py K29_classes.json 0 1; python3 triples_K29.py K29_classes.json 1 45` | `triples_K29_output.txt`: 6 uncovered triples per class, none with K+v in C; TOTAL violators 0 |
| (inline) | roles of the 45 classes | `python3 -c "...analyse(...)..."` as in L020 C3 | no NC pair at all, no b-/e-/f-configuration |
| `role_e_counts.py` | e-configurations per class | `python3 role_e_counts.py $I/cell_8_5_3.txt $I/cell_6_3_2.txt $I/cell_10_8_4.txt $I/cell_13_9_5.txt $I/cell_17_14_7.txt $I/cell_20_15_8.txt` | histograms in L020 C8 |
| `iterate_e.py` | glue the 120 graphs again with (8,5,3) | `python3 iterate_e.py pattern_e_found_cell_20_15_8.json $I/cell_8_5_3.txt iter1_K29_plus_853.json` | 0 (no e-configuration in the 29-vertex graphs) |
| `glue_e.py` | general pattern-(e) gluing A (+) B with iso classes and e-configurations of the results | `python3 glue_e.py $I/cell_10_8_4.txt $I/cell_10_8_4.txt glue_1084x1084.json same` | 465 classes (21,19,9), slack 2, none with an e-configuration |
| `check_nc_pairs.py` | Proposition 6 of L020 on all NC pairs of the stored near-tight graphs | `python3 check_nc_pairs.py $I/cell_3_1_1.txt ... $I/cell_26_22_11.txt` (10 lists) | 204 NC pairs, 0 violations |
| `check_7nu.py` | Lemma 2.1 of L020 (7 nu >= 2 |E| for subcubic graphs) | `for N in 1..10: geng -q -D3 N \| python3 check_7nu.py` (geng: experiments/referee/L013-round2/out/nauty_build/geng) | 5,389 graphs, 0 failures, equality only for subdivided K4's (+ isolated vertices) |
| `build_bf.py` | patterns (b) and (f) in reverse: b-configurations glued to E_1, f-configurations glued to E_1 or a (10,7,4) class with an NC pair | `python3 build_bf.py <slack-3 list> <out.json> [sample seed]` | (21,14,8,3): nothing; (18,13,7,3): 109 near-tight graphs in (22,17,9), (29,23,12); (22,18,9,3) sample 4000: one (26,22,11); (25,19,10,3) sample 3000: 4 graphs in (29,23,12). Outputs `bf_*_output.txt`, `bf_*.json` |
| (inline, see L020 C8) | iso test of the new (29,23,12) graphs against `K29_classes.json` | python snippet | `K29_new_from_18_13_7.json`, `K29_new_from_25_19_10.json`: both empty (no new classes) |
| `check_in_lists.py` | every built near-tight graph with <= 26 vertices must be isomorphic to a class of the stored complete list | `python3 check_in_lists.py bf_632_x_slack1.json` (also with `bf_18_13_7.json bf_22_18_9_sample.json`) | 0 outside the lists; the triangle gluings hit 19/19, 227/227, 37/37, 36/36 classes of (15,11,6), (19,16,8), (22,17,9), (26,22,11): Observation 7 (triangle chains) |
| `bf_632_x_slack1_output.txt` | triangle (6,3,2) glued by pattern (f) to slack-1 graphs with an NC pair | `python3 build_bf.py $I/cell_6_3_2.txt bf_632_x_slack1.json 0 1 $I/cell_8_5_3.txt $I/cell_12_10_5.txt $I/cell_15_11_6.txt $I/cell_19_16_8.txt $I/cell_22_17_9.txt` | 2,368 near-tight graphs; the 564 with 29 vertices are among the 45 classes |
| `pattern_e_24_20_10_output.txt` | pattern-(e) gluing of the slack-2 cell (24,20,10,3) (2,781 classes; experiments/20261027-0340-induction-n28-n29-f25/out/cells, unrefereed list) with (8,5,3) | `cd run24; python3 ../pattern_e_build.py <that list> $I/cell_8_5_3.txt` | no class of (24,20,10,3) has an e-configuration: nothing built |

Conclusion: Conjecture T'' is false (45 classes of connected Delta = 3 members of C with (n,m,tau) = (29,23,12), slack 1);
they satisfy I11, have no non-co-transversal pair, and admit no violating extension K + v. See L020 for the proofs of the
degree-3 lemma for near-tight graphs (Theorem 3), the Delta <= 2 bound (Theorem 2), the corrected reduction (Theorem 4,
Corollary 5: I11 follows from cell(25,23,11,3) = empty, C1-big and R-big) and Proposition 6.
