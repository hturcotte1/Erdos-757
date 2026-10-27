VERDICT: ACCEPT

Referee #3, round 2 (Claude Opus 5.5), on results/proofs/L017-i11-minimal-counterexample-structure.md as revised in commits 9a1819e (05:03:55 UTC) and b2e9c52 (05:13:39 UTC). Scratch folder: experiments/referee/L017-round2-opus/.

## Summary

The revision is purely editorial. `git diff 7e85c20 -- results/proofs/L017-...md` touches one file (16 insertions, 12 deletions), and `git diff ef8f6b1 7e85c20` on that file is empty, so the base is the round-1 text.

**Every round-1 fix was applied correctly.** That covers the four items of referee 1 (NEEDS-WORK, 20261027T045608Z), the five of referee 2 (ACCEPT WITH FIXES, 20261027T050734Z) and the three certificate-level recommendations of the scout (KNOWN, 20261027T050242Z). No edit changes a hypothesis or conclusion of Theorems 1–7. The edits do three things:
- add two small explicit statements, both already implicit in the round-1 text and both correct: $E^*\ne\emptyset$ in Theorem 2(H), and the $F_2$ side of Theorem 4(vi)(f);
- correct one false sentence in a remark (Remark 13.2, Property (P) for $E_1$);
- add attributions.

**Edited passages.** I re-derived every edited passage by hand:
- 2(H) and Step 3;
- 4(vi)(f) and 7.6;
- 9.2, including the free-choice justification;
- 9.3, checked against the engine source and the C4 output;
- 10.1, 13.1(ii) and 13.2.

**Citations.** I checked them against the PDF in the repository, kb/literature/papers/henning_yeo_ejc_2017.pdf: Definition 5, Proposition 9 ("well-known"), and Theorem 14 at k = 3, which is 18τ ≤ 4n+4m+2. I also checked the Henning–Yeo arXiv:1802.01825 §7 excerpt (Claims D–F).

**Independent computation.**
- Exact recomputation of Property (P) and the Theorem 4(vi)(f) $F_2$-side conclusion on the 13 refereed tight Δ≤3 classes.
- 6,000 random degree-3 extensions of real class-C components of slack 0 or 1. On these, the Theorem 4(iv) condition, evaluated on the components, agrees in every case with τ(H′) = τ(G)+1 computed directly on H′; this is Theorem 6(ii) for arbitrary extensions. Every non-deficient distribution gives τ(H′) = τ(G).
- The Chvátal–Hanson bound |E| ≤ 3ν+⌊ν/2⌋ on all 16,335 subcubic graphs with at most 11 vertices.

All give 0 failures.

**Spot checks.** I checked these steps adversarially by hand and found them correct:
- Theorem 1(g), m-minimality;
- Theorem 5(B)(ii) and 5(A)(iv)(β);
- Theorem 4(iii), the exclusion of r ≥ 4;
- Theorem 3(a), (e);
- Theorem 7, both 4.2 and the Tutte–Berge case table of 4.4;
- the no-circularity claim.

**Honest description.**
- The STATUS line now says what was done and states that the revision is unrefereed.
- Theorem 7 is labelled known: "[published, re-proved here]", at the statement and in 4.6(c).
- The Hall device is attributed to Henning–Yeo at Theorem 2(H) and in Step 3.
- The "Relation to the Henning–Yeo method" section opens by saying that Theorems 1–6 are the new content.
- 13.2, 13.3, 13.5 and 13.6 remain tagged "[verified-here as a computation, not refereed]". 13.4 is tagged "[derived-here from … the computational Corollary 13.3]" and says "Nothing here is proved unconditionally".

**Remaining items.** Five optional editorial points remain (below). The most visible is that the Tags paragraph still says "Theorems 1–7 [derived-here]". None is a gap, an error or a misattribution, so the verdict is ACCEPT.

## Fix-by-fix check

| Round-1 item | Applied? | Where / how checked |
|---|---|---|
| Ref. 1 #1: Property (P) in Remark 13.2 is false for $E_1$ | **Applied correctly** | 13.2 now says (P) "holds for the 12 connected tight classes with Δ≤3, at least 10 and at most 26 vertices". It names $E_1$'s three pairs as exceptions for the right reason (degrees (1,1), shared edge, τ = 1). 12 = 4+2+6 = (10,7,4)+(14,12,6)+(17,13,7). Recomputed: check A below. |
| Ref. 1 #2: Step 9.3 engine description ("up to 2d components") | **Applied correctly** | Now reads "processes all decompositions, including those with r≥4, even r>2d, and discards disconnected extensions only at the `filt` stage". Code: experiments/prover/L013/engine.py, identical to L012's (`diff` gives no output). `recurse` loops over every output of `decompositions()`, which has no bound on the number of parts. Connectivity is enforced only by `filt` (`#conn=1`). The C4 output (engine_decomps_output.txt, lines 67–71) has r = 7 > 2d = 6 at (27,14,10,3), with 2 inputs. |
| Ref. 1 #3: DEPENDS ON overstates independence from (P2), (P3) | **Applied correctly** | The bullet now adds "with the exceptions stated in Step 10.1: '$n\ge28$' in Theorem 1(a) and '$n-2\ge26$' in Theorem 5(B)(ii) rest on L016, a statement about the class C". This matches 10.1 and my own scan of the proofs (see "Re-verified passages"). |
| Ref. 1 #4: Theorem 6(ii) converse lacks the free-choice justification | **Applied correctly** | The 9.2 parenthetical says each $F_i\in C$ has $s(F_i)\le1$ and no isolated vertex, and that $F_i-x\in C$ has fewer than N vertices, so $s(F_i-x)\ge0$ by the choice of N and (U) applies. This is correct. See note E3: free choice is only needed for one direction. |
| Ref. 1 observations (a)–(c) (optional) | (a) not added (optional, no harm); (b) reflected by "2\|E\| ≤ 7ν" (Chvátal–Hanson); (c) added to 13.1(ii) | (c): experiments/falsify/i11-structure-lemmas/REPORT.md, line 18, gives "(25,23,11), Δ = 4: 3 isomorphism classes (4 graphs …)", consistent with "three tight members". experiments/20261027-0400-realize-21-18-9/results_main_21_18_9.json has 12 entries, all `realizable: False`. Both are tagged [unrefereed] and are not load-bearing. |
| Ref. 2 #1: Theorem 4(vi)(f), $F_2$ side | **Applied correctly** | Added to the statement ("for the $F_2$ side of (f), the other vertex of $\{d,f\}$ in $F_2$") and to 7.6(f) as a separate paragraph. Re-derived below; checked on data (check A). |
| Ref. 2 #2: Theorem 2(H), degenerate case $E^*=\emptyset$ | **Applied correctly** | Added: "(the existence of such φ and $x_e$ is contradictory; in particular $E^*\ne\emptyset$, since for $E^*=\emptyset$ the proof of 3.1 already gives $0>s(R)+\sum_is(F_i)\ge0$)". Re-derived below. |
| Ref. 2 #3: "inputs" are multisets | **Applied correctly** | 9.3 now says "inputs" are multisets of class tuples, "e.g. 10, not 16, for (10,7,4)+(10,7,4)". The engine does use `itertools.combinations_with_replacement(range(len(cls)), k)`, and C(4+1,2) = 10. The C4 output at (24,18,10,3) (lines 21–27) gives [(3,1,1),(10,7,4),(10,7,4)] → 10 and [(3,1,1)²,(17,13,7)] → 6, total 16 as quoted. |
| Ref. 2 #4: 10.1, "members of C" in Theorem 4(ii) | **Applied correctly** | Added: "For a violator outside C, read 'members of C' in Theorem 4(ii) as 'connected 3-graphs with s≥0'; the proofs never use membership of the components in C." True: 7.2 uses only s(F_i) ≥ 0 (proper induced subgraphs) and Δ(F_i) ≤ 3. |
| Ref. 2 #5: STATUS timestamp | **Applied correctly** | "submitted 2026-10-27 04:05 UTC" matches commit ef8f6b1 (04:05:19 UTC). The revision time 05:13 matches b2e9c52 (05:13:39 UTC). |
| Scout #1: Theorem 7 is known (HY EJC Prop. 9 + Thm 14; Chvátal–Hanson) | **Applied correctly** | In the Theorem 7 statement and in 4.6(c). Citation check below. |
| Scout #2: Hall device from HY arXiv:1802.01825 §7 | **Applied correctly** | In the Theorem 2(H) statement and in the Step 3 header ("Claims D–F"). In kb/literature/sources/henning_yeo/henning_yeo_1802.01825_sec7_deficiency.txt, Claim D (line 243) is the Hall argument ("no matching in $G_X$ … By Hall's Theorem"), and Claims E and F (lines 259–260) are its deficiency consequences. The attribution is accurate. |
| Scout #3: label the novelty | **Applied** (one cosmetic residue, E1) | "The new content of this certificate is the structure theorems 1–6 …; Theorem 7 and the Hall device are known" opens the HY section. |
| Scout #4: bibliography additions | not applicable | This concerns kb/, not the certificate. |

## Re-verified passages (by hand)

**Theorem 2(H) and Step 3.**
- Let $e\in E^*$ and $i=\varphi(e)$. Then $F_i-x_e=H[W_i\setminus\{x_e\}]$ is a proper induced subgraph, so $s(F_i-x_e)\ge0$, and (U) gives a minimum transversal $T_i\ni x_e$.
- Injectivity gives one prescribed vertex per block.
- Every edge of $E^*$ contains its $x_e\in T_{\varphi(e)}$, so (R+) holds with $T_0=\emptyset$. Then 1.3 gives $0>s(R)+\sum s(F_i)+2|E^*|\ge0$.
- For $E^*=\emptyset$ the same computation applies verbatim: the empty map, and $H=R\sqcup\bigsqcup F_i$. So the hypotheses force $E^*\ne\emptyset$, as the new parenthetical says.
- The "in particular" (3.2) is unchanged and correct. Hall's deficient set is automatically nonempty.

**Theorem 4(vi)(f) and 7.6, $F_2$ side.**
- The attachment vertices have $d'=d_H-1\in\{1,2\}$ (7.1).
- If $F_2$ is tight, (v) and the pair lemma give $|\partial_{F_2}(d,f)|=d'(d)+d'(f)-\sigma\le2$.
- Both $d'=2$ would need $\sigma\ge2$. If exactly one has $d'=2$, then $\sigma=1$.
- So at most one of d, f has H-degree 3, and if one does, it shares an $F_2$-edge with the other. This is correct.

**7.6(f), $F_1$ side (reworded).** I re-derived both sub-cases:
- If $d'(a)=2$, then $c$ and $e$ have $d'=1$ and lie in edges through $a$. The only edge at $c$ avoids $b$ (else $P_1\subseteq$ an edge of G), so $d'(b)=1$.
- If $d'(a)=d'(b)=1$ and $d'(c)=2$, the two edges at $a$ and $b$ both contain $c$ and are distinct by (i). Then $d'(e)=2$ would put $\{c,e\}$ in two edges, which linearity forbids.

**9.2, free choice for an arbitrary extension H′.**
- The justification is correct: $s(F_i)\le1$, $F_i$ connected and so without an isolated vertex, $F_i-x\in C$ with fewer than N vertices, so $s(F_i-x)\ge0$ by the choice of N, so $x$ is co-transversal by (U).
- The first half of 9.2, $\tau(H')=\tau(G)+1\iff(\star)$ via 0.3, holds for every extension.
- $s(H')=s(G)+3+6-11$. Linearity of H′ follows from the pair conditions.

**9.3, engine.** The description matches `recurse`:
- d runs over $\lceil3m/n\rceil..D$;
- $t'\in\{t-1,t\}$, with branches skipped if $S'<0$;
- `pieces()` admits isolated vertices only if $S'\ge3$;
- `ext_d (n-1) t' t d (d-1)`;
- `filt` keeps C-members that are connected with τ = t.

**10.1.** I scanned the proofs of Theorems 1(a)–(f), 2, 3, 4 and 5 for uses of (P2)/(P3) or membership in C:
- The only class-C inputs are "n ≥ 28" in 1(a) and its consequence "n−2 ≥ 26" in 5(B)(ii). Step 6 uses n ≥ 28 only to make the sets Z nonempty, and nonempty is all 1.3 needs.
- The label "members of C" in 4(ii) is now covered by the new sentence.
- Theorem 1(g) uses edge-deletion heredity of C, and it is correctly excluded from the list.

**13.2.** Property (P) holds for the 12 classes. The $E_1$ exception is stated correctly. Recomputed: check A.

**Theorem 7 tags and citations.** From the extracted text of kb/literature/papers/henning_yeo_ejc_2017.pdf (excerpt in hy/hy_ejc2017_excerpt.txt):
- Definition 5: $\mathcal H_k$ = "connected, linear, k-uniform hypergraphs with maximum degree 2".
- Proposition 9: "$\alpha'(G_H)=|E(H)|-\tau(H)$", introduced by "The following result is well-known (see, for example, [7])".
- Theorem 14: "For k ⩾ 3 an odd integer, if H ∈ $\mathcal H_k$, then τ(H) ⩽ ((k−2)(k+1)n + (k−1)²m + k−1)/(k(k²−3))". At k = 3 this is 18τ ≤ 4n+4m+2.

The derivation of I11 from Theorem 14 (4.6(a): n ≥ 5 and 3m ≤ 2n for connected components with m ≥ 2, plus additivity) is correct. It even gives s ≥ 1 for connected H with m ≥ 2, since 10n − 8m − 22 > 0 for n ≥ 5. Theorem 7's general identity $\tau=m-\nu(G)$ is Proposition 9 plus additivity over components; isolated vertices and isolated edges are trivial.

The Chvátal–Hanson reference (JCTB 20 (1976) 128–138, as in kb/literature/bibliography.md) is cited for |E| ≤ 3ν+⌊ν/2⌋ at Δ = 3. I did not check it against the 1976 paper, but I verified the formula numerically (check C). From it, 2|E| ≤ 7ν and hence 11ν ≥ 3|E| (strict for |E| ≥ 1). The certificate no longer presents Theorem 7 as new: see the statement, 4.6(c) and the HY-section opening sentence.

## Spot checks (adversarial, by hand)

**Theorem 1(g), m-minimality.**
- All minimal counterexamples have the same N, since each excludes the other from having fewer vertices. So "m least" is well defined.
- $H\setminus D\in C$ by edge-deletion heredity and has N vertices, and every member of C with fewer vertices satisfies I11. So $s(H\setminus D)<0$ would give a minimal counterexample with fewer edges.
- This yields $11\tau(H\setminus D)\le11\tau+s-2k$, and by integrality $\tau(H\setminus D)\le\tau-\lceil(2k-s)/11\rceil$. For k = 1 and s ∈ {−1,−2} the ceiling is 1.
- A minimum transversal of $H\setminus e$ misses e, so adding $x$ gives a minimum transversal T with T ∩ e = {x}. Correct.

**Theorem 5(B)(i), (ii).**
- (i): $s(H-y)=s+6=5$, and $a$, $b$ have degree 1 in $H-y$. Every component of $H-y$ contains $a$ or $b$ (0.7). A component K containing $a$ with $s(K)<5$ would make $a$ co-transversal ((U), with $K-a$ a proper induced subgraph), which is excluded. So both components have slack ≥ 5, and with total 5 there is a single component.
- (ii): By 6.6, $s(F)=0$ and $\tau(F)=\tau-1$. Every component of F contains one of b, c, d (0.7, with $\partial\{y,a\}=\{e,f\}$). Tight components have no isolated vertex.
- $b\notin f$ by linearity, so $d_F(b)=1$, with g ∉ ∂{y,a}.
- (⋆)-type exclusion holds, and free choice in tight components makes F connected.
- Pair lemma: $1+d_F(c)-\sigma_F(b,c)\le2$.
- $g\not\supseteq\{c,d\}$ because $|g\cap f|\le1$.
- The vertex outside g has $d_F=1$ and H-edges f plus its F-edge, so $d_H=2$. Correct.

**Theorem 5(A)(iv), (β).**
- Hall on {P_1,P_2} versus the non-trivial components: each pair contains a vertex of H-degree ≥ 2 (Theorem 3(a)), hence has a neighbour. So $N(P_1)=N(P_2)$ is the unique non-trivial component.
- (β): s(F) = s(G) − 3 = 0, and $d_H(b)=2$ by 3(c). c and d have degree ≥ 2 because at most one isolated vertex exists. The pair lemma gives |∂| ≤ 2. Correct.

**Theorem 4(iii), r ≥ 4 impossible.** |J| = 3 deficiency needs r ≤ 2. |J| = 2 deficiency puts two pairs in one component, and then the pairs meet at most 3 < r components, contradicting 7.2. Correct.

**Theorem 3(a), (e).**
- (a): Z = e and T = {a} give $11>9+2d(a)$, impossible since $a\in e$.
- (e): Z = {x,y₁,y₂}, T = {x} and |∂Z| = 2 give 11 > 13, false.
- Correct.

**Theorem 7 (4.2, 4.4).**
- 4.2 lower bound: |F| ≥ |U| − k, k ≤ ν, and $|T_1|\ge m-|U|$. Correct.
- 4.4: $2\nu-\tfrac6{11}M\ge\tfrac4{11}|U|+\sum t_i$. I re-derived every case of the table: c = 1: 0; c = 2: 16/11; c = 3: 4/11; c = 4: 8/11; c = 5 (e ≤ 7): 2/11; even c ≥ 6: 2c/11; odd c ≥ 7 (e ≤ (3c−1)/2): (2c−8)/11. Strict for M ≥ 1. Correct.

**No circularity.** Every graph whose I11-slack is assumed nonnegative in Theorems 1–5 is one of: H − Z with Z ≠ ∅; R with W ≠ ∅; F_i with W_i ≠ V(H); or F − X with F induced and X ≠ ∅. All are proper induced subgraphs. Two exceptions are handled correctly:
- Theorem 1(g) uses graphs $H\setminus D$ on the same vertex set, covered by the m-minimality hypothesis.
- Theorem 6 uses graphs with fewer than N vertices, covered by the choice of N (see E2).

## Checks performed (commands and outputs; one niced process at a time, all under `timeout`)

**Diff and provenance.**
- `git diff ef8f6b1 7e85c20 --stat -- results/proofs/L017-…md`: empty.
- `git diff --word-diff=plain 7e85c20 -- results/proofs/L017-…md`: 14 hunks, all listed in the table above; 16 insertions, 12 deletions.
- `git log -- results/proofs/L017-…md`: the round-1 version is ef8f6b1 (04:05:19); the revisions are 9a1819e (05:03:55) and b2e9c52 (05:13:39).

**Check A** (Remark 13.2, Property (P), and Theorem 4(v),(vi) incl. the $F_2$ side of (vi)(f)).
- Command: `python3 -I check_r2.py A`, giving partA_output.txt and partA_perclass.txt.
- Input lists: extracted afresh from experiments/prover/L012/cells.tar.gz; the four tight lists are byte-identical to the L013 tarball's.
- Graphs: the 13 tight Δ≤3 classes, with counts 1, 4, 2, 6.
- Method: τ by my own exact branch-and-bound decision procedure. Co-transversality by Fact 0.4 (τ(F−X) = τ − |X|), not by enumerating transversals.
- Result: every vertex is co-transversal. The non-co-transversal pairs are $E_1$: 3 of type (1,1,1), and (10,7,4): 4 of type (1,2,1), two each in classes 1 and 2. There are none in (14,12,6) or (17,13,7).
- Property (P) for the 12 classes with n ≥ 10, the pair lemma, and the (vi)(f) $F_2$-side conclusion: 0 failures.
- This matches 13.2 and C5 exactly.
- (A first run had a bug in my code, `has_cover` accepting k < 0 on an empty edge list. It was fixed before all reported runs.)

**Check B** (Theorem 4(iii)/(iv) and the Theorem 6(ii) converse for arbitrary extensions).
- Commands: `python3 -I check_r2.py B 3000 20261027` (partB_full_output.txt) and `SMALL=1 python3 -I check_r2.py B 3000 7` (partB_small_output.txt).
- Setup: G is a disjoint union of r ∈ {1,2,3} refereed class-C components, Δ≤3, all tight or exactly one of slack 1. The library is (3,1,1), (10,7,4), (14,12,6), (17,13,7), (8,5,3), (12,10,5), (15,11,6); SMALL restricts it to n ≤ 10.
- Extension: three random disjoint pairs of G-degree-1/2 vertices, no pair inside an edge, every component met.
- For each extension:
  - the pattern is classified;
  - the Theorem 4(iv) condition is evaluated on the components through Fact-0.4 co-transversality of pairs and triples;
  - it is compared with τ(H′) = τ(G)+1, computed directly on H′ by my branch-and-bound;
  - for non-deficient distributions, τ(H′) = τ(G) is required;
  - when (⋆) holds, s(H′) = s(G) − 2 is checked.
- Full run, 3,000 extensions, as [count, (⋆) true]: (a) 725/10, (b) 308/10, (c1) 258/0, (c2) 49/0, (d) 12/0, (e) 163/0, (f) 625/0, non-deficient r = 3: 860/0. 0 failures.
- SMALL run, 3,000 extensions: (a) 789/209, (b) 368/24, (c1) 206/0, (c2) 35/0, (d) 17/0, (e) 146/0, (f) 553/0, non-deficient 886/0. 0 failures.
- Every deficient r = 3 distribution was of type (d), as Theorem 4(iii) says.
- Both directions of the equivalence were exercised: 253 cases with (⋆) true, the rest false.

**Check C** (Chvátal–Hanson at Δ = 3, as quoted in Theorem 7 and 4.6(c)).
- Command: `for N in 1..11: geng -q -D3 N | python3 -I chk_ch.py`, giving chk_ch_output.txt.
- geng is the unmodified build in experiments/referee/L013-round2/out/nauty_build/; ν comes from networkx maximum-cardinality matching.
- Result: 16,335 graphs (the correct total for N ≤ 11). 0 violations of |E| ≤ 3ν+⌊ν/2⌋, and 0 violations of "11ν ≥ 3|E|, with equality only if |E| = 0". The bound is attained 17, 7, 31 and 2 times for ν = 1, 2, 3, 4.

**Check D** (citations).
- `pdftotext -layout kb/literature/papers/henning_yeo_ejc_2017.pdf`, then grep for Definition 5, Proposition 9 and Theorem 14; the excerpt is in hy/hy_ejc2017_excerpt.txt.
- grep for the Claims in kb/literature/sources/henning_yeo/henning_yeo_1802.01825_sec7_deficiency.txt.
- grep for Chvátal–Hanson in kb/literature/bibliography.md.

**Check E** (engine and C4).
- I read experiments/prover/L013/engine.py; `diff` against L012/engine.py gives no output.
- I read experiments/prover/L017/engine_decomps_output.txt, lines 21–27 and 60–75. I did not re-run C4; round-1 referees reproduced it.

**Check F** (13.1(ii) inputs). I read experiments/falsify/i11-structure-lemmas/REPORT.md (lines 17–18) and verified_tight_25_23_11_candidates.json: 4 graphs, filt summary "survivors_connected=4", Δ = 4, τ = 11. I read experiments/20261027-0400-realize-21-18-9/results_main_21_18_9.json: 12 classes, all `realizable: False`. I did not check these computations; the certificate marks them unrefereed.

**Not applicable.** `judge/judge.py` (no construction is claimed).

## Problems found (in order of severity)

No mathematical error, gap or misattribution was found. The following are optional editorial suggestions; none affects a theorem, a proof, or the honesty of the description, and none needs another round.

- **E1 (cosmetic tag consistency).** The Tags paragraph still says "Theorems 1–7 **[derived-here]**". The Theorem 7 statement and 4.6(c) now say "[published, re-proved here]". [derived-here] is not false for Theorem 7, since the proof is derived here from published theorems, and the text says clearly that the statement is known. Suggested wording for the next edit: "Theorems 1–6 [derived-here]; Theorem 7 known (a consequence of HY EJC 2017 Prop. 9 + Thm 14, or of Chvátal–Hanson), proof re-derived here".
- **E2 (wording of the no-circularity paragraph).** The paragraph says every use of I11 in Theorems 1–6 is for a proper induced subgraph of H, with the 1(g) exception. The new 9.2 parenthetical uses I11 for $F_i-x$. For an arbitrary extension H′ these are proper induced subgraphs of H′, not of H, and they are justified by the choice of N (fewer than N vertices). This is not circular, but the paragraph could mention "or a member of C with fewer than N vertices (Theorem 6)".
- **E3 (precision, 9.2).** Free choice is needed only for the direction (⋆) ⇒ (iv). The direction (iv) ⇒ (⋆), which is what "every such extension in C is a violator" uses, needs only 0.1: every "Conversely" clause in 7.4 is free-choice-free. The parenthetical is correct but stronger than needed.
- **E4 (implicit convention).** Theorem 2(R+)/(H) implicitly assume r ≥ 1. For r = 0, W = ∅, R = H is not proper, and the empty map exists. The "(W≠∅)" in 1.3 shows the intent.
- **E5 (paraphrase).** HY's class $\mathcal H_k$ has Δ = 2 exactly, while the certificate paraphrases Theorem 14 as "connected linear Δ≤2". This is harmless, because $E_1$ (Δ = 1) satisfies 18 ≤ 4·3+4·1+2 = 18, and 4.6(a) handles single edges anyway.

## Independence statement

- **What I read.** As instructed, I read the three round-1 reviews (20261027T045608Z, 20261027T050734Z, scout 20261027T050242Z) before checking the fixes. A further L017 referee review, 20261027T052541Z, appeared in results/reviews/ while I was working. I did not open it, and nothing in this review depends on it.
- **Code.** All verification code (experiments/referee/L017-round2-opus/check_r2.py, chk_ch.py) was written from scratch for this review. It imports nothing from e757/, judge/ or experiments/prover/. It uses only the Python standard library, plus networkx in chk_ch.py and the unmodified nauty `geng`.
- **Data and prover files.** The cell lists were extracted afresh from the refereed tarballs into my scratch folder. The prover's engine and C4 output were only read, not executed.
- **What I did not modify.** I did not modify the certificate, results/LEDGER.md, kb/, judge/, or anything outside experiments/referee/L017-round2-opus/ and this review file. (An automatic "exp: live scratch of running workers" commit, 2be94da, snapshotted an early version of my scratch file; I made no commits.)
