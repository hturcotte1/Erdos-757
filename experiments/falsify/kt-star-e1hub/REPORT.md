FALSIFIER: HOLDS-ON-DATA
KT* HOLDS (on all data tested; no irreducible special piece outside L* found)
KT^{L*} HOLDS (on all data tested; minimum P = A + DEF = 0 over every evaluated hub)

# E1-hub falsifier for KT* / KT^{L*} (L021)

Tags: [verified-here as computations, unrefereed]. NONE of this is a proof; HOLDS-ON-DATA is evidence only.
Folder: /home/user/Erdos-757/experiments/falsify/kt-star-e1hub/ . Machine-readable summary: results.json, hubs_global.json, cell_table.md.

## 1. Statement tested
For connected G' in C_3 (Delta <= 3) with A(G') = 27n+35m-132tau <= 15 (any slack) and a b-configuration {a,b,c} of G' (G'-degrees <= 2, no minimum
transversal of G' contains two of a,b,c), let H = G' + E1-hub (new v,x,y,z; edges xyz, vxa, vyb, vzc). Whenever H lies in C_3 (checked: linear, F7-free,
e(S)<=|S|-2 via the Hall pair test, L014 verifier pyverify.py) we asserted tau(H) = tau(G')+2 (kt.tau_masks and CP-SAT agree), so A(H) = A(G')-16 < 0, and computed
DEF(H) over the 32 pieces of L* (kt.deficiency) and P = A+DEF, and DEF^proper. Counterexample to KT^{L*}: P < 0. Counterexample to KT*: H not isomorphic
to a member of L* with A + DEF^proper < 0 (new irreducible special piece). None found.

## 2. Scope and counts
### 2.1 Main pass (stored connected classes)
Inputs: all stored lists of experiments/prover/L017/out/L012..L016, 20261027-0340-induction-n28-n29-f25 (out/cells, cells_chk, cells_ref, lists), 20261027-0300-transversal-richness/inputs;
for each cell (n,m,tau) with A<=15 the list with the most Delta<=3 classes was used (inventory.py / inventory.txt / inventory.json; 82 cells with A<=15, 55 of them with zero connected Delta<=3 classes,
27 non-empty; sources agree where several exist). The cells promised by experiments/20261027-0730-kt-cells did not exist when run (the folder was absent), and the stored (25,14,9), (26,13,9),
(26,17,10), (27,*), (28,*), (29,*) lists are empty or D2-only, so those cells are NOT covered (see section 5).
Totals: 9,773 classes scanned; 1,837 labelled b-configurations; 1,273 distinct hub isomorphism classes in C_3 (hubs_global.json); every one has P = 0; no hit.
Per cell: cell_table.md (copied below). Hub cells reached: (10,7,4) 2, (15,11,6) 9, (16,10,6) 5, (17,13,7) 3, (22,13,8) 21, (23,16,9) 90, **(28,16,10) 98, (29,19,11) 1,045**;
all with P = 0 exactly (KT equality); the ones in L* are (10,7,4), (15,11,6), (17,13,7) (14 classes); the others (16,10,6), (22,13,8), (23,16,9), (28,16,10), (29,19,11) are not in L* and have
A + DEF^proper = 0 as well (DEF^proper = DEF for n > 17).
**Correction to SYNTHESIS.md section 3:** the claim "the E1-hub mechanism never reaches n(H) >= 25 on stored data" is false: the probe's cell list omitted the cells (24,12,8) (129 classes, 125 labelled
b-configurations, 98 hub classes, n(H) = 28) and (25,15,9) (6,849 classes, 1,526 b-configurations, 554 classes carrying one, 1,045 hub classes, n(H) = 29). These are the sparse family (6k,3k,2k) (A = 3k) -> hubs
(6k+4,3k+4,2k+2) (A = 3k-16, P = 0). All hubs at n(H) >= 25 are equality cases, none fails. Not a counterexample, but it shows the mechanism is live at n >= 25 and that equality persists.
The (25,15,9) run was done in 12 resumable parts (run_parts.sh, main_25_15_9.part*.jsonl) because background jobs were killed twice and the disk filled; two earlier complete runs printed identical summary numbers
(main_25_15_9.run1.log).
Variant EDGEOK=1 (triples that are edges of G' allowed; edgeok_others.jsonl, all cells except (25,15,9)): thousands of extra labelled triples, identical sets of hubs in C_3 (an edge triple never gives a member of C): the 'not an edge' clause is automatic.

### 2.2 Disjoint-union pass
b-configurations on G' = G1 u G2 (u G3) with a,b,c in no minimum transversal of their own components. A cross-component pair is co-transversal iff both vertices lie in some minimum transversal. scan_notin*.py:
among all stored connected Delta<=3 classes with A <= 31 and n <= 27 (65 cells, 10,980 classes, scan_notin_A31.json) only the (7,3,2) path (A = 30) has a vertex of degree <= 2 lying in no minimum transversal; (14,9,5) etc. have them too but A >= 33.
Since components have A >= -16 (E_1), a connected hub over a union with sum A <= 15 needs (k=2) one non-inT vertex plus a non-co pair in the other component (only E_1, A=-16), i.e. (7,3,2) u E_1 (and u 2 E_1); k=3 would need two non-inT components (A >= 60-16 > 15), impossible.
union_small.py / union_small.log: all 17+20 b-configurations: the disconnected hubs have P = 14, and the connected ones ((0,7,8): a in the path, b,c in E_1) give n=14 and n=17 with A = -2 / -18, DEF = 2 / 18, **P = 0** (equality). No hit.
Caveat: only stored classes were considered; unstored sparse classes with a non-inT vertex and A <= 31 are not excluded.

### 2.3 Iteration
iterate.py: the hub construction applied again to every distinct hub graph from the main pass, the F-hub pass and the generator pass (1,827 distinct inputs, n up to 33): **0 b-configurations**, so level 2 is empty (iter2c.jsonl.stats.json; earlier subsets iter2*.stats.json).

### 2.4 Extension: F-hubs
fhub.py replaces E_1 by each of the 32 pieces F of L* (edges {v,q_i,g_i}, q_i low-degree vertices of F, g_i of G'; the tau-condition is derived in the script header and every kept H is re-asserted tau(H) = tau(G')+tau(F)+1).
G' from the 7 cells that have b-configurations; 18,594 attachments, 2,000 new iso classes, 228 in C_3, n(H) up to 42: min P = 0, no hit (fhub.jsonl.stats.json).

### 2.5 Second pass (generators)
* unions_vext.py (new, structured): parents = disjoint unions of <=3 components from a pool of 380 (the 32 L* pieces and all stored classes with n<=14, 0<=A<=30) with sum A <= 0 and n>=24; children = EVERY one-vertex extension raising tau by 1 (exact `vext` operator of experiments/falsify/i11-n28-40, d = 1..3 edges, children in C); A(child) = A(parent)+35d-105.
  All 72,423 parents (uv_full.stats.json): 25,154 children, 1,068 connected with A < 0 (all in cell (30,22,12), n = 30), each evaluated exactly (in C, tau, DEF): **min P = 0, no hit**. (A random half, 30,000 parents, uv_a: 554 classes, same.) Level 2 (extensions of those children): no children. Note: the full run's per-class jsonl lost most lines (disk full, ENOSPC); the counts are from the stats file; uv_a.jsonl has all 554.
* sa/a11.c (the i11 annealer with objective A): did not reach tau = 10 at (n,m) = (28,16) in 1e6-step runs (best A = 128); no data, abandoned.
* beamA.py (A-driven beam on vext): died immediately (vext extensions from L* seeds are rare); 0 reported. The beam/growth generators of i11-n28-40 were NOT rerun with objective A+DEF; their output is slack-driven (saturated graphs, A > 0).
So the generator pass is thin: no unbiased search of sparse A<0 graphs at 25 <= n <= 40 was achieved.

## 3. Acceptance (independent re-verification)
* verify.py (independent code: pyverify tau by branching, networkx induced-copy search + unbounded family enumeration for DEF): 17 sampled hubs (n = 22..30; main, F-hub, generator) all reproduce n, m, tau, A, DEF (verify_sample.log).
* f7_brute_check.log: 100 kept hubs F7-free by exhaustive 5-edge search (the brute test detects F7 itself).
* Every kept H passes tau(kt) == tau(CP-SAT) and tau == tau(G')+2 (assertions in hubs.analyse_H; the scripts would have aborted).
No hit existed, so there was no hit to re-verify.

## 4. Commands (all from the folder; nice -n 10; timeouts)
inventory.py > inventory.txt; run_main.py main_others.jsonl <cells> ; PART=i/12 run_main.py main_25_15_9.part$i.jsonl 25,15,9 (run_parts.sh, drive.sh); EDGEOK=1 run_main.py edgeok_others.jsonl <cells>;
iterate.py iter2c.jsonl main_others.jsonl main_25_15_9.part*.jsonl fhub.jsonl uv_a.jsonl; fhub.py fhub.jsonl 6,3,2 11,7,4 12,6,4 13,9,5 18,9,6 19,12,7 24,12,8; scan_notin.py 20; scan_notin2.py 27 31 scan_notin_A31.json;
union_small.py; unions_vext.py {a 40 0 25 30000, full 40 0 25 1000000}; verify.py N seed files; aggregate_H.py; make_report.py.

## 5. Limits (read before relying on this)
* NONE-FOUND-type evidence. Data: connected stored classes with A <= 15; the stored lists exclude most sparse A <= 15 graphs (hypertrees with perfect matching reach A <= 15 up to n = 63; only (9,4,3), (15,7,5), (21,10,7) are stored), and cells (25,14,9) [A=-23], (26,13,9), (26,17,10), (27,13..20,*) were empty or missing.
* n(H) <= 29 for the main pass; n(H) <= 42 only for F-hubs; the n=25..66 range left open by Lemma A is not exhausted: b-configurations require NC pairs, which stored data show only in the (6k,3k,2k) family up to k=5; (30,15,10) (A = 15, would give n(H) = 34) is not stored.
* The first-order mechanism (A(H) = A(G') - 16) means a counterexample needs DEF(H) < 16 - A(G'); in every case found DEF jumps by exactly the amount needed (knife-edge). A larger-k member of the (6k,3k,2k) family, or an A<=15 sparse G' with b-configuration not in the stored lists, is the natural next target (a (30,15,10) cell list, 15 edges on 30 vertices, would be enumerable).
* KT* is knife-edge: all hub outcomes are equalities.

## 6. Cell table (main pass)
| cell (n,m,tau) | A | list D | classes scanned | b-configs (labelled) | classes with b-config | hubs in C_3 (iso classes) | hub cells | min P |
|---|---|---|---|---|---|---|---|---|
| (3, 1, 1) | -16 | 3 | 1 | 0 | 0 | 0 | {} | None |
| (6, 3, 2) | 3 | 3 | 1 | 4 | 1 | 2 | {'(10,7,4)': 2} | 0 |
| (8, 5, 3) | -5 | 4 | 2 | 0 | 0 | 0 | {} | None |
| (9, 4, 3) | -13 | 3 | 1 | 0 | 0 | 0 | {} | None |
| (10, 7, 4) | -13 | 4 | 4 | 0 | 0 | 0 | {} | None |
| (11, 7, 4) | 14 | 3 | 35 | 10 | 10 | 9 | {'(15,11,6)': 9} | 0 |
| (12, 6, 4) | 6 | 3 | 4 | 7 | 2 | 5 | {'(16,10,6)': 5} | 0 |
| (12, 10, 5) | 14 | 4 | 149 | 0 | 0 | 0 | {} | None |
| (13, 9, 5) | 6 | 3 | 84 | 3 | 3 | 3 | {'(17,13,7)': 3} | 0 |
| (14, 8, 5) | -2 | 3 | 9 | 0 | 0 | 0 | {} | None |
| (14, 12, 6) | 6 | 3 | 2 | 0 | 0 | 0 | {} | None |
| (15, 7, 5) | -10 | 3 | 2 | 0 | 0 | 0 | {} | None |
| (15, 11, 6) | -2 | 4 | 19 | 0 | 0 | 0 | {} | None |
| (16, 10, 6) | -10 | 3 | 16 | 0 | 0 | 0 | {} | None |
| (17, 13, 7) | -10 | 3 | 6 | 0 | 0 | 0 | {} | None |
| (18, 9, 6) | 9 | 3 | 22 | 27 | 9 | 21 | {'(22,13,8)': 21} | 0 |
| (19, 12, 7) | 9 | 3 | 833 | 135 | 55 | 90 | {'(23,16,9)': 90} | 0 |
| (20, 11, 7) | 1 | 3 | 45 | 0 | 0 | 0 | {} | None |
| (20, 15, 8) | 9 | 3 | 953 | 0 | 0 | 0 | {} | None |
| (21, 10, 7) | -7 | 3 | 5 | 0 | 0 | 0 | {} | None |
| (21, 14, 8) | 1 | 3 | 299 | 0 | 0 | 0 | {} | None |
| (22, 13, 8) | -7 | 3 | 85 | 0 | 0 | 0 | {} | None |
| (22, 17, 9) | 1 | 4 | 37 | 0 | 0 | 0 | {} | None |
| (23, 16, 9) | -7 | 3 | 178 | 0 | 0 | 0 | {} | None |
| (24, 12, 8) | 12 | 3 | 129 | 125 | 42 | 98 | {'(28,16,10)': 98} | 0 |
| (25, 15, 9) | 12 | 3 | 6849 | 1526 | 554 | 1172 | {'(29,19,11)': 1172} | 0 |
| (26, 14, 9) | 4 | 2 | 3 | 0 | 0 | 0 | {} | None |

Cells in the stored lists with A<=15 and zero classes (empty or no connected Delta<=3 member): (11, 6, 4), (13, 8, 5), (14, 7, 5), (16, 9, 6), (17, 8, 6), (17, 9, 6), (18, 12, 7), (19, 10, 7), (19, 11, 7), (20, 10, 7), (20, 14, 8), (21, 13, 8), (21, 18, 9), (22, 11, 8), (22, 12, 8), (23, 11, 8), (23, 12, 8), (23, 13, 9), (23, 14, 9), (23, 15, 9), (23, 20, 10), (24, 12, 9), (24, 13, 9), (24, 14, 9), (24, 15, 9), (24, 18, 10), (24, 19, 10), (25, 12, 9), (25, 13, 9), (25, 14, 9), (25, 16, 10), (25, 17, 10), (25, 18, 10), (25, 22, 11), (26, 13, 9), (26, 14, 10), (26, 15, 10), (26, 16, 10), (26, 17, 10), (26, 21, 11), (27, 13, 10), (27, 14, 10), (27, 15, 10), (27, 16, 10), (27, 18, 11), (27, 19, 11), (27, 20, 11), (28, 14, 10), (28, 17, 11), (28, 18, 11), (28, 19, 11), (28, 23, 12), (29, 15, 11), (29, 16, 11), (29, 22, 12)
