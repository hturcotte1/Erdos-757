VERDICT: NEEDS-WORK

In the commissioning workflow's vocabulary this is **ACCEPT WITH FIXES**. My referee format allows only ACCEPT, NEEDS-WORK or REJECT, and it reserves ACCEPT for a document in which no problem remains. scripts/status.py tests for the exact string `VERDICT: ACCEPT`. The remaining fixes are editorial: two required, one recommended, one cosmetic (listed at the end). None of them touches a theorem statement or a proof step.

# Referee #5 (opus), round 3 (fix check only): results/proofs/L019-triple-coverage-C1.md at commit 76c2322

## Summary

Commit 76c2322 applies four of the five round-2 items correctly:
- (1) the L018 Theorem 6(b′) tag;
- (2) the L017 Theorems 1–5 tag in the GAP section;
- (3) the scout's novelty caveat;
- (5) the round-2 STATUS record.

It changes nothing else: four lines of the certificate (STATUS, one DEPENDS ON bullet, the provenance paragraph and the first GAP paragraph), lines 1–2 of reproduce.log, and one comment line of reproduce.sh. No theorem statement, proof step, GAP 1/GAP 2 statement or computation command was touched.

Item (4) is only **partly** applied:
- reproduce.sh and the first line of reproduce.log now state the record correctly.
- The certificate's own C8 evidence note (line 201) was not edited. It is byte-identical to the round-1 version (fda23fa). It still says that the (26,22,11) line was missing "because the original `reproduce.sh` gave each C8 run 1800 s and the $(26,22,11)$ run exceeded it (the script aborted there under `set -e`; …)". That is exactly the explanation that reproduce.log now calls "a reconstruction … withdrawn", so the certificate now contradicts its own evidence log.
- reproduce.log still contains the guess "the original run was evidently slowed by machine load". The opus round-2 review explicitly asked for it to be dropped, and it contradicts that log's own "The cause is NOT recorded".

The mathematics has not changed since round 2. There, both referees verified the proved parts and found nothing wrong. So the proved parts can be accepted as stated, with GAPs 1–2 and the PARTIAL status, once the fixes below are made.

## Checks performed (commands and outputs)

- `git log --oneline -8`: HEAD = 76c2322. `git show --stat 76c2322`: exactly 3 files: experiments/prover/L019/reproduce.log (3 +−), reproduce.sh (2 +−), results/proofs/L019-triple-coverage-C1.md (8 +−).
- `git diff -U0 9ee8a20 76c2322 -- results/proofs/L019-triple-coverage-C1.md | grep '^@@'`: hunks only at lines 4 (STATUS), 8 (DEPENDS ON, L018 bullet), 76 (Provenance and novelty) and 186 (GAP, first paragraph).
- `git diff --word-diff=porcelain 9ee8a20 76c2322 -- results/proofs/L019-triple-coverage-C1.md`: the only changed tokens are:
  - `them.` → `them.; revised again 07:26 UTC after round 2 (…)`;
  - `[derived-here, unrefereed]:` → `[verified-here: ACCEPTED, K67]:`;
  - the inserted caveat `(as far as the scout could check; the Henning–Yeo 2021 full text was unobtainable, so overlap with its internals cannot be excluded)`;
  - `(unrefereed);` → `[verified-here: ACCEPTED, K64];`.
- The range 9ee8a20..76c2322 contains five other commits (f09fcad, 64396c8, 7d7c60f, c9fd4bc, 436ad53). None of them touches an L019 file: the range diff restricted to L019 files equals the 76c2322 diff. `git status --short` on the certificate and on experiments/prover/L019/ is empty.
- The reproduce.sh diff: only line 30, a comment, changed. Every command line is unchanged, including the C8 `timeout 5400`.

### Item (1): DEPENDS ON, L018 Theorem 6(b′). APPLIED.
- Line 8 now reads "L018 Theorem 6(b′) [verified-here: ACCEPTED, K67]: cited for comparison in Remark 3.2 only".
- Checked against:
  - kb/known_results.md line 78 (K67), whose "Accepted as proved:" list includes "Theorem 6(b') (gadget lemma: … $H-v$ has at most TWO components …)";
  - results/LEDGER.md line 41 (K67/L018);
  - the STATUS line of results/proofs/L018-red-universality.md ("ACCEPTED 2026-10-27 as a PARTIAL certificate").

### Item (2): GAP section, L017 Theorems 1–5. APPLIED.
- Line 186 now reads "all of L017 Theorems 1–5 [verified-here: ACCEPTED, K64]". `grep 'Theorems 1–5 (unrefereed)'` finds nothing.
- K64 (kb/known_results.md line 75) is "verified-here (Theorems 1-6)", consistent with LEDGER line 39 and the L017 STATUS line ("ACCEPTED 2026-10-27").
- No stale L017/L018 tag remains. The remaining "unrefereed" occurrences (lines 6, 10, 68, 74, 171, 190) are all correct:
  - L017 Corollaries 13.3(iii) and 13.5(i) are unrefereed computations;
  - the transversal-richness analysis is unrefereed;
  - L019's own theorems are still under review.

### Item (3): novelty caveat. APPLIED.
- The caveat on line 76 matches the scout's review, results/reviews/L019-triple-coverage-C1__scout__20261027T061122Z.md:
  - line 43: "Henning-Yeo 2021: full text still NOT obtainable, so overlap with its internals cannot be excluded";
  - line 51: "checked only against the sources listed, not against the unobtainable Henning-Yeo 2021 text".

### Item (4): evidence narrative. PARTLY APPLIED.
- **reproduce.sh: APPLIED.** The line-30 comment is now "C8 timeout raised to 5400 s after round 1; recorded completed runs of the (26,22,11) step took 5 to 8.5 minutes". There is no "about an hour" and no `set -e` story. For the precision of "5 to 8.5 minutes", see F3.
- **reproduce.log, line 1: APPLIED in substance.** It says that the cause is NOT recorded, that the earlier 'exit 0' log predates nbhd_cover.py, and that the timeout explanation is withdrawn. It does not mention exit 124. I verified the timeline with `git log --date=iso-strict-local`:
  - the 'exit 0' log was committed in 02d63ff at 05:22:52 UTC;
  - `git show 02d63ff:experiments/prover/L019/reproduce.sh` has 24 lines and 0 mentions of nbhd_cover;
  - nbhd_cover.py first appears in 1664a25 at 05:30:25 (file mtime 05:29:54);
  - nbhd_cover_output.txt had its 2nd and 3rd lines committed in 1664a25 (05:30:25) and 4a1c71e (05:34:38), and its 4th line in 2f5b7e8 (07:05:32).
- **reproduce.log, lines 4–6: re-run record present, but a guess retained.**
  - Present: the re-run "started 06:54:23 … finished 06:59:17 … exit status 0", and the result "(6, 4): 144, matching the certificate and both referees". This agrees with the current nbhd_cover_output.txt line `cell_26_22_11.txt … {(6, 4): 144}`.
  - **Not applied:** the parenthetical "(about 5 minutes on a quieter machine; the original run was evidently slowed by machine load)" is still there. The opus round-2 review (Section 2, Fix item 3) asked for "evidently slowed by machine load" to be dropped as a guess, and it contradicts line 1. The machine load during either run is not recorded.
- **Certificate C8 note (line 201): NOT APPLIED.**
  - `diff` of line 201 between 9ee8a20 and HEAD is empty. The note is word-for-word the round-1 (fda23fa) text: "the stored file `nbhd_cover_output.txt` initially lacked the $(26,22,11)$ line, because the original `reproduce.sh` gave each C8 run 1800 s and the $(26,22,11)$ run exceeded it (the script aborted there under `set -e`; the `exit 0` in the old `reproduce.log` was misleading)".
  - The note does not mention 124 or "about an hour". But it asserts as fact the timeout cause that the repository record does not support and that reproduce.log now withdraws. This is the "C8 note" part of item (4) and of opus round-2 Problem 1.
  - The rest of the note is accurate: the independent round-1 reproductions (opus `c8_check.py`, fable `nbhd26.cpp`), the 5400 s timeout, and the single-step regeneration with exit status 0.
- **Precision of "5 to 8.5 minutes"** (reproduce.log line 1, reproduce.sh line 30). I read the round-1 referees' records read-only:
  - `experiments/referee/L019-round1-opus/rerun_full/c8_loop.sh` runs all four C8 cells, and its log `c8_loop.log` reads "rc=0 elapsed 503". That is the four-cell loop, not the (26,22,11) step alone.
  - `experiments/referee/L019-round1-fable/repro/repro.log` reads "real 8m15.013s". It times that folder's whole reproduce.sh, C1–C8. Its file mtimes run from 05:54:10 (copy) to 06:02:25 (nbhd_cover_output.txt, 303 bytes, four lines).
  - Only the prover's single-step re-run timed the step itself: 06:54:23 to 06:59:17, i.e. 4 min 54 s.
  - So the record supports "finished within about 8.5 minutes", not "took 5 to 8.5 minutes". This is minor.

### Item (5): STATUS records round 2. APPLIED.
- Line 4 ends "revised again 07:26 UTC after round 2 (opus NEEDS-WORK = editorial, fable ACCEPT WITH FIXES: stale tags, evidence narrative, novelty caveat)". The commit time is 07:26:20.
- Cosmetic: the join reads "depends on them.; revised again".
- The "evidence narrative" entry becomes accurate only after fix F1.

## Remaining problems, in order of severity (all editorial)

- **F1 (required).** Certificate line 201 (C8, "Evidence note (round 1)"): replace the causal clause "because the original `reproduce.sh` gave each C8 run 1800 s and the $(26,22,11)$ run exceeded it (the script aborted there under `set -e`; the `exit 0` in the old `reproduce.log` was misleading)" with what is recorded. Suggested text: "; the cause is not recorded (the old `exit 0` in `reproduce.log` was written at 02d63ff, 05:22 UTC, before `nbhd_cover.py` existed; the timeout explanation of the 06:55 revision was a reconstruction and is withdrawn)". The heading could become "Evidence note (rounds 1–2)". Keep the rest of the note.
- **F2 (required).** experiments/prover/L019/reproduce.log line 4: delete "on a quieter machine; the original run was evidently slowed by machine load" and keep the measured duration (06:54:23–06:59:17 UTC, 4 min 54 s).
- **F3 (recommended, minor).** reproduce.log line 1 and the reproduce.sh line-30 comment: replace "took 5 to 8.5 minutes" with "finished within about 8.5 minutes (the single-step re-run took 4 min 54 s; the round-1 referee records time the whole four-cell C8 loop, 503 s, and a whole reproduce.sh run, 8 min 15 s)". In reproduce.log line 2, drop the stale "once appended".
- **F4 (cosmetic, optional).** In the STATUS line, ".;" should be "." or ";". experiments/prover/L019/README.md line 9 says "about 5-30 minutes" for the (26,22,11) step, but no record exceeds 8.5 minutes; it is an estimate, not a causal claim.

After F1 and F2 (F3 and F4 optional), a fix check of these few lines is enough. No computation and no new mathematical review is needed.

## Status of the proved parts

- 76c2322 changed no mathematical text: the four certificate hunks are bookkeeping lines.
- Rounds 1 and 2 (four referee reports) verified Theorems 1–6, Lemmas 7 and 11, Propositions 8 and 10, and Proposition 9 conditional on Conjecture T3, with independent computation in each round. They found no error in anything presented as proved.
- In this fix-check round I did not re-derive or recompute the mathematics; the task did not require it. My acceptance of the proved parts rests on those reports plus my verification that nothing mathematical changed since round 2.
- With GAPs 1–2 marked and the PARTIAL status, the proved parts can be accepted as stated. The only open items are F1–F4.

## Independence statement

- I read the two round-2 reviews:
  - results/reviews/L019-triple-coverage-C1__referee__20261027T072253Z.md (opus, NEEDS-WORK);
  - results/reviews/L019-triple-coverage-C1__referee__20261027T071808Z.md (fable, ACCEPT WITH FIXES).
- I also read the caveat lines of the scout review, and these round-1 referee records, read-only: experiments/referee/L019-round1-fable/README.md, repro/repro.log and the repro/ file listing; experiments/referee/L019-round1-opus/rerun_full/c8_loop.sh and c8_loop.log.
- My conclusions come from my own reading of the git record: `git show`, `git diff`, word diffs, `git log` timelines, and a byte comparison of line 201 at fda23fa, 9ee8a20 and HEAD.
- I ran no computation beyond git and grep, used no prover or referee code, and modified no file other than this review.

## Round 3 re-check (commit 5ece597, checked 2026-10-27T07:34:48Z)

Commands:
- `git show 5ece597`
- `git diff --stat 76c2322 5ece597 -- <L019 files>` (this equals the 5ece597 diff; no other commit in the range touches L019)
- word diffs of the certificate and reproduce.log
- `git status --short` (clean)
- `git ls-tree 02d63ff experiments/prover/L019/`

Results:
- **F1, certificate line 201: APPLIED.** Only the evidence-note sentence changed; the C8 data statement and every theorem and proof step are untouched. The note now says "the cause is not recorded (the earlier `exit 0` in `reproduce.log` came from a run that predates `nbhd_cover.py`; the timeout explanation given in the 06:55 revision was a reconstruction and is withdrawn)". The record supports this: the 02d63ff snapshot (05:22:52 UTC) holds the 'exit 0' log and a reproduce.sh without C7 or C8, and contains neither nbhd_cover.py nor blocked_and_6b.py.
- **F3: APPLIED.** The reproduce.sh comment and reproduce.log line 1 now give the single timed-alone figure, 4 min 54 s (06:54:23–06:59:17 UTC). Minor wording point in reproduce.log line 1: "other figures in this folder time whole loops or the whole script" is inaccurate. Those figures (503 s and 8 min 15 s) are in the round-1 referee folders. The only other figure in experiments/prover/L019/ is the README estimate "5-30 minutes" for the step itself.
- **F2: NOT CLEANLY APPLIED.** reproduce.log line 4 now ends "exit status 0 (about 5 minutes on a quieter machine; the original run was)." The guess was cut mid-sentence. This leaves a dangling fragment, and it keeps "on a quieter machine", an unrecorded comparison that F2 asked to delete.
- The certificate's `set -e` command line (reproduce.sh line 3) is correct as it stands.

**Final verdict (round 3): ACCEPT WITH FIXES (= NEEDS-WORK in my format; first line unchanged as instructed).**
- The certificate file needs no further change. All five items are applied in it, and its proved parts can be accepted as stated, with GAPs 1–2 and the PARTIAL status.
- One fix remains, in the auxiliary log. In reproduce.log line 4, replace "(about 5 minutes on a quieter machine; the original run was)" with "(4 min 54 s)".
- Optional: in reproduce.log line 1, change "in this folder" to "in the round-1 referee folders".
