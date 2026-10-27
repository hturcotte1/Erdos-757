VERDICT: NEEDS-WORK

In the commissioning workflow's vocabulary this is **ACCEPT WITH FIXES**. My referee format allows only ACCEPT, NEEDS-WORK or REJECT, and it reserves ACCEPT for a document in which no problem remains. Everything presented as proved is correct, and the round-1 edits changed no theorem statement or proof step. Some editorial fixes remain, one of them about the honesty of the evidence record.

# Referee #3 (opus), round 2: results/proofs/L019-triple-coverage-C1.md (revision 9ee8a20)

Scratch folder: experiments/referee/L019-round2-opus/. All runs used `nice -n 10`, one process at a time, under `timeout`. Load average was about 12 on 4 cores.

## Summary

I read the three round-1 reports:
- opus NEEDS-WORK, 20261027T065058Z;
- fable ACCEPT WITH FIXES, 20261027T060439Z;
- scout PARTIAL, 20261027T061122Z.

**The edits are editorial.** I compared the certificate before fda23fa with the version at 9ee8a20 token by token (`sentdiff.py`, output `diff_report.txt`). Only the following changed:
- the STATUS line and the DEPENDS ON tags;
- one sentence appended after the statement of Conjecture C1;
- a definition of "triple-rich" in the Consequences paragraph of Theorem 2;
- tag sentences in Proposition 9 and Remark 9.2;
- a new provenance paragraph;
- the inequality wording of step 10.2;
- [heuristic] tags in GAP 1 and GAP 2;
- remark-level corrections ("On the data", C2, C7, C8, one sanity check).

The statements of Theorems 1–6, Lemmas 7 and 11 and Propositions 8–10 are unchanged. The only proof-text change is step 10.2, and it corrects a mis-stated side condition without changing the conclusion.

**Applied correctly** (each checked by hand, the data claims also by my own code):
- the new L017 tags and the flags on the unrefereed L017 Corollaries 13.3(iii) and 13.5(i);
- the restricted-form sentence;
- step 10.2;
- the definition of triple-rich;
- the [heuristic] tags;
- the corrections in "On the data", C2 and C7;
- the sanity-check rephrasing;
- the regenerated C8 line.

**Spot checks of two unedited theorems.** For Theorem 5 (folding lemma) and Theorem 3 (pair-pair coverage) I re-derived the exact slack change and the class-C criterion by hand. I then tested them with code written for this review. That code shares no code with the prover or the round-1 referees.
- Theorem 5: 5,836 folds on stored class-C graphs, AP hypergraphs of real (4,5)-sets and random linear 3-graphs. 0 failures.
- Theorem 3, together with Theorem 4(a),(d) and Lemma 7: tested in the hereditary class L′ (linear and F7-free), where the setting of C1 is non-empty. 0 failures.

**Remaining problems.**
1. The new C8 evidence note, reproduce.log and the reproduce.sh comment state as fact a cause for the missing (26,22,11) line: the 1800 s timeout was exceeded, timeout returned status 124, and `set -e` aborted the script "before the final `exit 0`". The repository's own git record contradicts this.
2. One round-1 fix that both referees requested was not applied: the GAP section still calls L017 Theorems 1–5 "unrefereed".
3. Two smaller tag and provenance points.

All are fixable without touching the mathematics.

## 1. Item-by-item check of the round-1 requests

The commands are `git show fda23fa 2f5b7e8 9ee8a20 -- results/proofs/L019-triple-coverage-C1.md experiments/prover/L019/` and `python3 sentdiff.py L019_before.md L019_after.md`. The working copy of the certificate is byte-identical to 9ee8a20 (`cmp`).

| # | Request (source) | Status |
|---|---|---|
| 1 | Complete the C8 evidence file for (26,22,11) (opus 1, fable 1) | **Applied.** `nbhd_cover_output.txt` now has `cell_26_22_11.txt (k, tau of edges meeting N[v]) : count {(6, 4): 144}`. Its format is exactly the `print` of nbhd_cover.py line 22. The whole file is byte-identical to the fable round-1 rerun copy experiments/referee/L019-round1-fable/repro/nbhd_cover_output.txt (`diff` empty). It agrees with the independent opus c8_check.py output (`144 ... {(6, 4): 144}`). |
| 1′ | Correct reproduce.log (opus 1: "refresh after a complete run"; fable 1) | **Rewritten, but the narrative of the original run is not supported by the record**; see Problem 1. No complete run of the current reproduce.sh is recorded; only the single C8 step was re-run (06:54:23–06:59:17 UTC, documented). |
| 2a | Update the L017 tags to refereed (opus 2, fable 2) | **Applied in DEPENDS ON**: "[verified-here: Theorems 1-6, ACCEPTED, K64; Theorem 7 published (re-proved there); ...]". This matches kb/known_results.md K64/K65 and LEDGER line 39. **Not applied in the GAP section**: line 186 still reads "all of L017 Theorems 1–5 (unrefereed)". Both referees named this phrase explicitly. See Problem 2. |
| 2b | Flag L017 Corollaries 13.3(iii) and 13.5(i) as unrefereed (opus 2, fable 4) | **Applied**, in four places: DEPENDS ON ("[both unrefereed computations]"), the parenthetical of Proposition 9, Remark 9.2, and GAP 2 ("an unrefereed computation there"). L017's own Tags line (its line 89) and the K64 Check column agree. |
| 3 | Label the restricted form of C1 (opus 3) | **Applied, accurate.** The source statement (experiments/20261027-0300-transversal-richness/README.md, line 157: "(C1) If F in C has slack <= 1 and v extends F inside C ...") has neither "F connected" nor "I11 below n_F". The new sentence says so and correctly notes that a proof of the restricted form does not prove the source conjecture. |
| 4(i) | "On the data": restrict to slack ≤ 1 (opus) | **Applied** ("with slack at most 1"; "for the slack-2 cells this is false"). |
| 4(ii) | Tag the GAP 1 and GAP 2 judgements as heuristic (opus) | **Applied** ("[heuristic] ... a judgement, not a theorem"). |
| 4(iii) | Rephrase the (6,3,2) sanity check (opus) | **Applied, correct.** In the class L of all linear 3-graphs, I11 holds up to N = 6. The 6-vertex K = (6,3,2) has s = 2. The gadget F7 lies in L. So Theorem 2(ii) at k = 2 cannot be relaxed to s ≤ 2 in L. |
| 4(iv) | C7 cell count (opus) | **Applied, verified.** The inputs folder has 19 cells, all of slack 0, 1 or 2 (I computed 3n+2m−11τ for each). The loop runs 17 of them and skips (3,1,1) and (23,21,10). My `c7_23.py`: all 699 classes of (23,21,10) have a vertex of degree ≥ 4 (and one of degree ≤ 1). (3,1,1) has degrees 1. |
| 5(i) | Step 10.2 wording (opus 5(i), fable 3) | **Applied, correct**; see Section 3. |
| 5(ii), 5(iii) | Harmonise naming; check_folding.py docstring (opus, optional) | Not applied (optional). The README (line 5) still lists "Theorems 1-6, Lemma 7, Propositions 8, 9". check_folding.py still says "random connected". Cosmetic. |
| F5 | Define "triple-rich"; record that the bound \|S\| ≥ 6 is attained (fable 5) | **Applied.** The definition matches Theorem 2(iii) with k = 3, n(K) = N, s(K) ≤ 1 = 7−6. The C2 addition is verified by my run: in (10,8,4), minimal blocking saturated sets of size 6 occur (3 folds) and of size 7 (16 folds). |
| S1 | Credit Chen–Kanj–Jia for the graph fold (scout) | **Applied** (J. Algorithms 41 (2001) 280–301; arXiv:1312.6260, arXiv:1708.06151). The scout's further recommendation was not adopted: to say that the novelty of the 3-uniform form and of 5(d)–(e) was checked only against the sources listed, the Henning–Yeo 2021 full text being unobtainable. See Problem 4. |
| S2 | Theorems 2–3 are standard bookkeeping (scout) | **Applied** ("standard minimal-counterexample potential bookkeeping (Thomassé-Yeo; Henning-Yeo arXiv:1802.01825, Claim B) ... not new methods"). Claim B is at kb/literature/sources/henning_yeo/henning_yeo_1802.01825_sec7_deficiency.txt line 204. It is a delete-and-cover potential argument of exactly this type. |

Evidence files:
- reproduce.sh line 32 now reads `timeout 5400` (verified).
- The README timing was corrected to "about 5-30 minutes" for the (26,22,11) run.

## 2. Regenerated evidence and the honesty of reproduce.log (Problem 1 in detail)

The revised reproduce.log, line 1, says:

> the steps C1-C7 and the first three C8 runs completed; the fourth C8 run (cell_26_22_11) exceeded the old 1800 s timeout (timeout exit status 124) and `set -e` aborted the script before the final `exit 0`.

The certificate's C8 note and the reproduce.sh comment (line 30, "the (26,22,11) run takes about an hour; the original 1800 s timeout aborted it under set -e") repeat this. The repository record contradicts it:

- **No version of reproduce.sh has an `exit` statement.** Checked at 02d63ff, 1664a25, 9f85da0, fda23fa and HEAD; `grep -c -w exit` gives 0 in each. So there was no "final `exit 0`" for `set -e` to skip. The old log line "exit 0" was written by an external wrapper.
- **The old log belonged to an earlier, smaller script.** The "exit 0" log was committed in 02d63ff (05:22:52 UTC) together with a 24-line reproduce.sh that contained only C1–C6. C7 and C8 were added to the script later, in 1664a25 (05:30:25) and 9f85da0 (05:43:22). The old log was therefore stale, not a record of a run that included C8.
- **The 1800 s timeout cannot have fired before submission.** nbhd_cover_output.txt had 2 lines in 1664a25 (05:30:25) and 3 lines in 4a1c71e (05:34:38). The certificate was committed with 3 lines in 9f85da0 (05:43:22). So the fourth C8 run had been running for at most about 13 minutes when the certificate was submitted.
- **Every recorded completed run of that step finished well within 1800 s.**
  - the prover's own re-run took 4 min 54 s;
  - the opus round-1 C8 loop, run under the 1800 s script, finished all four cells in 503 s: experiments/referee/L019-round1-opus/rerun_full/c8_loop.log, "rc=0 elapsed 503";
  - the fable round-1 rerun copy has all four lines (repro/nbhd_cover_output.txt, 06:02), and its repro.log records "real 8m15.013s".

  Fable's round-1 README also mentions an attempt that was "stopped manually", which is not a timeout. No record anywhere shows a 124 exit status. The "about an hour" in the reproduce.sh comment contradicts both the README ("5-30 minutes") and the measured 5 minutes.

What the record does support: the certificate and its outputs were committed while the fourth C8 run had not yet produced its line. Why it never produced it is not recorded.

None of this affects the mathematics: C8 is illustrative, and its (26,22,11) value is now confirmed by three implementations. But the purpose of this revision was to make the evidence trail honest, and it replaced one unsupported statement ("exit 0") with another, more specific one.

**Fix.**
1. Replace the causal story in the C8 note, in reproduce.log lines 1–2 and in the reproduce.sh comment with the recorded facts: the old log came from the C1–C6 script; the certificate was committed before the fourth C8 run had written its line; the cause is not recorded.
2. Keep the documented single-step re-run.
3. Drop "about an hour" (and "evidently slowed by machine load", which is a guess).

## 3. Edited passages re-verified by hand

- **DEPENDS ON, L017.** Matches K64 (Theorems 1–6 verified-here, referee ACCEPT x2 in round 2; Corollaries 13.3/13.5 and Remarks 13.2/13.4/13.6 excluded as unrefereed computations) and K65 (Theorem 7 published, re-proved). "L017 Theorem 5(A)(iv) [verified-here, ACCEPTED]" is correct, since it is part of Theorem 5.
- **Proposition 9 parenthetical and Remark 9.2.** Both conclusions rest on unrefereed L017 computations, and the text now says so:
  - "no vertex of degree 1 under T3" is L017 13.5(i): a degree-1 vertex forces a connected tight Δ ≤ 3 member of C with n−2 ≥ 26 vertices, which T3 (≤ 24) forbids;
  - "s = −1 under T3" is L017 13.3(iii) / 13.1 Relevance (i).

  The proof of Proposition 9 itself (9.1) uses neither: it uses L016, Theorem 5(a),(c) and Theorem 1. I re-checked that n(H°) ≥ 26, H° is connected, Δ(H°) ≤ 3 and s(H°) = 0, so T3 applies.
- **GAP 2, conditional closure.** If C1 failed for a tight F, then F would be connected (by hypothesis), tight, with Δ(F) ≤ Δ(H) = 3 (Theorem 1) and n_F ≥ 27 (Theorem 4(c)). T3 forbids this. The argument is self-contained; the attribution "the argument of L017 Corollary 13.3(iii), an unrefereed computation there" is accurate.
- **Restricted-form sentence.** Correct; see item 3 of the table.
- **Step 10.2.** |Z| = 7, since the three disjoint pairs and v are distinct. |∂_H(Z)| = 3+k: an edge meeting Z either contains v or is an edge of H−v meeting W.
  - (Red) holds for any minimal counterexample. Its proof uses only that T_R ∪ T is a transversal of H, the identity 0.5, and s(H−Z) ≥ 0 for H−Z ∈ C with fewer vertices; nothing about s = −2.
  - (Red) gives 0 ≤ s + 11|T| − 21 − 2(3+k), i.e. 11|T| ≥ 27 + 2k − s ≥ 28 + 2k when s ≤ −1, which holds by Theorem 1.
  - k ≥ 3 gives 11|T| ≥ 34, so |T| ≥ 4. k ≥ 9 gives 46 > 44, so |T| ≥ 5. s = −2 with k ≥ 8 gives 27 + 16 + 2 = 45 > 44, so |T| ≥ 5.
  - The old "s(H) ≥ −2" was a reversed side condition. The new "s(H) ≤ −1" is what the inequality uses.
- **Triple-rich.** For d_H(y) = 3: K = H−y has n−1 = N vertices and s(K) = s(H)+2 ≤ 1 = 7 − 2·3. Theorem 2(iii) needs Δ(K⁺) ≥ 4, which is the "degree-4 witness". Correct.
- **Attributions.** Chen–Kanj–Jia, "Vertex cover: further observations and further improvements", J. Algorithms 41 (2001) 280–301, is the standard source of degree-2 vertex folding. The arXiv pointers are those the scout actually read. Thomassé–Yeo is cited without bibliographic data; it is Combinatorica 27 (2007) 473–487 in kb/literature/bibliography.md (optional fix).

## 4. Adversarial spot checks of two unedited theorems

### Theorem 5 (folding lemma), by hand

**Size and slack.** Linearity makes x, u, u′, w, w′ distinct. Since y and z are non-adjacent, no edge of K−x contains both, so every image φ(g) is a 3-set. Two edges with equal images would have to be an edge through y and an edge through z sharing two further vertices, which contradicts linearity. So:
- m(K°) = m − 2 exactly, and n(K°) = n − 2;
- d(ζ) = d(y) + d(z) − 2, and every other degree equals its degree in K−x.

If x ∈ T ∈ 𝒯(K), then φ(T∖{x}) covers K° with at most τ − 1 vertices. Together with the lift (b), this gives τ(K°) = τ − 1 and s(K°) = 3(n−2) + 2(m−2) − 11(τ−1) = s + 1.

**Class-C criterion.**
- *Linearity.* Two image edges sharing two vertices must share ζ and a vertex t ∉ {y, z}, one edge coming through y and the other through z. Then t is a common neighbour of y and z in K−x. The co-vertices u′ and w′ cannot play this role: u′ is adjacent to y = u only through the deleted edge {x,u,u′}. The converse direction uses injectivity on edges.
- *F7.* An F7 avoiding ζ consists of edges g ⊆ V(K)∖{x,y,z} and is therefore already in K.
- *(P3).* For S° ∋ ζ, let S = φ⁻¹(S°). Then e_{K°}(S°) = e_{K−x}(S) = e_K(S), because no edge inside S contains x. Since e_K(S) ≤ |S| − 2 always, (P3) fails at S° iff S is saturated. Sets S° ∌ ζ inherit (P3) from K.
- *|S| ≥ 6.* |S| = 3 would make S an edge through y and z; |S| = 4 needs two edges in four points; |S| = 5 needs three edges of a linear 3-graph in five points, which is impossible.

All correct.

### Theorem 5, by computation (`spot_thm5.py`, library `ref2.py`)

`ref2.py` computes transversals by brute force over vertex combinations. It finds F7 copies by brute force over 5-edge subsets, using the characterisation "7 vertices, pairwise intersections ≤ 1, degree multiset 3,2⁶", which I proved in my notes: the centre's three edges partition the other six vertices, and each of the two remaining edges takes one vertex from each. It checks (P3) by a zeta transform over all subsets.

`selftest2.py` output:
- F7: 1 copy, τ = 3, s = −2;
- AG(2,3): 36 F7 copies, which is the predicted number, one per point pair;
- Fano: 0 copies;
- 300 random linear graphs: 0 mismatches of τ and (P3) against a second, recursive implementation.

Results (every FAIL counter covers parts (a), (b), (c), the linearity iff, "F7 ∋ ζ", the (P3) iff and |S| ≥ 6):

- `spot_thm5.py cells`: all classes of (8,5,3), (10,7,4), (10,8,4), (14,12,6), (17,13,7), the first 40 of (12,10,5) and the first 30 of (13,9,5).
  - Stored τ re-confirmed for every graph; 157 graphs, all in C.
  - 2,910 folds, all at co-transversal x. **0 failures.**
  - Folds in C: (14,12,6) 62 of 165, which agrees with fable round 1.
  - P3-blocked folds: (14,12,6) 8, minimal size 9; (12,10,5) 2, sizes 8 and 9. Both agree with the prover's C2 output.
- `spot_thm5.py ap`: AP hypergraphs of (4,5)-sets, every set first re-checked as a (4,5)-set by brute force over 4-subsets and its AP hypergraph verified to lie in C.
  - Sets: the records for n = 8, 10, 11, 12 (three sets) and 14 (A_base); Fibonacci {2,3,5,…,233}; the generic gluing of the 8-point record with 1000003·(10-point record) + 10¹²; and 134 random induced subsets of A_base with an AP.
  - 143 graphs, 1,428 folds (37 at non-co-transversal x, where τ(K°) − τ ∈ {0, −1}). **0 failures.**
- `spot_thm5.py random 300 31`: 300 random linear 3-graphs on 7–12 vertices, 139 of them in C.
  - 1,498 folds, 196 at non-co-transversal x (Δτ ∈ {0, −1}).
  - Minimal blocking saturated sets of size 6 occur. **0 failures.**

### Theorem 3, by hand

F + v(P_i, P_j) has vertex set V(F) ∪ {v} and edges E(F) plus the two edges at v. That is H with the edge {v} ∪ P_k deleted, so it lies in C by edge-heredity. With N = n_F, the hypothesis of the setting is exactly the hypothesis of Theorem 2.

If no minimum transversal of F met P_i and P_j, 0.7 would give τ(K⁺) = τ(F) + 1 and s(K⁺) = s(F) + 3 + 4 − 11 ≤ −3 on n_F + 1 vertices. But Theorem 1 at N + 1 bounds every negative slack below by −2: a degree-3 vertex x has s(K⁺ − x) = s + 8 − 6 ≥ 0, and the case Δ ≤ 2 is excluded by 0.8. Neither connectivity nor the third pair is used. Correct.

### Theorem 3, by computation (`spot_thm3.py`)

Inside C the setting of C1 has no instance with n_F ≤ 26 at which C1 fails, by L016. So I tested the same proofs in the hereditary class L′ = {linear, F7-free}. The proofs of Theorems 1–4 and Lemma 7 use only heredity, linearity and 0.8, so they hold in L′ verbatim with N = 8. I11 holding in L′ up to 8 vertices is taken from the round-1 opus enumeration; I did not repeat it.

- **Part A (violators).** Random search found 771 labelled violators on 9 vertices in 2 invariant classes, both (9,8,4) with s = −1 and degrees 2³3⁶. This is consistent with Theorem 1's prediction Δ = 3, s ∈ {−1, −2}. No 8-line subset of AG(2,3) is an F7-free violator.
- **Part B (the setting).** 12 instances: each degree-3 vertex v of each class has H−v connected. In every instance:
  - s(F) = 1;
  - no minimum transversal of F meets all three pairs (Theorem 4(a));
  - τ(H) = τ(F) + 1 and s(H) = s(F) − 2;
  - every 𝒯_ij is non-empty (**Theorem 3**) and disjoint from P_k (Theorem 4(d));
  - Lemma 7 holds in all 124 instances.

  **0 failures.**
- **Part C (Theorem 2(ii) at k = 2 directly).** 1,763 sampled F in L′ with 8 vertices and slack ≤ 1 (2 invariant classes), giving 66,865 gadgets F + w(Q₁, Q₂) in L′. Each has a minimum transversal meeting Q₁ and Q₂. **0 failures.**

## 5. Remaining problems (in order of severity; none affects a proved statement)

1. **The C8 evidence narrative is contradicted by the record** (Section 2). It appears in the certificate's C8 evidence note, reproduce.log lines 1–2 and the reproduce.sh line-30 comment. Fix as described in Section 2. Required: the revision was meant to make the evidence trail honest, and project rule 7 forbids stating unrecorded facts.
2. **A requested round-1 fix was not applied.** Line 186 (GAP section) still says "all of L017 Theorems 1–5 (unrefereed)". Both round-1 referees asked for this phrase to be updated. It should read "(refereed, K64)" or similar. Required; trivial.
3. **Stale L018 tag.** DEPENDS ON says "L018 Theorem 6(b′) [derived-here, unrefereed]". L018 was accepted at 06:37:40 UTC (commit ba02f13, K67), before this revision (06:55), and K67 lists Theorem 6(b′) among the accepted proved parts. It should be [verified-here, ACCEPTED, K67]. It is cited for comparison in Remark 3.2 only. Round 1 did not raise this, because at fable's review time L018 was not yet accepted. Required for tag accuracy; trivial.
4. **The novelty phrasing is firmer than the scout's evidence.** "New here is only the 3-uniform linear form ... and the class-C criterion" should carry the scout's caveat: "not found in the sources checked (scout, round 1; the Henning–Yeo 2021 full text was unobtainable)". Minor.
5. **Optional and cosmetic.**
   - The README (line 5) names "Theorems 1-6, Lemma 7, Propositions 8, 9" (Proposition 10 and Lemma 11 are missing; opus 5(ii)).
   - The check_folding.py docstring says "random connected" (opus 5(iii)).
   - Thomassé–Yeo is cited without bibliographic data.

## Independence statement

I read the three round-1 reports, as this round requires. To investigate Problem 1, I opened the round-1 referees' run logs and output files read-only (experiments/referee/L019-round1-opus/rerun_full/c8_loop.log; experiments/referee/L019-round1-fable/repro/repro.log, repro/nbhd_cover_output.txt, README.md). I used none of their code.

All verification code in experiments/referee/L019-round2-opus/ was written for this review:
- the library ref2.py;
- selftest2.py, spot_thm5.py, spot_thm3.py and c7_23.py;
- sentdiff.py, for the diff.

It imports nothing from e757/, judge/, experiments/prover/L019/ (hg.py), experiments/20261027-0300-transversal-richness/pyverify.py or the round-1 referee folders. The only shared inputs are the stored class lists in experiments/20261027-0300-transversal-richness/inputs/, whose stated τ my code re-confirmed for every graph it used, and data/small_records.json, whose sets my code re-checked as (4,5)-sets.

I did not re-run the prover's 26-vertex C8 step, because the machine load was about 12 on 4 cores. Instead, the regenerated line is byte-identical to fable's independent rerun and agrees with opus's independent implementation.

I modified no file outside my scratch folder and this review.
