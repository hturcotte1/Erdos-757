VERDICT: ACCEPT

# Referee review, round 4: L001-abase-two-point-extensions (certificate)

## Scope and provenance

- **Repo state.** HEAD was 3ffa385 at the start and 563b919 at the end. The only commit in between changed `journal/LOG.md`, and `git diff 3ffa385 HEAD` is empty on every reviewed file.
- **Files reviewed.** sha256 prefixes, identical at the start and end of this review:

| File | sha256 prefix |
|---|---|
| `results/proofs/L001-abase-two-point-extensions.md` | f4f76e1de6d0b2c1 |
| `extend.py` | 0ee1050dcdf3da9e |
| `bruteforce_check.py` | 546d617140a90883 |
| `results.json` | dd1244dfb7d23cb7 |
| `witnesses.json` | 822703c7c8490fab |
| `brute.log` | 47f2d37c8236c5f8 |
| `README.md` | c8c626d3e1708874 |
| `tests/test_abase_extensions.py` | 6320239000698886 |
| `judge/judge.py` | e061f0e2072e7d09 (equals `judge/judge.sha256`) |

- **What changed since round 3.** Code and data are byte-identical to round 3. Only the proof text changed (`git diff 39194c2 3ffa385`).
- **Independence.** Scratch work is in `experiments/referee/L001-round4/`.
  - No code imports anything from `e757/`, `judge/`, the authors' scripts, or the round 1–3 referee folders.
  - The judge was only executed, as a subprocess (`r4_run_judge.py`).
  - Nothing outside the scratch folder and this file was modified.
- **Earlier reviews.** I read rounds 1–3 but did not rely on them. Every computational claim was re-derived below, including by a method that no earlier round used.

## Summary

**ACCEPT.** The certified statement is true, and every step of the proof text is verified: for all distinct reals x, y ∉ A_base with B = A_base ∪ {x,y} a (4,5)-set, h(B) = 10.

**Route L (new in this round) covers all of R² directly from the Sidon definition.** It uses no 3-AP reduction, no weak-Sidon lemma, and no case split.
- h(B) = 10 iff S ∪ {x,y} is Sidon for one of the 143 maximum Sidon sets S of A.
- So the deficient pairs are exactly the valid points of the locus D = ⋂_S (union of the relation lines of S ∪ {X,Y}).
- I computed D exactly. It consists of:
  - the 29 whole lines X=a, Y=a (a ∈ A) and X=Y, all excluded by hypothesis;
  - 702 isolated points, none of them a (4,5)-set.
- The result is identical for two different choices of the starting set S1.
- Seven positive controls (A_base minus one or two points) all detect the known deficient extensions, and the deficient points they report are confirmed by MaxSAT.

**Route C re-derives every number in the case split with new code:** 223 (237 with A), 50, h(A∪{x}) = 9, 11,774, 1,743, h = 10, 42, 498, 0.

**Route W reproduces every window figure in the text,** including round 1's older-window figures 6,876 = 589 + 6,287.

**The authors' artifacts reproduce.**
- The authors' pipeline reproduces `results.json` and `witnesses.json` byte-for-byte.
- Their brute force reproduces `brute.log`.
- The frozen judge passes all 1,794 sets, and the test file passes.

**All requested edits are made.** The three must-fix edits requested by round 3 are in the text verbatim, and the optional items 4(a)–(d) were also done.

**Remaining issues are editorial and non-blocking.** The most notable is that the title omits the "(4,5)" qualifier. Literally read, the title is false: 351 non-(4,5) two-point extensions have h = 9. The Statement, which is the certified claim, carries the hypothesis and is correct.

## Diff against round 3's "What is needed for ACCEPT"

| Round-3 request | Status in `3ffa385` |
|---|---|
| 1. Replace the 6,876 sentence | Done verbatim |
| 2. P_x "not in A" / "∖A" | Done: both "not in $A$" and "minus $A$"; now consistent with 223 |
| 3a. K3 in DEPENDS ON | Done: "K3 [published] ((4,5) ⊂ weak Sidon, so K4 applies to B)" |
| 3b. K3/K4 parenthetical after "exhibited" | Done, together with "exhibited or constructed" (4c) |
| 3c (optional). K5–K6 | Marked "explanatory only" |
| 4(a) 5-minute wording | Done ("the whole script runs in about 5.5 minutes"; measured 5m22s here, 5m42s in `brute.time`) |
| 4(b) "or a further AP appears" | Removed |
| 4(d) STATUS line | Now mentions rounds 1–3 |
| 4(e) README stale lines | Not changed (optional; see Note 2) |

## Step-by-step check of the proof text (my numbering)

**Statement**

| # | Claim | Status |
|---|---|---|
| St1 | For all distinct reals x,y ∉ A with B (4,5): h(B) = 10 | VERIFIED over all of R² (R1), and through the case split (R3) |
| St2 | No 16-point (4,5)-set containing A_base has h ≤ 9 | Equivalent to St1. OK |
| St3 | No 17-point one either | OK: delete one new point (heredity), then h is monotone |
| St4 | Nothing is claimed for four or more new points; 5/9 < 4/7 | Correct scope |
| St5 | Title "No 2-point extension of A_base has a largest Sidon subset of size 9" | True only with the implicit "(4,5)"; see Note 1 |

**Proof**

- **Pf1. h(B) ≤ h(A) + 2 = 10.** OK. h(A) = 8 is re-verified in R3 by brute force and MaxSAT.
- **Pf2. 3-AP-free subsets of B are Sidon.** OK.
  - B is (4,5), hence weak Sidon (K3). A parallelogram a+d = b+c gives at most 4 distances.
  - For weak Sidon sets, 3-AP-free ⇔ Sidon (K4).
  - The labels match `kb/known_results.md` rows K3, K4 and K11, all [published].
- **Pf3. P_x = (midpoints ∪ endpoints) ∖ A has 223 elements.** OK (R3: 237 elements before removing the 14 points of A).
- **Pf4. T0.** OK. S ∪ {x,y} is 3-AP-free because no 3-AP of B meets {x,y}.
- **Pf5. T1.** OK.
  - The WLOG is valid because the statement is symmetric in x and y.
  - Heredity forces x ∈ P_ok, and |P_ok| = 50 (R3).
- **Pf6. T1a.** OK. h(A∪{x}) = 9 for all 50 x, by two methods (R3). S9 ∪ {y} is 3-AP-free. The upper bound h(B) ≤ h(A∪{x}) + 1 is trivial.
- **Pf7. T1b.** OK.
  - y lies in the finite set Q(x) of midpoints and endpoints of pairs of A∪{x}.
  - 11,774 pairs, of which 1,743 are (4,5), all with h = 10 (R3).
  - The witnesses are valid (R3).
- **Pf8. T2 at points on exactly one line.** OK.
  - Under the T2 hypothesis every new AP contains both x and y, so it is {a',x,y} and gives a line through (x,y).
  - Off the exceptional points, H(B) = H(A) + {a,x,y}.
  - Its α is 10 because every a ∈ A is avoided by some maximum Sidon set of A (R3).
  - Wording: see Note 3.
- **Pf9. The 498 exceptional points.** OK: none is (4,5) (R3), and each has at least 2 APs through {x,y}.
- **Pf10. Exhaustiveness.** OK by hand. Independently confirmed with no case split by R1.

**Computer-verified paragraph and sanity checks**

| # | Claim | Status |
|---|---|---|
| CV1 | `extend.py` produces `results.json` | R5: byte-identical |
| CV2 | The test re-checks 50 stored extensions | R8: 2 tests pass; the first samples 50 of the stored 16-point sets |
| CV3 | Brute-force figures: 5,185,660; 0 failures; 15,800; 766 contained with exact keys; h(A) = 8 | R4 (own code) and R6 (authors' code) |
| CV4 | Round-1 sentence (6,876 = 589 + 6,287; three implementations) | Matches the round-1 review (C2, C4, C8) and my old-window recount (R4) |
| SC | Judge h(A_base) = 8; the 1,743 sets have 16 points and ratio 5/8 | R7 |

## Checks performed

All runs were single processes, launched from `experiments/referee/L001-round4/` (rerun/ for R5 and R6) with `python3 -I`. Logs are next to the scripts.

### R1. Route L, deficiency locus over all of R²

Command: `python3 -I r4_locus.py` (9m38s including the controls; files `r4_locus.log`, `r4_locus_out.json`).

**Method.**
- M is the set of all Sidon 8-subsets of A, computed by brute force over all 3,003 8-subsets: there are 143. There are 0 Sidon 9-subsets.
- For S ∈ M, K(S) is the set of all lines αX+βY = γ given by formal coincidences s1+s2 = s3+s4 ({s1,s2} ≠ {s3,s4}) over the symbols S ∪ {X,Y}.
- D ⊆ K(S1). For each line l of K(S1):
  - if l lies in every K(S), it is a whole line of D;
  - otherwise l ∩ D lies in the finite set l ∩ K(S2), for some S2 with l ∉ K(S2). Each such point was tested against all 143 S.
- The validity test is: x ≠ y, x,y ∉ A, and every 4-subset of B meeting {x,y} has at least 5 distances. Whole lines are tested at a point verified to be generic: every coincidence over A ∪ {X,Y} that holds there holds identically on the line.

**Results.**

| | S1 = M[0] | S1 = M[77] |
|---|---|---|
| Lines in K(S1) | 581 | 537 |
| Candidate points tested | 148,534 | 155,880 |
| Whole lines of D | 29 | 29 |

- **Whole lines of D.** They are X=a and Y=a for the 14 points a ∈ A, and X=Y. All are excluded by the hypothesis.
  - There is no line X = c with c ∉ A, so h(A∪{c}) = 9 for every real c ∉ A.
- **Isolated points of D (off the whole lines).** There are 702 for each choice of S1, and the two sets are identical.
  - Full 1,820-quadruple test: all 702 are non-(4,5), and 0 are valid.
- **Conclusion.** D ∩ Valid = ∅, which is the theorem over all of R².
- Every candidate point had denominator dividing 120 (scaled coordinates were integral). This is not needed for correctness, since all arithmetic is exact.

### R2. Positive controls

Command: `python3 -I r4_controls_post.py` (file `r4_controls_post.log`).

**c1: A' = A_base ∖ {u,v}.** h(A') = 8 for all 91 pairs, so (u,v) is deficient: h(A_base) = 8 < 10. I ran (0,246), (243,249), (528,1056) and (136,596).
- (u,v) is detected in all four cases, either as a valid isolated point or as a point on a reported valid whole line such as X=0.
- The method reports 184, 456, 828 and 1,008 valid isolated deficient points respectively.
- The first five in each case were checked: all are (4,5) with MaxSAT h = 9 < 10.

**c2: A'' = A_base ∖ {u}, for u = 0, 246, 1056.**
- X=u and Y=u are reported as valid whole deficient lines.
- At a generic point (u,t), the set is (4,5) and h = 9 < 10 (MaxSAT).
- The reported isolated points (first five in each case) are confirmed in the same way.

### R3. Route C, recount of the case split

Command: `python3 -I r4_cases.py` (1m43s; files `r4_cases.log`, `r4_cases_out.json`). h is computed two ways:
- the criterion "some S ∈ M with S ∪ new Sidon";
- exact MaxSAT (pysat RC2) on all sum collisions.

Neither method is the judge's.

**A_base.**
- (4,5) on all 1,001 quadruples.
- h = 8 by brute force (143 maxima) and by MaxSAT.
- 12 3-APs, whose midpoints are exactly the 12 interior points.

**P and T1.**
- |P_full| = 237, of which 14 are in A, so |P| = 223. |P_ok| = 50.
- h(A∪{x}) = 9 for all 50 x; the two methods agree.
- T1b: 11,774 unordered candidate pairs. 1,743 are (4,5) by the full test, and h = 10 for all 1,743 by both methods. 997 of them have both points in P.

**Authors' files.**
- `results.json`: 1,743 rows with 1,743 distinct exact keys, all h = 10. The symmetric difference with my set is 0, and the summary fields match.
- `witnesses.json`, pairs: 1,743 witnesses, 0 invalid (10 distinct points ⊆ B, Sidon by definition), and the key set equals the stored set.
- `witnesses.json`, S9: 50 witnesses, 0 invalid, and their x-set equals P_ok.

**T2.**
- 42 distinct lines: 273 parallel pairs and 588 non-parallel pairs.
- 512 distinct intersection points, 498 after removing x=y and x or y ∈ A. 0 of them are (4,5). Each has at least 2 cross APs, and 42 have a coordinate in P.
- Every a ∈ A is avoided by some maximum Sidon set.
- 168 random points on the 42 lines all have exactly 13 APs. The (4,5) ones lie on 30 lines, and all have h = 10.

### R4. Route W, window recount

Command: `python3 -I r4_window.py` (21 s; numpy int64 in doubled coordinates; file `r4_window.log`).

**Window [-300, 1699.5].**
- 3,305 valid singles.
- 5,185,660 (4,5) pairs.
- 16,566 pairs with both points in 3-APs: 15,800 line-generic and 766 non-line-generic.
- 766 stored pairs lie in the window: 0 missing and 0 unmatched.
- 83 sampled numpy decisions were re-confirmed in pure Python.

**Round-1 window [-60, 1120]** (with or without the endpoint):
- 1,781 singles and 1,455,177 (4,5) pairs.
- 6,876 pairs with both points in 3-APs: 6,287 line-generic and 589 non-line-generic.
- 589 stored pairs in the window, 0 missing.

### R5. Authors' `extend.py`

Run as `rerun/extend_copy.py`; the diff from the original is lines 141 and 144 only (output paths). Run time 27 s.
- The summary is identical: 11,774 / 1,743 / 223 / 50 / 498 / 0 / 1,743, and all 42 line alphas are 10.
- `results_rerun.json` and `witnesses_rerun.json` are byte-identical to the stored files.

### R6. Authors' `bruteforce_check.py`

Run as `rerun/bruteforce_copy.py`, an unmodified copy run next to a copy of `results.json`. It took 5m22s, and its output is identical to `brute.log`.

### R7. Frozen judge

Commands: `python3 -I r4_make_claims.py` then `python3 -I r4_run_judge.py`. This runs `judge/judge.py` on 1,794 files in `jin/`, each with `claimed_h` and a witness.
- Result: 1,794 × PASS NO-IMPROVEMENT, exit 0, 33.6 s.

| n | h | Sets | h/n | h/n < 4/7 (exact)? |
|---|---|---|---|---|
| 14 | 8 | 1 | 4/7 | no |
| 15 | 9 | 50 | 3/5 | no |
| 16 | 10 | 1,743 | 5/8 | no |

- There is no record artifact.
- My first attempt put the judge path and a shell redirect in one command, and `.claude/hooks/protect.py` blocked it. Nothing was written to `judge/`.

### R8. Test file

`python3 -m pytest -q tests/test_abase_extensions.py`: 2 passed.

### R9. Title check

Command: `python3 -I r4_title_check.py`. The 702 isolated points of D (351 unordered pairs) are all non-(4,5), and all have MaxSAT h = 9.
- Example: {x,y} = {-1244, 1516}.
- x + y = 0 + 272, so {x, y, 0, 272} has the distances {2760, 1244, 1516, 272}: only 4 distinct values.

## Problems found (in order of severity)

No mathematical, computational or logical problem was found. The notes below are editorial. None affects the truth or verifiability of the certified Statement, so none blocks acceptance.

**Note 1. The title omits "(4,5)" (recommended fix, one word).**
- Read literally, "No 2-point extension of A_base has a largest Sidon subset of size 9" is false: the 351 non-(4,5) pairs of R9 have h = 9.
- The Statement says "such that B is a (4,5)-set" and is correct. The repo also uses "extension" for (4,5)-supersets elsewhere (START_HERE §7: "No 2-point extension of $A_{\rm base}$ beats 4/7").
- Suggested title: "No (4,5)-set A_base ∪ {x,y} has a largest Sidon subset of size 9".
- When the result is recorded in the LEDGER, K13 or D6, quote the Statement, not the title.

**Note 2. The experiment README has stale lines (optional; round-3 4(e), unchanged).**
- Line 8 says "~1 h"; the brute force takes about 5.5 min.
- Line 41 (Conclusion) still names the old window [-60,1120].
- Lines 44–48 are the old brute-force section. They are superseded by the section starting at line 50, but still present.
- Line 59 cites `brute.log` for the run time, which is in `brute.time`.

**Note 3. Wording in T2 (optional).**
- "At a generic point of the line" means "at a T2 point lying on exactly one of the 42 lines".
- The one-line reason is not written in the proof itself: under T2 every new AP contains both x and y, so it is another of the 42 lines. The exhaustiveness sentence implies it, and README line 23 states it.
- Spelling it out would make the T2 paragraph self-contained.

## Consequence

The certificate is verified. K13 / D6 may be tagged [verified-here] with exactly this scope: (4,5)-sets A_base ∪ {x,y} (two points), hence also 17-point (4,5)-supersets. Extensions by four or more points remain open, and an 18-point (4,5)-superset with h = 10 would be a record.
