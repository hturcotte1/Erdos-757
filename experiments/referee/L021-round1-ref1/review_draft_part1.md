VERDICT: NEEDS-WORK
(Workflow category: ACCEPT WITH FIXES. I found no mathematical error in any theorem presented as proved, and the GAPs are marked honestly. The first line is NEEDS-WORK only because the referee rules allow just three verdict strings and say that any remaining fixable problem means NEEDS-WORK. The required fixes are items 1 to 7 below: one missing case in the proof of Theorem 7(v), which is true by L016 and only needs a line; one unqualified remark; and five editorial items.)

Referee #1, round 1. Certificate: results/proofs/L021-i11-deficiency-route.md (submitted 2026-10-27 07:00 UTC). Work folder: experiments/prover/L021/. My scratch folder: experiments/referee/L021-round1-ref1/.

## Summary

L021 is a partial certificate and says so. It defines the shifted potential A = 27n + 35m - 132 tau and a deficiency DEF over families X of vertex-disjoint induced copies of the 32 graphs of L*, with edge cost 35. It then proves the following:
- Theorem 1: J_eps on C_3 implies J_eps on C, and J_eps on C implies c* >= (6 - eps)/11.
- Theorem 2: KT (132 tau <= 27n + 35m + DEF on C_3) implies J_{1/6}, because DEF <= 11(n - m).
- Theorems 3 to 5: the Henning-Yeo Claims A, B, C, E, F; co-transversality; the free-hub configurations (D1) to (D3); edge-criticality.
- Theorem 6: KT for Delta <= 2, via Tutte-Berge.
- Propositions 8 and 9: Claim H conditionally, and the two (D1) trace exclusions via L016.
- Theorem 7: computations, among them that up to 24 vertices the only "irreducible" graphs are the 32 members of L*.

KT* itself, and hence c* >= 35/66, is explicitly not proved; the open steps are GAPs G1 to G4. I checked every step of Theorems 1 to 6 and of Propositions 8 and 9 line by line, including all of the 27/35/132 bookkeeping, the Hall exchange in 3.4, the case split j = 1, 2, 3, >= 4 in 4.3, the Tutte-Berge computation and the theta table, the K4^s-to-(8,5,3)#0 identification, and the arithmetic 19|X| - 16 - 27 nu and 19|X| - 97. All of it is correct.

I recomputed Theorem 7(i) to (iii) and (v) with my own code. It shares nothing with kt.py, e757 or the judge: tau and DEF are computed by CP-SAT integer programs, induced copies by VF2 monomorphisms of typed incidence graphs, and minimum transversals of the pieces by brute force. The inputs are the cell lists re-extracted from the refereed tarballs and hash-compared. Every number agrees: 43 candidate triples (32 with n <= 24); 12 non-empty cells with 328 graphs, all re-verified to be connected members of C_3 with the stated tau; exactly 32 irreducible graphs, namely the full cells (3,1,1), (8,5,3), (10,7,4), (15,11,6) and (17,13,7); the other 296 have A + DEF = 0 exactly; (L1) holds for all 32; the weights are 16, 5, 13, 2, 10; the role counts are identical to roles_output.txt.

The defects:
- The proof of Theorem 7(v) omits the distribution in which all three hub edges go into one piece. H is then disconnected, and the statement as written covers this case. It is closed at once by L016 or by restricting (v) to connected H, which is the only use. My direct brute force over the small pieces includes this case and finds no counterexample.
- The remark "no saturated graph with n >= 11 is special" silently uses I11 (s >= 0), which is proved only for n <= 27.
- KT* is not explicitly labelled as a NEW conjecture that is not known to follow from I11.
- The judge's sign typo is confirmed: A = 3k - 16, not 16 - 3k.
- The title and the work-folder README overstate "the special family is 32 pieces", which was computed only for n <= 24.
- The status of L017 in DEPENDS is out of date.
- The README calls Theorem 6 "new" without noting the related known results.
