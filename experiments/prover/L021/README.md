# L021: the Henning–Yeo deficiency route (prover work folder)

Certificate: results/proofs/L021-i11-deficiency-route.md (submitted 2026-10-27; under referee (round 2: fable ACCEPT, opus editorial items applied); partial proof with GAPs G1–G4).
Tags below follow that file: [derived-here] proofs there, [verified-here as computation, unrefereed] the outputs here.

## Question
Can the Henning–Yeo deficiency method (arXiv:1802.01825, Section 7, Theorem 21) be set up for I11-type bounds on the
class C, with special pieces taken from the known low-slack graphs, and how far does the minimal-counterexample argument go?

## Answer in one paragraph
The literal version (coefficients 3n + 2m, tight pieces as special pieces) is vacuous: tight pieces have weight 0. The working
analogue shifts weight from vertices to edges so that deleting a degree-3 vertex whose removal lowers tau is exactly neutral
(27 + 3*35 = 132, as 6 + 3*13 = 45 in Henning–Yeo), and gives up epsilon = 1/6 on the vertex coefficient:
**KT: 132 tau <= 27 n + 35 m + DEF(H)** on C_3 (members of C with max degree <= 3), DEF = max over families of disjoint induced
special pieces of (sum of weights - 35 |E*|). KT implies 11 tau <= (3 + 1/6) n + 2 m on C, hence c* >= 35/66 > 9/17 (goal B),
because any epsilon < 3/17 suffices. The special family, computed exactly from the stored refereed lists, is 32 pieces among the connected members of C_3 with at most 24 vertices (at most 27 by the unrefereed run experiments/20261027-0730-kt-cells, see its README)
(E_1; (8,5,3) x2; (10,7,4) x4; (15,11,6) x19; (17,13,7) x6), and KT holds on all of C_3 up to 24 vertices; all other
special-candidate graphs are equality cases. Proved: Henning–Yeo Claims A–F, vertex co-transversality, the free-hub local
structure (D1)–(D3) at degree-3 vertices, edge-criticality, KT for max degree <= 2 (via Tutte–Berge; closely related to Henning–Yeo EJC 24(2) (2017) P2.50 Prop. 9, tau = N - nu(G), plus Chvatal–Hanson-type matching bounds for subcubic graphs, so not claimed as new; novelty left to the scout), Claim H under a
replacement hypothesis, and two small-subgraph exclusions. Not proved: the impure (D1)–(D3) configurations (G1), Claim H in
the cases where the replacement graph leaves C_3 (G2), degree-2 vertices (G3), and finiteness of the special family (G4).

## Files and commands (run from this folder; Python 3; exact integers; one process; nice -n 10; each under timeout)
| script | command | output | what it shows |
|---|---|---|---|
| kt.py | (library) | – | A(H) = 27n + 35m - 132 tau; induced-copy matcher; exact DEF by branch and bound |
| scan_cells.py | `timeout 120 nice -n 10 python3 scan_cells.py > scan_cells_output.txt` | scan_cells_output.txt, special_cells.json | the 43 triples (n,m,tau), n <= 27, that a connected member of C_3 with A < 0 can have (I11 by L016, K8, P3, connectivity), and the stored list for each; complete for n <= 24 |
| closure.py | `timeout 1500 nice -n 10 python3 closure.py > closure_output.txt` | closure_output.txt, closure_results.json | irreducible special graphs = the 32 pieces; the other 296 graphs with A < 0 (n <= 24) have A + DEF = 0 exactly |
| validate_def.py | `timeout 900 nice -n 10 python3 validate_def.py` | validate_def_output.txt | brute-force recomputation of DEF on 173 graphs: 0 mismatches |
| l1_check.py | `timeout 300 nice -n 10 python3 l1_check.py` | l1_check_output.txt | (L1) every vertex of every piece lies in a minimum transversal (32/32); max weight 16 < 35 |
| delta2_test.py | `timeout 2400 nice -n 10 python3 delta2_test.py 12` | delta2_test12_output.txt (and delta2_test_output.txt for N <= 10) | KT on all 27,525 connected linear 3-graphs with max degree <= 2 and <= 12 edges: 0 failures (Theorem 6 proves it in general) |
| attach.py | `timeout 1500 nice -n 10 python3 attach.py` | attach_output.txt (partial: 10 of 32 pieces before the timeout; the script is slow because of a redundant loop in in_C, results are exact) | numbers of admissible and of uncoverable 2- and 3-attachments of a hub to one piece (data for GAP G1) |
| roles.py | `timeout 600 nice -n 10 python3 roles.py` | roles_output.txt | independent recomputation of L017 C5's role counts for the 32 pieces: role_b > 0 only E_1, role_e > 0 only the two (8,5,3), role_c = role_f1 = 0 (Theorem 7(v)) |
| sanity.py | `timeout 600 nice -n 10 python3 sanity.py` | sanity_output.txt | F7 and the (9,8,4) violator (outside C) violate KT; hypertrees with a perfect matching are equality cases |
| random_assemblies.py | `timeout 900 nice -n 10 python3 random_assemblies.py 2 600 45` | random_assemblies_output.txt | mini-falsifier: 782 random assemblies of 2-4 pieces joined by random edges and degree-2/3 hubs (at most 45 vertices), 361 connected and in C_3, NONE with A < 0, so KT holds trivially on them and the test is uninformative: random assemblies do not reach the special region (a first run with up to 6 pieces, seed 1, was killed by its timeout inside a DEF computation and printed nothing) |

Inputs: the refereed cell lists, extracted read-only in experiments/prover/L017/out/ (from experiments/prover/L012/cells.tar.gz,
L013/cells.tar.gz, L014/cells.tar.gz, L016/cells_new.tar.gz); L017's role tables experiments/prover/L017/tight_configs_output.txt and
tight_configs_slack1_output.txt (used in Theorem 7(v)); nauty geng at experiments/referee/L013-round2/bin/geng.

## Results (numbers)
- Weights (times 12): E_1 16, (10,7,4) 13, (17,13,7) 10, (8,5,3) 5, (15,11,6) 2; edge cost 35.
- Cells with A < 0 and n <= 24, non-empty: (3,1,1) 1, (8,5,3) 2, (9,4,3) 1, (10,7,4) 4, (14,8,5) 9, (15,7,5) 2, (15,11,6) 19,
  (16,10,6) 16, (17,13,7) 6, (21,10,7) 5, (22,13,8) 85, (23,16,9) 178 (328 graphs); irreducible: exactly the 32 pieces.
- Not covered by stored lists: (25,14,9) (only a D2 list), (26,13,9), (26,17,10), (27,13,9), (27,15,10), (27,16,10), (27,20,11).
- Attachment data (k = 2 / k = 3 uncoverable among admissible): E_1 3/3, 1/1; (8,5,3)#0 7/149, 257/423; #1 8/108, 175/236;
  (10,7,4)#0 0/309, 198/1155; #1 2/219, 122/658; #2 2/221, 143/666; #3 0/306, 173/1140; (15,11,6)#0 2/1008, 178/8732;
  #1 2/1042, 196/9121; #2 2/1042, 188/9124.

## Elementary reductions tried for the impure configurations (GAP G1), and why they fail
Notation: (D1) at a degree-3 vertex v: a piece F is a component of H - v met by k >= 2 edges at v; G' = H - v - V(F).
1. Z = V(F) + v, T = (minimum transversal of F) + v: A(H) >= A(G') - W(F); with DEF(H) = 0 this gives P(H) >= P(G') - DEF(G') - W(F),
   short by W(F) + DEF(G') (the free hub is exactly balanced, so every inexact step loses).
2. Same Z with the families: DEF(H) >= DEF(G') + W(F) - 35 k'; useless, as the k' <= 3 edges at v cost 105.
3. For k = 2 with a single-vertex trace on e_2 = {v, c, o}: replace the uncovered e_2 by a pendant edge {v, o, z} (z new) in R = H - V(F):
   R' is in C_3, and P(H) >= 8 - W(F) - DEF(R'); with DEF(R') <= 16 (as in Proposition 8) this fails for every piece.
4. Small induced subgraphs: B = H[V(F) + v + outside co-vertices] has tau(B) = tau(F) + 1 by Claim B, and I11 for B (L016, n(B) <= 20)
   excludes the trace types (2,2) and, over tight pieces, (2,1) when k = 2 (Proposition 9); for k = 3 the slack of B is
   s(F) + 3(4 - q) - 5 with q = number of 2-vertex traces, negative only for q = 3, the pure case.
5. The Henning–Yeo replacement (Proposition 8) works whenever the new edge on the boundary keeps the graph in C_3; it fails when
   the boundary contains a pair lying in an edge of H - V(X), or creates an F7 or a P3-tight set.

## Computations needed (to continue this route)
1. The finite check for GAP G2 with empty boundary: assemblies H = H[V(X)] of at most five pieces of L* joined by |X| + 1 edges,
   n >= 25 (at most 85 vertices): test KT (equivalently, that none is a minimal counterexample).
2. Cells with A < 0 at n = 25, 26, 27 not yet stored: cell(25,14,9,3), cell(26,13,9,3), cell(26,17,10,3), cell(27,13,9,3),
   cell(27,15,10,3), cell(27,16,10,3), cell(27,20,11,3) (the last reported empty by experiments/20261027-0300-tight-cells-d4,
   unrefereed); with them, Theorem 7(ii) extends to n <= 27 (or a new irreducible piece appears).
3. A falsifier run on KT for n = 25..40 with the generators of experiments/falsify/i11-n28-40 (connected, max degree 3, A < 0),
   computing DEF with kt.deficiency; random_assemblies.py is a first, small version.
4. For GAP G1 with k = 3: for every piece F and every uncoverable 3-attachment (C6 data), the list of minimal "outside completions"
   (which co-vertices are outside F); then targeted reductions per type, as in Henning–Yeo's Claims H.4–H.5.
5. A cheaper attach.py (drop the redundant loop) to finish the attachment data for the 22 remaining pieces.
