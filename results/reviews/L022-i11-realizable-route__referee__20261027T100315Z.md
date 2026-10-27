VERDICT: NEEDS-WORK
(Editorial only. On the scale requested for this round this is ACCEPT WITH FIXES. Every round-1 item (referee #2 items 1-5 and referee #1 items E1-E4) is applied correctly. The edits are purely editorial: no theorem statement or proof step changed in substance, and the certificate remains PARTIAL with GAPs 1-3 open. The first line reads NEEDS-WORK only because the referee format allows just ACCEPT / REJECT / NEEDS-WORK, and ACCEPT requires that no problem remain. Four one-line status and consistency fixes remain, F1-F4 below. F1 was introduced by the fix round itself.)

Referee #3, round 2 (fix check), of results/proofs/L022-i11-realizable-route.md. Revised version: commit 510ae65 (2026-10-27 09:51 UTC), identical to HEAD and to the working tree. Round-1 base: 9954b8d~1, which is byte-identical to the 06:35 submission 9ea13d7 that both round-1 referees reviewed (`git diff 9ea13d7 9954b8d~1` is empty). Review written 2026-10-27, 09:55-10:05 UTC. Scratch folder: experiments/referee/L022-round2/.

## Summary

The round-1 revision changes exactly 15 of the 211 lines (4, 6, 7, 34, 38, 40, 60, 85, 87, 108, 116, 142, 161, 173, 175). I checked each word-level change against the two round-1 reviews and against the knowledge base.

- **Statuses.** L017 = K64 (Theorem 7 = K65), L018 = K67 (Theorem 5(vi) and Proposition 6.2 included, the latter conditional on P2), L019 = K68, L020 = K69, L021 = K71. P2' (C-version) is exactly L018's Conjecture P2. All of this is correct.
- **Step 1.5 hypertree verification.** The new delta-coefficient argument is correct and complete. It is more precise than either round-1 one-liner and should be kept (details below).
- **Theorem 2(vi).** It now also covers single edges. This is a trivial strengthening proved by the unchanged Step 2.6, and it agrees with L017 Theorem 4(vi), which has no single-edge restriction.
- **Corollary 3'.** The added hypothesis and the remark 2·12+3 = 27 < 29 are correct. The remark relies on r ≤ 3, which is L017 Theorem 4(iii) (accepted).
- **Step 1.4.** The case list is correct. I confirmed it by exhaustive enumeration.
- **Step 2.7.** The citation is removed correctly.
- **(19,16,8) row.** The "incomplete" annotation is exact.
- **W7 and GAP 4.** Both are tagged correctly, and every number in the GAP 4 update matches the stored outputs.

What remains is editorial:
- (F1) The new DEPENDS ON sentence says L021 is cited in GAP 1. L021 is cited nowhere in the certificate. The same sentence calls L020 a "target", but L020's accepted content is the refutation of Conjecture T''.
- (F2) GAP 1 still offers the refuted Conjecture T'' as a route.
- (F3) The sentence "None of GAP 1-4 is a finite statement" now contradicts the revised GAP 4.
- (F4) W7 and N4 still call the cell (25,23,11) "uncomputed".

## Item check

| Round-1 item | Where | Applied? | Check |
|---|---|---|---|
| R2-1 / R1-E1: outdated statuses | l.4 STATUS, l.6 L017, l.7 L018 | yes | **L017.** K64 (kb/known_results.md l.75) accepts Theorems 1-6, with the computational Corollaries 13.3/13.5 excluded. So "Corollary 13.3 ... not part of the accepted proved parts" (l.6) is right, and so is the remaining tag "[verified-here as a computation, NOT refereed]" at Step 6.1. K65 = L017 Theorem 7. **L018.** K67 (l.78) accepts "Theorems 1, 3, 5, 7, 8 ..., Propositions 6.2 (conditional on P2)", so "including Theorem 5(vi) and Proposition 6.2 (the latter conditional on L018's Conjecture P2)" is right. The quoted content of 5(vi) matches L018 l.139. A grep confirms that no "[unrefereed]" is left on L017's or L018's proved parts; the remaining "unrefereed" tags (l.12, 38, 58, 60, 149, 171, 175, 185) all refer to computations. |
| R1-E1: "[unrefereed]" on L018 Thm 5(vi) | Cor. 3 statement (l.38), Step 3.3 (l.116), Tags (l.60), GAP 3 (l.173) | yes | All four now read "ACCEPTED, K67". |
| R1-E1: P2' (C-version) = L018's Conjecture P2 | Cor. 3 statement (l.38), DEPENDS ON (l.7) | yes (not in Tags, see F5) | L018 l.156: "Every connected member of C with Δ≤3, slack 0 and at least 5 vertices has at most one pendant vertex." The only connected linear 3-graphs on fewer than 5 vertices are the isolated vertex (slack 3, not tight) and E_1, because no connected linear 3-graph has 2 or 4 vertices. So "connected, tight, at least 5 vertices" is the same as "connected, tight, not a single edge", and the identification is exact. |
| R2-2 / R1-E2: Thm 1(e) hypertree clause | Step 1.5 (l.87) | yes, written out and tagged [derived-here, sketch, not load-bearing] | Correct and complete; see the next section. The tag's claim that both round-1 referees checked the clause is accurate. Referee #2 checked it by hand. Referee #1's check_small_configs.py enumerates all one-edge extensions with 1, 2 or 3 old vertices, so 9-vertex hypertrees are included, and it reports "502 ... not exactly realizable: 0". K33 covers only configurations on ≤ 8 vertices (known_results l.39), so the hypertree clause is genuinely needed. |
| R2-3 / R1-E4: Step 2.7 citation | l.108 | yes | "which is absurd by the definition of τ". The logic is unchanged. |
| R2-4: (19,16,8) row incomplete | l.142 | yes | My recount: the inputs list cell_19_16_8.txt has 956 classes, 227 of them with Δ ≤ 3, and 66 of those 227 lie among classes 0-373. realize_19_16_8.jsonl has 374 lines: 308 skipped, 58 realizable, 8 not, so 161 are untested. All of this matches the row. |
| R2-5 / R1-E4: (vi) "re-proved", single-edge clause dropped | l.34, l.4 | yes | Step 2.6 is unchanged. The x_j have G-degree 1 or 2 (L017 4(i)). The pair lemma forbids two of them having F-degree 2 (4 − σ ≤ 2 is impossible), and this holds verbatim when F is a single edge {x_1,x_2,x_3}: there all three x_j have F-degree 1, ∂_F(x_j,x_k) is one edge, and the pairs are non-co-transversal because τ = 1. So (vi) holds for single edges with the proof as written. The downstream uses (Cor. 3 statement, 3.1, 3.4, GAP 2) still read "a single edge or at least two pendants", which is consistent. L017 Theorem 4(vi) (L017 l.68) has no single-edge restriction either. |
| R1-E3: Cor. 3' (30,15,11) hypothesis and remark | l.40 | yes | (30,15,11): s = 90+30−121 = −1, HY 187 ≤ 195, 30 ≤ 31. Under "I11 for ≤ 29 vertices" a violator here is a minimal counterexample: linear and vertex-critical, with a degree-3 vertex (L017 Thm 1(d)). L017 Thm 4(iii) gives r ≤ 3 (Theorem 2(i) even gives r ≤ 2). H − v has 15 − 3 = 12 edges, and a connected 3-graph with k edges has ≤ 2k+1 vertices. So H − v has ≤ 24 + 3 = 27 < 29 vertices: a contradiction that uses no stored list. Without Theorem 4, r could be as large as 6 and 24 + 6 = 30 ≥ 29, so r ≤ 3 is needed and is available. Step 3.4's original argument (H − v connected, 29 > 25) is unchanged and also valid. |
| R1-E4: Step 1.4 three coincidence types | l.85 | yes | Correct. Difference forms give a B-sum of ±1. A 1+3 / 3+1 parallelogram split gives ±1. An AP split gives ±1 or ±2. A 2+2 parallelogram split gives ±2 (equal signs in B) or X_p − X_q with p ≠ q (opposite signs). So φ_B(1) = 0 only for X_p − X_q, where φ_B(z) ≠ 0. One wording nit, no fix needed: the first clause ("split 2+2 between the parts gives X_p−X_q") means "with opposite signs in B", and the next clause covers equal signs. **Exhaustive check** (Part C): every cross form of Φ on 4+4 indices gives 72 cross forms with φ_B(1) = 0, all of them 2+2 parallelograms with φ_B = X_p − X_q; 0 violations. |
| W7 tag (R1 GAPs remark) | l.161 | yes | Tagged as unrefereed computations, with sources. |
| GAP 4 status | l.4, l.175 | yes | **Cell counts.** experiments/20261027-0340-induction-n28-n29-f25/progress.tsv l.39/l.41: (25,23,11,4) = 6 and (25,23,11,3) = 0. My parse of lists/cell_25_23_11_D4.txt: all 6 classes have n = 25, m = 23 and maximum degree exactly 4 (degrees 1²2⁶3¹³4⁴). **Realizability.** experiments/20261027-0400-realize-21-18-9/results_25_23_11_D4.json has "realizable": false for all 6. **L023.** results/proofs/L023-f25-equals-15.md exists (submitted 08:46 UTC, one GAP). journal/LOG.md l.635 shows its referees were launched, and there are no L023 reviews yet, so "pending / under referee" is accurate. "Nothing in Theorems 1, 2, 4 or Corollary 3 depends on it" is true. |

Nothing else changed: there are exactly 15 differing lines, the line count is unchanged (211), and I read every hunk in experiments/referee/L022-round2/wdiff_out.txt.

## The Step 1.5 delta-coefficient argument (the question put to this round)

**Setting.** A (4,5)-set A realizes the tree built so far, and a new edge {u,p,q} meets it only in u. Put p = x_u + δ and q = x_u + 2δ.

**The argument.** Every form of Φ on A ∪ {p,q} that involves p or q has value c + (α + 2β)δ, where α and β are its coefficients on p and q.
- In Φ's sign convention, α, β ∈ {+1, −1, −2, 0}. The value −2 occurs only on the midpoint of an AP form.
- So α + 2β = 0 with (α,β) ≠ (0,0) forces α = −2 and β = 1. The form is then X_a + X_q − 2X_p for some a ∈ A, with value x_a − x_u, which vanishes only for a = u. That is the intended AP.
- Every other form has a nonzero δ-coefficient and vanishes for at most one δ.
- Forms not involving p or q keep their values on A.
- So for all but finitely many δ, the set is weak Sidon and its APs are exactly APs(A) + {u,p,q}. This is linear because p and q are new, so the set is (4,5) by 0.2.

**Why u is an endpoint.** The parenthetical is right. If u is made the midpoint (p = x_u − δ, q = x_u + δ) while u is already the midpoint of (a,u,b), then p + q = a + b for every δ.

**Verdict on the question.** The written argument is correct and complete, and it should be preferred to the round-1 one-liners.
- Referee #2 wrote that "the only coincidence form whose delta-coefficient vanishes is X_i+X_q−2X_p with i = v". Referee #1 wrote that every form "has delta-coefficient α+2β ≠ 0, except the new AP form itself".
- Both are slightly inaccurate. All |A| forms X_a + X_q − 2X_p have δ-coefficient 0. What singles out a = u is that its constant value is 0.
- The certificate's text states exactly this.
- The only implicit steps are that forms not involving p or q are unchanged, and the final appeal to 0.2. Both are evident, and the clause is tagged as a non-load-bearing sketch.

**Computation** (check_step15_14.py; independent; no e757/judge imports; exact integers and Fractions):
- **Part A.** 27 base sets (the 7 sets of data/small_records.json and 20 random greedy (4,5)-sets of 6-12 points), every u: 241 cases.
  - Every Φ-form involving p or q was enumerated. 2,253 forms have δ-coefficient 0, exactly |A| per case, all of the type X_a + X_q − 2X_p. In every case exactly one of them vanishes (a = u), and the value x_a − x_u was checked for all of them.
  - A random δ avoiding the finitely many roots gave a (4,5)-set in all 241 cases (brute force over 4-subsets), with AP set exactly APs(A) + {(u,p,q)}.
- **Part B.** All 3 + 15 + 105 = 123 attachment sequences of linear hypertrees with 2, 3 and 4 edges, starting from an AP and built by the Step 1.5 procedure. All 123 were exactly realized on the first random δ (0 retries): (4,5) by brute force, AP set equal to the intended edges. The 105 four-edge sequences cover every 9-vertex linear hypertree.
- **Part D.** The midpoint counter-case p + q = a + b holds for every AP of the 27 sets (0 exceptions).
- **Part C** is the Step 1.4 enumeration above.

## Substance check

**Proofs.** No proof step changed in substance:
- Steps 1.4, 1.5 and 2.7 are expository rewrites of the same arguments.
- Steps 2.6 and 3.4 are untouched.

**Statements.** No theorem statement changed in substance:
- Theorem 2(vi) gained a trivially true case, covered by the unchanged proof.
- Corollary 3' gained a hypothesis that the original Step 3.4 had already used implicitly ("a violator with 30 vertices is then a minimal counterexample"), plus a remark giving a second short argument.
- Corollary 3's statement gained only status tags and the P2 = P2' identification.
- Theorems 1, 4 and 5 and Corollary 6 are unchanged.

**GAPs.** GAPs 1-3 are unchanged in content. GAP 4 received only a status update, which no proof uses.

## Problems remaining (in order of severity; all editorial, all one-line fixes)

**F1 (introduced in round 1, l.7, DEPENDS ON).** The sentence reads: "Also cited in GAP 1 only, as targets and not as dependencies: L019 (K68), L020 (K69) and L021 (K71), accepted proved parts."
- L021 is cited nowhere else in the certificate. `grep -c L021` gives 1 for the revised text and 0 for the round-1 text, and GAP 1 cites only L019 and L020.
- L020's accepted content (K69, L020 STATUS) is Theorem 1, *Conjecture T'' is false* (at least 45 connected Δ = 3, slack-1 classes in (29,23,12)). So L020 is not a "target".
- Fix: e.g. "Also cited in GAP 1 only, not as dependencies: L019 (K68; Conjecture C1 remains a conjecture) and L020 (K69; Conjecture T'' is refuted)". Drop L021, or add the intended L021 reference to GAP 1.

**F2 (pre-existing, l.169, GAP 1).** The text says "To exclude this one needs ... Conjecture C1 ... or a classification of such graphs (Conjecture T''; L020)."
- T'' (every connected member of C with Δ ≤ 3 and slack ≤ 1 has at most 26 vertices) is refuted by L020 Theorem 1 (K69, accepted 08:16 UTC; L020 was submitted 06:13 UTC, before L022).
- So this alternative is closed in the form T''. The sentence presents a refuted conjecture as an open route. This is the same kind of outdated status as round-1 E1.
- Fix: say that T'' is false (L020, K69), so any classification must include the slack-1 graphs with Δ = 3 and 29 vertices that L020 exhibits.

**F3 (pre-existing, now contradicted by the revised GAP 4; l.177).** The text says "None of GAP 1-4 is a finite statement; each is a statement about all sizes."
- GAP 4 concerns one cell, (25,23,11), and two lines earlier it is described as "closed by computation".
- Fix: "None of GAP 1-3 is a finite statement ...; GAP 4 concerned the single cell (25,23,11) and is closed by an unrefereed computation (L023 pending)."

**F4 (stale after the GAP 4 update).**
- W7 (l.161) still reads "(outside the uncomputed cell (25,23,11))".
- N4 (l.184) still lists "The cell (25,23,11,3) in C and its realizable part (GAP 4)" as a needed computation.
- Fix: mark both as computed (cell(25,23,11,3) = 0, unrefereed; L023 pending). The count "13 tight classes" in W7 stays correct, because the cell is empty for Δ ≤ 3.

**F5 (optional).** Round-1 E1 also asked for the Tags line (l.60) to say that P2' (C-version) is L018's Conjecture P2. That identification now appears in the Statement of Corollary 3 and in DEPENDS ON, but not in the Tags line.

None of F1-F5 touches a theorem, a proof or a computation. Once F1-F4 are applied, I see nothing left that would stand in the way of ACCEPT for the PARTIAL certificate (GAPs 1-3 open).

## Checks performed (all from experiments/referee/L022-round2/, under `nice -n 10` and `timeout`)

**Diff of the revision.**
- `git diff 9954b8d~1 510ae65 -- results/proofs/L022-i11-realizable-route.md`. The working tree equals 510ae65 and HEAD. The base equals 9ea13d7, the version reviewed in round 1.
- `python3 -I wdiff.py L022_old.md L022_new.md > wdiff_out.txt` gives the word-level diff of the 15 changed lines. L022_old.md and L022_new.md are scratch copies made with `git show`.

**Steps 1.4 and 1.5.** `timeout 900 nice -n 10 python3 -I check_step15_14.py > out_step15_14.txt`. Output:

```
Part A (Step 1.5 delta argument): 27 base sets; {'cases': 241, 'bad_struct': 0, 'a2_fail': 0, 'a2_vals_fail': 0, 'not45': 0, 'ap_mismatch': 0, 'zero_delta_forms': 2253}
Part B (hypertrees with 2-4 edges by Step 1.5 procedure): {'seqs': 123, 'ok': 123, 'retries': 0}
Part C (Step 1.4 coefficient sums): {'zero_cases': 72, 'violations': 0, 'zero_types': [('par', 2, 2)]}
Part D (midpoint counter-case p+q=a+b always): fails 0
```

**Recounts with inline Python** (exact counts are in the table above).
- (19,16,8): the stored list and realize_19_16_8.jsonl.
- (25,23,11,4): degrees in lists/cell_25_23_11_D4.txt, and realizable = false in results_25_23_11_D4.json.

**Status look-ups.**
- kb/known_results.md rows K33, K64, K65, K67, K68, K69, K71.
- L017 Theorem 4 (l.50-68).
- L018 Conjecture P2 (l.156) and Theorem 5(vi) (l.139).
- The L020 and L023 headers.
- journal/LOG.md l.621-625 and l.635.

**Earlier work.** I read referee #1's check_small_configs.py to confirm that its 502 configurations include 9-vertex hypertrees.

## Independence statement

I read both round-1 reviews (as permitted) to get the item list, then checked every item myself against the certificate text, the knowledge base and the stored data. My scripts (wdiff.py, check_step15_14.py) are new, written for this review. They import nothing from e757/, judge/, experiments/prover/ or the round-1 referee folders, and they use exact integer and Fraction arithmetic. The only code from earlier work I looked at is referee #1's check_small_configs.py, which I read but did not run, to confirm what its count covers. I did not modify the certificate or any file outside experiments/referee/L022-round2/ and this review.

## Round 2 re-check (commit 4c32ca5, checked 2026-10-27 10:07 UTC)

**What I checked.**
- I ran `git show 4c32ca5`. The working tree and HEAD are identical to 4c32ca5 for the certificate.
- I produced a word-level diff against 510ae65 (experiments/referee/L022-round2/wdiff_r2_out.txt). Exactly 6 lines changed (4, 7, 161, 169, 177, 184), and no theorem statement or proof step was touched.

**Item by item.**
- **F1 (l.7): fixed.** L020 is now described as "(K69; it REFUTES Conjecture T'' and gives the structure of near-tight graphs at a degree-3 vertex)". That matches K69 and L020 Theorems 1 and 3. L021 is now "not used here", which is correct.
- **F2 (l.169, GAP 1): fixed.** GAP 1 now says T'' is refuted by L020 Theorem 1 (K69). It also says "L020 Corollary 5 states the replacement hypotheses C1-big and R-big", which matches K69.
- **F3 (l.177): fixed.** The sentence now reads "None of GAP 1-3 is a finite statement ... (GAP 4 was finite and is closed by the unrefereed computation cited there)".
- **F4: substantively addressed.**
  - N4 (l.184) now reads "DONE, unrefereed": cell(25,23,11,3) empty and 6 non-realizable classes in cell(25,23,11,4). This matches the counts I verified above.
  - W7 (l.161) gained the note "the 6 classes of cell(25,23,11,4) are also non-realizable, each containing the 8-point obstruction Q_8 of L023; unrefereed".
  - I checked that note independently with check_q8.py (out_q8.txt; exact RREF; no imports from e757, judge or prover code). Q_8 has 95 injective midpoint labellings and all 95 are dead: 60 force a parallelogram and 35 force equal points, which matches L023's 35/60/0. Q_8 occurs as a sub-hypergraph of each of the 6 classes, with 4 ordered occurrences each, again matching L023. Since R is closed under sub-hypergraphs (Theorem 1(e)), each class is non-realizable.

**Cosmetic leftovers.** None of these is required.
- W7's first sentence still reads "(outside the uncomputed cell (25,23,11))". This is harmless given the appended note, and the count of 13 classes stays right.
- The STATUS line ends in "edge.; round-2 items".
- The line-7 phrase "as targets" now sits next to a refutation.
- F5 (the Tags line) is not applied; it was optional.

Final verdict: ACCEPT. All round-1 and round-2 items are applied correctly; L022 is a correct PARTIAL certificate (Theorems 1, 2, 4 and Corollary 3 proved; Corollary 3', Theorem 5 and Corollary 6 computational; GAPs 1-3 open; GAP 4 closed by an unrefereed computation, L023 pending).
