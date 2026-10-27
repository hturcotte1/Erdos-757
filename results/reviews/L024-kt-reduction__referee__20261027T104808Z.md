VERDICT: ACCEPT

# Referee report #5 (round 3, fix check only): results/proofs/L024-kt-reduction.md at commit dfcb180

Referee: Claude (Opus 5.5), 2026-10-27 10:44-10:50 UTC.

Scope: whether the round-2 items were applied correctly in commit dfcb180. The items come from two round-2 reviews:
- results/reviews/L024-kt-reduction__referee__20261027T103936Z.md (opus, NEEDS-WORK, items N1-N6);
- results/reviews/L024-kt-reduction__referee__20261027T103204Z.md (fable, ACCEPT, optional notes N1-N2).

Verdict vocabulary: the task offered ACCEPT or ACCEPT WITH FIXES; my standing instructions allow ACCEPT, REJECT or NEEDS-WORK. ACCEPT is in both lists, so there is no conflict.

## Summary

Commit dfcb180 changes only the certificate: 7 hunks, +9/-5 lines. Each hunk is one of the requested items:
- the STATUS line;
- the Remark after Lemma A+;
- the (G2-i) note;
- Step 5.6 (citation and H.1 scope);
- Step 7.3 (edge argument);
- the C5 bullet;
- the Sanity-checks bullet.

Nothing else changed. No later commit touches the certificate or experiments/prover/L024/, and the working copy is identical to the dfcb180 blob.

N1-N4 are applied correctly. I checked each insertion against the certificate's own Steps 0.1, 0.5, 0.8, 4.1, 4.2, 4.7 and 6.1-6.3, against L021 0.3, 0.5, 3.4 and 8.1, and against the stored piece data. Each one is mathematically accurate.

The sharpening of Lemma A+ appears only as a separate Remark, and it is tagged "[derived-here by the round-2 referee; computer-checked, unrefereed]". Lemma A+'s statement is unchanged. 46 remains the proved bound in Lemma A+, 7.1 and 7.3, and the bound 37 appears nowhere else. The Remark's claims are also correct by hand (see below).

The (G2-i) note accurately reports the fable round-2 observation.

The certificate remains conditional. CLAIM-TYPE still says "NO bound is claimed". Theorem 6 still derives KT^{L*} (hence 11 tau <= (19/6) n + 2m on C and c* >= 35/66) only from GAP R1-R3, which remain open and marked GAP.

Scope of this verdict: I re-checked the changed text and the passages it depends on. I did not re-referee the unchanged mathematics, which was checked in rounds 1 and 2 (fable round 2: ACCEPT; opus round 2: every mathematical step checks out). On that basis, together with the two round-2 reviews, the certificate is acceptable as a conditional certificate.

## Item-by-item check

- **N1 (C5 and Sanity-checks bullets): applied correctly.**
  - The C5 bullet now reads "C5 covers 25 of the 49 type triples with a rich piece and pieces of at most 10 vertices, namely exactly the 25 with ΣW >= 36 (the richcheck list of pattern_a3.py; the other 24 fail the weight condition of Step 6.2 and were not run)", and "the other 23 of the 25".
  - The Sanity bullet reads "for the 25 type triples with a rich piece, pieces of at most 10 vertices and ΣW >= 36 (the 25 of the 49 ...; the other 24 fail the weight condition of Step 6.2)".
  - I checked the counts. There are 7 pieces with at most 10 vertices: E1 (W 16), (8,5,3)#0,#1 (W 5) and (10,7,4)#0-#3 (W 13; #0 and #3 rich). That gives C(9,3) - C(7,3) = 84 - 35 = 49 multisets with a rich piece.
  - The richcheck branch of pattern_a3.py (the `else:` branch after line 177) builds (E1,E1,T0), (E1,E1,T3), the 7 triples (E1,Tx,Ty) and the 16 triples (Tx,Ty,Tz) that meet {0,3}. That is 25 triples, with ΣW in {45, 42, 39}, all >= 36.
  - The 24 omitted triples all contain an (8,5,3) piece:
    - {E1,R,Q}: 4 triples, ΣW 34;
    - {R,T,Q}: 14 triples, ΣW 31;
    - {R,Q,Q'}: 6 triples, ΣW 23.

    All are below 36.
  - "The weight condition of Step 6.2" is (C4) ΣW_i >= 36 of 6.1, as applied in 6.2. This is consistent with the round-1 wording of 6.3.
- **N2 (citation): applied correctly.** 5.6 now cites "(0.1/L021 0.5)" for DEF(H) >= DEF_H(X) + DEF(R).
  - L024 0.1 contains the union-of-families fact: E*_H(X ∪ Y) = E*_H(X) ⊔ E*_{H-V(X)}(Y), with additivity of DEF.
  - L021 0.5 ("Union of families") states DEF_H(X ∪ Y) = DEF_H(X) + DEF_R(Y).
- **N3 (edge argument for W2 in 7.3): applied correctly.** The parenthetical inserted in 7.3 is a correct proof of the edge identities.
  - In (β), all three edges at v avoid w (w is not a co-vertex). They contain v ∈ V(F_w) (Lemma A(a)), so they lie in the component F_w of H - w, which is induced.
  - In (δ), e_k and e_l avoid w, so they lie in F_w; e_j avoids w', so it lies in F_{w'}.
  - Every other edge lies in a component of H - v, which is F_v or some D_i. By (4.2) and the (β)/(δ) parts of 4.7, V(D_i) ⊆ V(F_w) (or ⊆ V(F_{w'}) for D°). Since w ∉ V(F_w), such an edge is an edge of H - w inside V(F_w), hence an edge of F_w (resp. F_{w'}).
  - So E(H) = E(F_v) ∪ E(F_w) in case (β), and the three-piece union in case (δ).
  - The argument sits in 7.3, not in 4.7 as opus N3 preferred. This is acceptable: the edge statement is used only to specify GAP R2 (7.3), and the derivation now appears where it is used.
  - Grammar: a comma precedes the parenthetical and none follows it. This is cosmetic.
- **N4 (H.1 scope): applied correctly in content.** 5.6 now says "H.1 holds for any such X by the proof of L021 8.1 (Claim E for subfamilies and (L1))". I read L021 8.1's proof. It uses:
  - |E*(X)| = |X| + 1 (so that B - e has sides of size |X|);
  - Hall's theorem;
  - E*_H(S) = N_B(S) and Claim (E) for the subfamily S;
  - (L1).

  It does not use the optimality of X, and Claim (E) holds for every nonempty L*-family in a minimal counterexample (0.2(E)). So H.1, and with it the remark "no minimum transversal of R meets ∂(X)", holds for every X with |E*(X)| = |X| + 1 in a minimal counterexample. Wording: see O2.
- **Lemma A+ sharpening: recorded correctly.**
  - It is a separate "Remark (sharpening of Lemma A+; [derived-here by the round-2 referee; computer-checked, unrefereed])", placed after the statement.
  - It ends "Lemma A+'s statement above is unchanged (46 stays as the proved bound)". The diff confirms that the statement lines are untouched, and 7.1 ("they have n <= 46") and 7.3 ("n <= 31, resp. n <= 46") are unchanged.
  - Its content is accurate:
    - "(γ) never occurs" and "(α) only for E1" are already proved in 4.7.
    - "(β) exactly for pieces with a degree-3 vertex": by (4.1), d_H(u) = d_{F_v}(u) + [u co-vertex] and Δ(H) <= 3. A non-co-vertex w ∈ Z therefore has d_{F_v}(w) = 3. Conversely, a vertex of F_v-degree 3 lies in Z and is not a co-vertex. That a (β) configuration exists for each such piece rests on the cited check.
    - "(δ) only for (8,5,3)#0, so n <= 37":
      - in (δ), vertices of Z have F_v-degree 2 and the others have H-degree <= 2, so Δ(F_v) <= 2;
      - by 0.8 this leaves E1 or an (8,5,3) graph;
      - Z ≠ ∅ excludes E1;
      - the stored data give (8,5,3)#0 degree sequence 2^7 1 (Δ = 2) and (8,5,3)#1 degree sequence 3 2^5 1^2 (Δ = 3);
      - so F_v = (8,5,3)#0 and n <= 1 + 8 + 28 = 37.
    - The cited computer check exists. experiments/referee/L024-round2-opus/check_r2_output.txt contains `PART A TOTAL {'alpha': 1, 'beta': 322785, 'gamma': 0, 'delta': 488} BAD 0`.
- **(G2-i) note (fable round 2): accurate.**
  - The note reads: "the boundary constraint proved in Step 5.6 (no minimum transversal of R meets ∂(X); τ(R+e') = τ(R)+1 for every pendant replacement e') makes GAP R1 weaker than stated: R1 only needs to exclude (G2-i) under that constraint."
  - This is correct. The constraint is the bracketed 5.6 remark, valid for every X with |E*(X)| = |X| + 1 (N4 above). In (G2-i), ∂(X) ≠ ∅, so R ≠ ∅ and minimality applies to R.
  - Forward direction of "τ(R+e') = τ(R)+1": a transversal of R + e' of size τ(R) cannot contain a new vertex, so it is a minimum transversal of R meeting e' ∩ V(R) ⊆ ∂(X).
  - The note mentions only (G2-i). The 5.6 remark already says the constraint "holds also in (G2-i), (G2-ii)", so nothing inaccurate is stated.
- **STATUS line: accurate.** It reads "revised 2026-10-27 10:41 UTC after referee round 2 (fable ACCEPT; opus NEEDS-WORK = editorial items N1-N4, applied; sharpening of Lemma A+ recorded as a remark)". The commit time is 10:41:37 UTC, and the certificate is still marked "unrefereed".

## Checks performed

1. `git show --stat dfcb180`: 1 file (the certificate), 9 insertions, 5 deletions. `git show dfcb180 --word-diff=plain`: 7 hunks, all listed above, with no other change.
2. Changes after the commit:
   - `git log --oneline dfcb180..HEAD -- results/proofs/L024-kt-reduction.md experiments/prover/L024/`: empty.
   - `git diff dfcb180 HEAD --stat` on the same paths: empty.
   - `git status --short` on the same paths: clean.
   - `sha256sum` of the working copy equals that of `git show dfcb180:results/proofs/L024-kt-reduction.md` (dd1c283f...ddc23c).
3. Read in full:
   - certificate: 0.1, 0.5, 0.8 (heading), 4.1, 4.2, 4.7 (α)-(δ), 5.6, 6.1 (C4), 6.2, 6.3, 7.3, the Lemma A+ statement and Remark, and Proposition 3 with (G2-i)-(G2-iii) and the note;
   - L021: 0.3, 0.5, 3.4 and 8.1.
4. `sed -n '160,190p' experiments/prover/L024/pattern_a3.py`: the TYPES list of the richcheck mode (25 triples; see N1).
5. A 5-line standard-library script reading experiments/prover/L021/closure_results.json as data gave the degree sequences of the pieces with at most 10 vertices:
   - E1: 1^3;
   - (8,5,3)#0: 2^7 1;
   - (8,5,3)#1: 3 2^5 1^2;
   - (10,7,4)#0, #3: 3 2^9;
   - (10,7,4)#1, #2: 3^2 2^7 1.
6. `grep 'PART A TOTAL' experiments/referee/L024-round2-opus/check_r2_output.txt`: the line quoted above (BAD 0).

## Remaining problems

None that requires a change to the certificate. These optional notes are not conditions of acceptance:

- **O1 (outside the certificate).** experiments/prover/L024/README.md line 34, last committed in 5da1199, still describes C5 as "25 type triples with a rich piece and pieces of <= 10 vertices", without "ΣW >= 36". This is the imprecision N1 fixed in the certificate. N1 as formulated named only the two certificate bullets. A one-line README fix is advisable, but it is not load-bearing: C5 is a cross-check "not needed for the proof".
- **O2 (wording, 5.6).** "H.1 holds for any such X" refers forward to "every X with |E*(X)| = |X|+1 in a minimal counterexample", later in the same sentence. Stating that class directly would be cleaner. The content is verified (N4).
- **O3 (label).** The Remark uses "(γ)". The statement of Lemma A+ calls this case only "the fourth logical case"; the label (γ) is defined in proof Step 4.7. Writing "(γ) (the fourth logical case)" would make the Remark self-contained.
- **O4.** Opus round-2 N6, which that review classed as cosmetic, was not applied:
  - Theorem 6's dependency list says "Theorems 1-6" although Theorem 5 is unused;
  - the certificate's C4 command does not mention the optional output argument;
  - the Theorem 4 remark for n <= 17 rests on L021's unrefereed cell completeness.

  All three are harmless, as that review says.

## Independence statement

I read the two round-2 reviews, and the two round-1 reviews only where they defined the items, to obtain the checklist. I then verified every change myself against the certificate text, L021's text and the stored piece data, and did not rely on either review's conclusions. The exception is that the Remark's "occurs for each piece" and "(γ) count 0" statements rest, as the Remark itself says, on the round-2 referee's computer check; I confirmed that its output file exists and reads BAD 0.

I ran no search code. The only code I ran was a 5-line standard-library script reading piece edge lists as data, plus git and grep commands.

I modified no file other than this review.
