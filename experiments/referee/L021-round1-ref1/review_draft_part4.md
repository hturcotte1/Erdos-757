
## Problems found, in order of severity

1. **Theorem 7(v): the proof omits a case. The statement is true. Minor gap, one-line fix.**
   - As stated, (v) covers every H in C_3 with a degree-3 vertex v such that H - v is the disjoint union F_1 + F_2 of two members of L* and tau(H) = tau(H - v) + 1. Connectivity of H is not assumed.
   - 7.6 asserts that the distribution of the three pairs is one of (b), (c1), (c2), (e), (f). That list (L017 7.3) excludes the distributions {1,1,1} and {2,2,2}, in which all three pairs lie in one piece. L017 can exclude them because there H is connected, by L017 Theorem 4(ii).
   - The distribution {1,1,1} gives a disconnected H = (F_1 + v) + F_2. It is not isomorphic to a member of L*, so 7.6 does not cover it as written.
   - The case is empty. F_1 + v = H[V(F_1) u {v}] lies in C, has tau(F_1) + 1 and slack s(F_1) - 2 < 0, and has at most 18 vertices, which contradicts L016.
   - My brute force enumerates this distribution explicitly (check2 and check2b, and check2c over all 528 pairs, R3c). Every τ-raising configuration of this kind lies outside C_3. For example, (8,5,3) with all three pairs gives the (9,8,4) graphs, which violate (P3), and (15,11,6) gives (16,14,7) graphs outside C.
   - Fix: add "connected" to (v). The only application, case (D2) in a minimal counterexample, has H connected. Alternatively, dispose of {1,1,1} by L016 in one sentence.

2. **An unqualified statement relies on I11 beyond its proved range.** The Note after "The list L*" says: "no saturated graph (m = n-2) with n >= 11 is special, since then A = 12s + 2n - 22 >= 0".
   - The inequality needs s >= 0, which is I11. I11 is proved on C only for n <= 27 (L016).
   - For n >= 28, Henning-Yeo gives only s >= -(3n + 2)/17, and then A could be negative.
   - The remark is not used in any proof, but as written it is unproved for n >= 28.
   - Fix: append "(for n <= 27 by L016; in general under I11)". Remark 2.4 already words its analogue correctly ("with s >= 0").

3. **KT* is not labelled as a new conjecture independent of I11.**
   - The certificate tags KT* [conjecture], but nowhere says that it is introduced here and is not known to follow from I11. It is also not known to imply I11: it implies only J_{1/6}.
   - I11 gives A = 12s - 9n + 11m >= 0 only when 11m >= 9n. In the sparse region KT needs DEF to compensate. The candidate cells (21,10,7) (s = 6, A = -7) and (27,13,9) (s = 8, A = -4) show that I11-satisfying graphs with A < 0 exist or are allowed.
   - The only evidence for KT* is Theorem 7 (n <= 24). The random assemblies never reached A < 0.
   - Fix: one sentence after Conjecture KT* and in the CLAIM-TYPE line.

4. **Sign typo (Sanity checks, hypertrees with a perfect matching).** The text has "A = 16 - 3k"; the correct value is A = 3k - 16.
   - The prover's own sanity_output.txt shows A = -13, -10, -7, -4, -1 for k = 1..5.
   - My check4 confirms A = 3k - 16 and DEF = 16 - 3k on random hypertrees with a perfect matching for k = 0..5, so P = 0. For k = 6: A = 2, DEF = 0.
   - As printed, the line is internally inconsistent: A + DEF would be 32 - 6k, not 0.

5. **"The special family is 32 pieces" is overstated.**
   - The title says "the computed special family (32 pieces)", and experiments/prover/L021/README.md line 16 says "The special family, computed exactly from the stored refereed lists, is 32 pieces".
   - Both must say "among connected members of C_3 with at most 24 vertices". The candidate cells (25,14,9) (only a D2 list), (26,13,9), (26,17,10) and the four n = 27 cells are not computed.
   - Theorem 7(i) and GAP G4 are correctly qualified.

6. **DEPENDS block: one status out of date and one use of L016 missing.**
   - DEPENDS describes L017 as "[round 1: two referees, no mathematical error; round 2 pending]". L017 is ACCEPTED (round 2: two referees ACCEPT; K64).
   - DEPENDS says L016 is "used only in the cell scan of Step 7 ... and for J_{1/6} of the pieces (Theorem 2)". L016 is also used in Proposition 9 (9.2 and 9.3 end with "contradiction with L016"), and it would be used in the fix of item 1.
   - Both lines should be updated.

7. **Novelty wording (README only).**
   - The README calls Theorem 6 "(new, via Tutte-Berge)".
   - The identity tau = N - nu(G) is HY EJC 24(2) (2017) P2.50 Prop. 9, which the certificate cites. The matching bound behind Theorem 6 belongs to the Chvatal-Hanson / subcubic-matching circle of results.
   - The README should cite these and leave the novelty question to the scout. The certificate itself makes no novelty claim.

8. **Suggestion, not a defect: G2 is narrower than stated.**
   - Let p, q in ∂(X) share no edge of R = H - V(X), with |X| >= 3 and |∂(X)| >= 2. Then the replacement e' = {p, q, z} (z new) always lies in C_3:
     - z has degree 1 and F7 has minimum degree 2, so no copy of F7 uses z;
     - linearity holds because no edge of R contains both p and q;
     - (P3) holds because e_{H'}(S) = e_R(S - z) + 1 <= |S| - 2;
     - p and q each lose an E* edge, so no degree exceeds 3.
   - 8.2 and 8.3 apply verbatim with nu = 1 and give A(H) >= 19|X| - 43 > 0.
   - So for |X| >= 3 and |∂(X)| >= 2 the only remaining exception is "every two vertices of ∂(X) share an edge of R". I re-derived this; the panel judge noted it first.
