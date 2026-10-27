VERDICT: ACCEPT

Referee #5, round 3 (fix check only), of the PARTIAL certificate `results/proofs/L021-i11-deficiency-route.md` as revised in commit 2558405, which also edits `experiments/prover/L021/README.md`. I read the round-2 reviews first:
- `results/reviews/L021-i11-deficiency-route__referee__20261027T093649Z.md` (opus): NEEDS-WORK, meaning editorial items 1-4;
- `results/reviews/L021-i11-deficiency-route__referee__20261027T092532Z.md` (fable): ACCEPT, with two optional nits.

Scratch folder: `experiments/referee/L021-round3-ref5/`.

## Summary

Commit 2558405 applies every required round-2 item, and applies each correctly:
- the Step 8.4 (H$_1$) chain now ends "$\le|S|-2$", with an accurate parenthetical;
- the KT* remark names the three reused empty cells and the run they come from;
- the README says "closely related to" instead of "a consequence of";
- the DEPENDS line attributes the $\Delta\le2$ formula to L017 Theorem 7 = K65.

Fable's optional nit about the README's "unrefereed" is also applied. Its other optional nit ("We did the former") is not, which is acceptable for an optional stylistic point.

A word-level diff shows exactly seven word replacements, five in the certificate and two in the README, and nothing else. No definition, hypothesis, theorem statement or proof step changed beyond the one-symbol correction in Step 8.4 and its parenthetical. Both files are unchanged from 2558405 to HEAD and have no uncommitted changes.

I checked the corrected inequality by hand and by exact enumeration over all 446 pairs $(R,u)$, with $R$ ranging over the 32 stored pieces. It is exactly the (P3) bound that defines $C$, which is what (H$_1$) needs for $H'\in C_3$, and it holds for every $S\supseteq e'$. The old "$\le|S|-3$" fails at $S=e'$ and nowhere else.

The proved parts of the certificate stand as stated: Theorems 1-6, Propositions 8 and 9, and Theorem 7 as computations. The certificate remains PARTIAL with GAPs G1-G4 marked, and it claims no bound. The leftovers are all optional and cosmetic. None of them touches a statement or a proof (Section 4); the main one is the README's stale "Computations needed" item 2.

## 1. Item-by-item check (`git show 2558405`)

| # | Round-2 item | Applied? | Check |
|---|---|---|---|
| 1 | opus 1: Step 8.4 (H$_1$), "$e_{H'}(S)\le e_R(S\setminus\{z_1,z_2\})+1\le\lvert S\rvert-3$ for $S\supseteq e'$" is false at $S=e'$; replace with $\le\lvert S\rvert-2$ | Yes. It now reads "$\le\lvert S\rvert-2$ for $S\supseteq e'$ (only $\le\lvert S\rvert-2$ is needed; for $S=e'$ both sides equal $1$)" | Correct (Section 2). In 8.4 only the constant and the parenthetical changed (word diff, Section 3). |
| 2 | opus 2: the KT* remark omits the reused empty cells (26,13,9,3), (27,15,10,3), (27,16,10,3) | Yes. It adds "it reuses as empty the cells ... computed by another unrefereed run, experiments/20261027-0340-induction-n28-n29-f25" | Accurate (details below the table). The optional rewording of "untested for $n\ge28$" was not made; it was optional. |
| 3 | opus 3: README "a consequence of" should be "closely related to" | Yes (README line 19) | Correct. The disclaimer "not claimed as new; novelty left to the scout" is kept. |
| 4 | opus 4: the $\Delta\le2$ formula is L017 Theorem 7 = K65, not K64 | Yes. It now reads "[ACCEPTED, K64 for Theorems 1-6; the $\Delta\le2$ dual-graph formula is L017 Theorem 7, K65 (published, re-proved); ...]" | Matches the sources (details below the table). |
| 5 | fable nit 1: README line 3 "unrefereed" is stale | Yes. It now reads "under referee (round 2: fable ACCEPT, opus editorial items applied)" | Accurate. |
| 6 | fable nit 2: "We did the former" in 7.6 | No | Optional and stylistic. Step 7.6 is unchanged (Section 4). |

Details for item 2:
- experiments/20261027-0730-kt-cells/README.md lines 10 and 29 say these three cells were "reused from the 0340 folder".
- In experiments/20261027-0340-induction-n28-n29-f25/out/cells/, the files cell_26_13_9_D3.txt, cell_27_15_10_D3.txt and cell_27_16_10_D3.txt each hold only the INFO record, with `"connected_hits": 0` and no graph lines.
- No accepted certificate covers these cells. K66 and K70 use the 0340 lists only as a source of witness sets, and those sets were judged separately. So "unrefereed" is right.

Details for item 4:
- kb/known_results.md K64: "Theorems 1-6 ...; Theorem 7 is K65".
- K65: tag "published, re-proved here"; referee ACCEPT x2 (round 2) of the L017 re-proof; scout KNOWN.
- L017 line 87: Theorem 7 with "[published, re-proved here]". L017 Step 4.2 is its proof of $\tau(H)=m-\nu(G)$, which is what the DEPENDS line cites.

STATUS line. It appends "; round 2 (fable ACCEPT; opus NEEDS-WORK = one symbol in Step 8.4 and three wording items): applied 09:39 UTC". This matches the round-2 reviews (opus item 1 plus three wording items) and the commit time, 09:39:44 UTC.

## 2. The corrected Step 8.4 (H$_1$) inequality

Setting (Proposition 8, (H$_1$)):
- $\partial(X)=\{u\}$. The vertex $u\notin V(X)$ lies on an edge of $E^*(X)$, so $u\in V(R)$.
- $R=H-V(X)\in C_3$ by heredity (0.1).
- $e'=\{u,z_1,z_2\}$ with $z_1,z_2$ new, and $H'=R+e'$.

**By hand, for $S\supseteq e'$.** The only edge of $H'$ that contains $z_1$ or $z_2$ is $e'$. So the first inequality of the chain is in fact an equality: $e_{H'}(S)=e_R(S\setminus\{z_1,z_2\})+1$.
- If $|S|\ge4$: then $|S\setminus\{z_1,z_2\}|\ge2$, and (P3) for $R$ gives $e_{H'}(S)\le(|S|-4)+1=|S|-3$.
- If $S=e'$: then $e_R(\{u\})=0$, so $e_{H'}(e')=1=|e'|-2$. The parenthetical "both sides equal 1" is accurate, and the middle term is also 1.

Hence $e_{H'}(S)\le|S|-2$ for every $S\supseteq e'$.

**By hand, for $S\not\supseteq e'$.** The edges of $H'$ inside $S$ are edges of $R$, so $e_{H'}(S)=e_R(S\cap V(R))\le|S|-2$ whenever $|S|\ge2$. This was implicit in the text before the fix and is unchanged.

**Why this is exactly what (H$_1$) needs.** "$\le|S|-2$ for $|S|\ge2$" is precisely the (P3) condition in the definition of $C$ (certificate line 17). Together with the other three conditions it gives $H'\in C_3$:
- linearity;
- $F_7$-freeness: $z_1$ has degree 1 and $F_7$ has minimum degree 2;
- $\Delta(H')\le3$: $d_{H'}(u)\le d_H(u)$, because $u$ loses an edge of $E^*(X)$.

Nothing stronger is used afterwards:
- minimality applies because $n(H')+m(H')<n(H)+m(H)$;
- then $A(H')\ge-\mathrm{DEF}(H')\ge-16$ by 8.3;
- with $\nu=2$ and $|X|\ge4$ this gives $A(H)\ge19|X|-16-54\ge6>0$, contradicting (F).

The stronger bound "$\le|S|-3$", which was false at $S=e'$, was never needed. Proposition 8 and its proof stand as stated.

**By computation** (`h1_check.py`: my own code, standard library only, exact integers). For each of the 32 pieces $R$ in experiments/prover/L021/closure_results.json and each vertex $u$ of $R$, I enumerated all edge subsets and checked:
- (a) $R$ is linear and satisfies (P3);
- (b) $H'=R+\{u,z_1,z_2\}$ is linear and satisfies (P3) on all nonempty edge subsets;
- (c) $\max_{S\supseteq e'}(e_{H'}(S)-|S|)=-2$, attained only at $S=e'$.

Output: `pieces=32 (R,u) cases=446 failures=0 cases where max_(S>=e') e(S)-|S| = -2 attained only at S=e': 446` and `ALL OK`. So the corrected bound holds in all 446 cases, and the old bound fails exactly at $S=e'$ in every case, as the round-2 referee said. The test does not require $d_R(u)\le2$, so it checks a wider set of graphs than (H$_1$) needs.

## 3. Nothing else changed

- **Word-level diff.** `git show 2558405 --word-diff=plain -- <certificate> <README>` was saved to experiments/referee/L021-round3-ref5/worddiff.txt and parsed. It contains exactly seven replacements:
  1. README: "unrefereed;" becomes "under referee (...)".
  2. README: "a consequence of" becomes "closely related to".
  3. STATUS: the round-2 note is appended.
  4. DEPENDS: "K64;" becomes "K64 for Theorems 1-6; ... K65 (published, re-proved);".
  5. KT* remark: "unrefereed])" becomes "unrefereed]; it reuses as empty the cells ... experiments/20261027-0340-induction-n28-n29-f25)".
  6. Step 8.4: "$\le|S|-3$" becomes "$\le|S|-2$".
  7. Step 8.4: "$e'$;" becomes "$e'$ (only $\le|S|-2$ is needed; for $S=e'$ both sides equal $1$);".

  Everything else is untouched: the title, CLAIM-TYPE, the Statement section, Theorems 1-7, Propositions 8-9, Conjecture KT*, Steps 0-7, 8.1-8.3 and 9, the GAP list and the sanity checks.
- **No later or uncommitted edits.** `git log` on both files shows 2558405 as the latest commit, directly after 22e95c9, the version both round-2 referees reviewed. `git diff 2558405 HEAD` on both files is empty, and `git status` is clean. So, apart from the seven replacements, the text is identical to the version reviewed in round 2.
- **Bundled L026 edits.** The commit also changes four files of a different certificate, L026: experiments/prover/L026/{README.md, hubtriangle_check.py, hubtriangle_check_output.txt} and results/proofs/L026-e1hub-lemma-kt-form.md. Neither L021 file mentions L026 (grep count 0), and L021 does not depend on it. Those edits cannot affect L021, and I did not review them.

## 4. Residual observations (optional and non-blocking; none touches a statement, proof step, tag or dependency of the certificate)

1. **Stale README to-do item.** In experiments/prover/L021/README.md, "Computations needed" item 2 (lines 66-68) still lists the cells (25,14,9,3), (26,13,9,3), (26,17,10,3), (27,13,9,3), (27,15,10,3), (27,16,10,3), (27,20,11,3) as "not yet stored".
   - The unrefereed run experiments/20261027-0730-kt-cells has since computed four of them and reused the other three, as the certificate's KT* remark now says.
   - Opus round 2 flagged this as a side remark in its item 3 ("Also, ... item 2 is stale"), and it was not updated.
   - Suggested wording: "done by the unrefereed run experiments/20261027-0730-kt-cells (n <= 27); a refereed certificate of these cells is still needed".
   - This is a planning note in the work folder, not part of the certificate.
2. **Step 7.6 wording.** Fable's nit "We did the former" and the opus remark on the word "so" remain. Both are stylistic; the "so" can also be read correctly, as "so [this graph] ... has I11 slack $s(F_1)-2<0$".
3. **STATUS line.** It contains a stray ".;" ("Folder: experiments/prover/L021/.; round 2 ..."), and it gives "revised 09:10 UTC" for a commit made at 09:08:40. Both are immaterial.

## 5. Commands and outputs

- `git show --stat 2558405`: 6 files, 2 of them L021 files.
- `git show 2558405 -- results/proofs/L021-i11-deficiency-route.md experiments/prover/L021/README.md`: read in full. The word-diff version is in worddiff.txt, with the seven replacements listed in Section 3.
- `git log --oneline -- <both files>`: 2558405, then 22e95c9. `git diff 2558405 HEAD --stat -- <both files>`: empty. `git status --short -- <both files>`: clean.
- `grep -n` on kb/known_results.md (K64, K65) and on results/proofs/L017-i11-minimal-counterexample-structure.md (Theorem 7, Step 4.2): as quoted in Section 1.
- `grep` on experiments/20261027-0730-kt-cells/README.md: lines 10 and 29 ("reused from the 0340 folder", "Reused empty").
- `grep -o '"connected_hits": [0-9]*'` on the three cell files of experiments/20261027-0340-induction-n28-n29-f25/out/cells/: 0, 0, 0, with no graph lines.
- `grep -n 20261027-0340` on kb/known_results.md and results/LEDGER.md: only K66/K70 (witness sources).
- `timeout 600 nice -n 10 python3 -I h1_check.py experiments/prover/L021/closure_results.json`, output in experiments/referee/L021-round3-ref5/h1_check_output.txt: `ALL OK`, in a few seconds.

## 6. Independence statement

- **What I read.** The two round-2 reviews, as instructed. I took the round-1 items only from their summaries there.
- **What I re-derived.** Every check in this review, from the diff, the certificate text and the cited sources (kb/known_results.md, L017, the kt-cells and 0340 folders). I did not take any of these checks on trust from the earlier reviews.
- **My code.** h1_check.py uses only the Python standard library and imports nothing from e757/, judge/, experiments/prover/L021/ or any referee folder. It reads only the edge lists of the 32 pieces in closure_results.json and re-checks that they are linear and satisfy (P3).
- **What I did not do.** This round was scoped as a fix check, so I did not re-verify the unchanged steps independently. Their correctness rests on the round-1 and round-2 reviews, each with independent code, and their text is identical to the version those reviews accepted.
- **Files written.** Only this review and the scratch folder experiments/referee/L021-round3-ref5/ (h1_check.py, h1_check_output.txt, worddiff.txt). Nothing else was modified.

Review by referee #5 (round 3), claude-opus-5-5.
