VERDICT: NEEDS-WORK
(Workflow category: ACCEPT WITH FIXES. I found no mathematical error in any theorem presented as proved, and the GAPs are marked honestly. The first line is NEEDS-WORK only because the referee rules allow just three verdict strings and say that any remaining fixable problem means NEEDS-WORK. The required fixes are items 1 to 7 below: one missing case in the proof of Theorem 7(v), which is true by L016 and only needs a line; one unqualified remark; and five editorial items.)

Referee #1, round 1. Certificate: results/proofs/L021-i11-deficiency-route.md (submitted 2026-10-27 07:00 UTC). Work folder: experiments/prover/L021/. My scratch folder: experiments/referee/L021-round1-ref1/.

## Summary

L021 is a partial certificate and says so. It sets up the shifted potential A = 27n + 35m - 132 tau and a deficiency DEF, a maximum over families of vertex-disjoint induced copies of the 32 graphs of L*, with edge cost 35. It proves that the inequality KT (132 tau <= 27n + 35m + DEF on C_3) would give J_{1/6} on C and hence c* >= 35/66 (Theorems 1, 2). It derives the structure of a minimal counterexample to KT (Theorems 3 to 5, Propositions 8 and 9), proves KT for Delta <= 2 (Theorem 6), and verifies KT by computation up to 24 vertices (Theorem 7). KT* itself is left open as G1 to G4.

I checked every step of Theorems 1 to 6 and of Propositions 8 and 9 line by line. This includes all of the 27/35/132 bookkeeping, the Hall exchange in 3.4, the case split j = 1, 2, 3, >= 4 in 4.3, the Tutte-Berge computation, the theta table, the K4^s-to-(8,5,3)#0 identification, and the bounds 19|X| - 16 - 27 nu and 19|X| - 97. All of it is correct.

I recomputed Theorem 7(i) to (iii) and (v) with my own code, which shares nothing with kt.py, e757 or the judge:
- tau and DEF by CP-SAT integer programs;
- induced copies by VF2 monomorphisms of typed incidence graphs;
- minimum transversals by brute force;
- a direct brute force of the pure hub assemblies over all 528 pairs of pieces;
- inputs: the cell lists re-extracted from the refereed tarballs and hash-compared.

Every number agrees:
- 43 candidate triples (32 with n <= 24);
- 12 non-empty cells with 328 graphs, all re-verified;
- exactly 32 irreducible graphs, namely the full cells (3,1,1), (8,5,3), (10,7,4), (15,11,6) and (17,13,7);
- the other 296 graphs have A + DEF = 0 exactly;
- (L1) holds for all 32 pieces, and the weights are 16, 5, 13, 2, 10;
- the role tables are identical.

The prover's own scripts reproduce their outputs exactly. KT survives every induced subgraph of A_base, of the three 12-point sets and of the other record sets, as well as Fibonacci sets and hypertrees.

The defects, in order (details under Problems):
1. The proof of Theorem 7(v) omits the case in which all three hub edges go into one piece, giving a disconnected H. The statement is still true: L016 rules the case out, and so does the brute force.
2. The side remark "no saturated graph with n >= 11 is special" silently uses I11, which is proved only for n <= 27.
3. KT* is not stated to be a new conjecture that is not known to follow from I11.
4. The panel judge's sign typo is confirmed: A = 3k - 16, not 16 - 3k.
5. "The special family is 32 pieces" (title, README) is established only for n <= 24.
6. DEPENDS is out of date: L017 is now accepted, and the use of L016 in Proposition 9 is not listed.
7. The README calls Theorem 6 "new" without citing the related known results.
