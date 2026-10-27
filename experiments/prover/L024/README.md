# L024: KT reduction (prover work folder)

Certificate: results/proofs/L024-kt-reduction.md (submitted 2026-10-27; unrefereed). Spec: step 4 of
experiments/prover/panel-synthesis/SYNTHESIS.md section 5 (Lemma A of section 3; L021 additions (a), (b) of section 1).
Tags: everything computed here is [verified-here as a computation, unrefereed]; the hand proofs are [derived-here] in the certificate.

## Question
Turn the judge's Lemma A (minimal apex) and L021 additions (a), (b) into complete proofs; decide the finite (D3) family of
pattern (a); state exactly what remains for KT^{L*} (hence c* >= 35/66).

## Answer in one paragraph
Proved by hand: Lemma 1 ((E+) implies the apex hypothesis; the special component of H - v is unique); Lemma 2 (rich-member
lemma: in a minimal counterexample no L*-family X with |E*(X)| = |X| + 1 contains a piece whose vertex pairs are all
co-transversal; proof by Claim E + capacitated Hall + Claim B); Lemma A exactly as stated by the judge (n >= 67), and Lemma A+
(the threshold is 47: below it the only non-hub cases are (beta) n <= 31 and (delta) n <= 46, each covered by 2 or 3 special
pieces plus v); Proposition 3 (two-vertex pendant: |X| <= 2 unless the boundary is a clique of R; one-vertex pendant: |X| <= 3
whenever the boundary is nonempty; empty boundary: |X| in {2,3,4}). Computer-assisted: Theorem 4, pattern (a) (H - v connected
at a degree-3 vertex) never occurs in a minimal counterexample to KT^{L*}: Lemma 2 leaves 12 type triples of non-rich pieces,
and the exhaustive search finds 359 Claim-B configurations, of which the 206 in C_3 are themselves pieces of L* (P = 0) and
none has n >= 24. Remaining: GAP R1 (G2 residue), GAP R2 (cases beta, delta of Lemma A+), GAP R3 (E1-hub lemma, KT form).

## Files and commands (run from this folder; Python 3; exact integers; one process at a time; nice -n 10; each under timeout)
| script | command | output | what it shows |
|---|---|---|---|
| hyp24.py | (library) | - | own exact code: tau, all minimum transversals, C_3 membership (linear, F7 via centres, P3 via per-pair matchings), automorphisms, induced copies, DEF certificates (branch and bound with early stop at a target), family_def (independent value of a family) |
| test_hyp24.py | `timeout 1200 nice -n 10 python3 test_hyp24.py > test_hyp24_output.txt` | test_hyp24_output.txt | 3,000 random 3-graphs: P3, tau, minimum transversals, F7 against brute force; 0 mismatches; all 32 pieces in C_3 |
| pieces_info.py | `timeout 600 nice -n 10 python3 pieces_info.py > pieces_info_output.txt` | pieces_info_output.txt | n, m, tau, W, degree sequences, (L1) for the 32 pieces; Delta <= 2 only for (3,1,1)#0 and (8,5,3)#0 |
| richness.py | `timeout 600 nice -n 10 python3 richness.py > richness_output.txt` | richness_output.txt | all non-co-transversal pairs of every piece; rich pieces: (10,7,4)#0,#3, (17,13,7)#0-5, (15,11,6)#4,5,14-17; (10,7,4)#1,#2: only {0,1},{0,2} |
| pattern_a.py | `timeout 1800 nice -n 10 python3 pattern_a.py 0 > pattern_a_part0_output.txt` | pattern_a_part0_output.txt, pattern_a_results_0.json | pure (D1) case H = F + v: 74 Claim-B configurations, 0 in C_3 |
| pattern_a.py | `nice -n 10 python3 pattern_a.py 1` (stopped: too slow on 17-vertex pieces) | pattern_a_part1_output.txt (partial) | generic search, 13 type triples: per-type counts used to validate pattern_a3.py |
| pattern_a2.py | `nice -n 10 python3 pattern_a2.py poor` (stopped after 6 type triples, superseded) | pattern_a2_poor_output.txt (partial) | same generic search with an explicit type list and Claim-E tags |
| pattern_a3.py | `timeout 1700 nice -n 10 python3 pattern_a3.py small > pattern_a3_small_output.txt` | pattern_a3_small_output.txt, pattern_a3_small_results.json | fast level-based search reproduces the generic counts on 7 type triples (44, 8, 32, 40, 12, 105, 138) |
| pattern_a3.py | `timeout 7000 nice -n 10 python3 pattern_a3.py poor > pattern_a3_poor_output.txt` | pattern_a3_poor_output.txt, pattern_a3_poor_results.json | Theorem 4: the 12 non-rich type triples, 783 g-orbits, 359 Claim-B configurations, 206 in C_3, all tau = sum + 1, all with P = 0 via the single-member family {H} (H is a piece of L*); 0 configurations for n = 24, 31 |
| pattern_a3.py | `timeout 1700 nice -n 10 python3 pattern_a3.py richcheck > pattern_a3_richcheck_output.txt` | pattern_a3_richcheck_results.json (evidence; the text log lost its tail) | Lemma 2 cross-check: 25 type triples with a rich piece and pieces of <= 10 vertices: 20 Claim-B configurations (all (E1,E1,(10,7,4)#0/#3)), none satisfies Claim E, none in C_3 |
| summarize_results.py | `timeout 300 nice -n 10 python3 summarize_results.py > results_summary.txt` | results_summary.txt | totals and per-type counts from the three pattern_a3 result files |
| sanity24.py | `timeout 3000 nice -n 10 python3 sanity24.py > sanity24_output.txt` | sanity24_output.txt | S1: the judge's 186 E1-hubs recomputed with own code: tau(H) = tau(G') + 2, A(H) = A(G') - 16, P(H) = 0 exactly for all; S2: 400 non-b-configuration triples: tau(H) = tau(G') + 1, A(H) = A(G') + 116; S3: 4,693 two-vertex and 1,094 one-vertex pendant additions to 102 stored graphs all in C_3 |

Inputs: experiments/prover/L021/closure_results.json (the 32 pieces), stored refereed cell lists in experiments/prover/L017/out/
(extracted from the L012-L016 tarballs; read-only). L021's kt.py is not imported.

## Search method of pattern_a3.py (complete)
Configuration: three disjoint pieces, g = {g1,g2,g3} (one vertex per piece, piece-degree <= 2, up to the automorphisms of each
piece), three disjoint co-vertex pairs of vertices of degree <= 2 in G = F1+F2+F3+g, no pair inside an edge of G, with Claim B
(no union of minimum transversals of the pieces meets g and the three pairs). WLOG labelling: level 0 takes a largest union U0
of minimum transversals meeting g; some pair avoids U0 (call it P1). Level 1 takes a largest union U1 meeting g and P1; some
other pair avoids U1 (P2). Level 2: P3 must avoid every union meeting g, P1, P2 (computed exactly by grouping the minimum
transversals of each piece by the set of clauses they meet). Every solution is re-verified by brute force over all triples of
minimum transversals (via clause patterns).

## Specifications for further computations (not run)
- W1 (GAP R1, case G2-iii; finite). For k = 2, 3, 4: all assemblies of k non-rich pieces (E1, (8,5,3)#0,#1, (10,7,4)#1,#2, the
  13 non-rich (15,11,6) classes) and k + 1 further edges with all vertices in the pieces, each meeting at least two pieces,
  max degree <= 3, linear, with sum W >= 35k - 96 and n >= 25 (for k = 2 only {(10,7,4)#a, (15,11,6)#b} and two (15,11,6)
  classes), Claim B (no union of minimum transversals meets the k + 1 edges) and Claim E for every subfamily (at least |Y| + 1
  of the k + 1 edges meet V(Y)). Test C_3 membership and compute P = A + DEF (hyp24.def_certificate with target -A); any H with
  P < 0 refutes KT*. Method: the level-based search of pattern_a3.py with clauses = the k + 1 edges (each 3-set must avoid the
  current union U_i). Start with k = 2.
- W2 (GAP R2; finite in principle). Case (beta) of Lemma A+: H = {v} u F_v u F_w with F_v, F_w pieces, |F_w| >= |F_v| >= 8, w a
  vertex of F_v of piece-degree 3 that is not a co-vertex of v, v in F_w, all three edges at v and all components of
  H - v - V(F_v) inside F_w, n <= 31. Case (delta): H covered by v and the pieces F_v, F_w, F_{w'} (w, w' co-vertices of v of
  H-degree 3 on different edges at v), n <= 46. Enumerate the overlap patterns of the two (three) pieces, require (AH)
  (Lemma 1: unique special component at every degree-3 vertex, met by all three edges, Claim B), and compute P.
- W3 (GAP R3). The falsifier experiments/falsify/kt-star-e1hub/ (running when this was written) tests the E1-hub mechanism.

## Note on the logs
Text logs of commands that ran longer than about 100 s in the foreground of the agent's shell lost their final lines
(the processes completed, exit code 0, and wrote their JSON result files at the end). The JSON result files and
results_summary.txt are the evidence of record; pattern_a3_poor_output.txt (background run) is complete. Earlier partial
re-runs of the cross-check (from type 17 and from type 23) agreed with the full run and were deleted.
