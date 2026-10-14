VERDICT: NEEDS-WORK

# Referee review, round 3: L001-abase-two-point-extensions (certificate)

## Scope and provenance

- **Repo state.** HEAD 39194c2.
- **Files reviewed** (sha256 prefixes, identical at the start and end of the review):

| File | sha256 prefix |
|---|---|
| `results/proofs/L001-abase-two-point-extensions.md` | 7b96ee498c191ce4 |
| `extend.py` | 0ee1050dcdf3da9e |
| `bruteforce_check.py` | 546d617140a90883 |
| `results.json` | dd1244dfb7d23cb7 |
| `witnesses.json` | 822703c7c8490fab |
| `brute.log` | 47f2d37c8236c5f8 |
| `README.md` | c8c626d3e1708874 |
| `tests/test_abase_extensions.py` | 6320239000698886 |

- **Earlier reviews.** I read rounds 1 and 2 (`...__referee__20261014T080455Z.md`, `...T084239Z.md`) but formed my own verdict.
- **Independence.** Every check below was redone with new code in `experiments/referee/L001-round3/`:
  - that code imports nothing from `e757/`, `judge/`, the authors' scripts, or the round-1/round-2 folders;
  - the frozen judge was only executed, never modified.
- **Files touched.** Nothing outside that folder and this file was modified.

## Summary

**The certified theorem is true, and I verified all of it independently.** The theorem: for all distinct reals x, y ∉ A_base such that B = A_base ∪ {x,y} is a (4,5)-set, h(B) = 10.

I checked it by two routes.

- **Route 1** re-derives every computation in the T0/T1a/T1b/T2 case split with new code.
  - h is computed by two exact methods, both different from the judge: CDCL SAT on all sum-collision clauses, and numpy enumeration of all 2^n subsets.
  - Both h methods test the Sidon definition directly; neither uses the 3-AP reduction.
  - (4,5) is tested on all quadruples, in numpy and in pure Python.
  - Grid scans confirm that the candidate formulas are complete.
- **Route 2** is a line arrangement of all formal relations s1+s2 = s3+s4 on A ∪ {X,Y}.
  - It uses neither the case split nor the AP/weak-Sidon reduction, and it covers all of R².
  - The only non-generic (4,5) extensions it finds are exactly the stored 1,743 pairs.
  - Every class it finds has h = 10.
  - Positive controls (A_base minus two points) are detected.

Further checks:
- The frozen judge passes all 1,794 sets: A_base with h = 8, the 50 one-point extensions with h = 9, and the 1,743 pairs with h = 10.
- The authors' `extend.py` reproduces `results.json` and `witnesses.json` byte-for-byte.
- Their brute force reproduces `brute.log`.
- My own recount reproduces every window number quoted in the proof.

**Why NEEDS-WORK.** The proof text still contains statements that are false or unjustified as written:
1. A sentence that round 2 required to be fixed and that the revision left unchanged: "checked all 6,876 line pairs".
2. A definition/count mismatch for P_x (237 versus the stated 223).
3. A missing hypothesis check: K4 is applied to B, but the text never says why B is weak Sidon (that is K3).

Each is a one-line text edit. No new computation is needed, and a round-4 check only has to diff the text.

## Step-by-step check of the proof (my numbering)

### Statement

| # | Claim | Status |
|---|---|---|
| St1 | Main statement: for every admissible pair, h(B) = 10. | VERIFIED by R2–R5 |
| St2 | "No 16-point (4,5)-set containing A_base has h ≤ 9." | Equivalent to St1. OK |
| St3 | "Deleting a point, no 17-point one has h ≤ 9 either." | OK (see below) |
| St4 | Scope: nothing is claimed about four or more new points; an 18-point extension with h = 10 (ratio 5/9 < 4/7) is not excluded. | Correct. Round-2 Problem 1 is fixed |

St3 holds because a 17-point (4,5)-superset of A contains a 16-point (4,5)-superset of A (heredity), so its h is at least 10.

### Proof steps

**Pf1. h(B) ≤ h(A) + 2 = 10.** OK. h(A) = 8 is re-verified three ways in R1.

**Pf2. "A 3-AP-free subset of B of size 10 is exhibited in every case."**
- Converting 3-AP-free to Sidon needs B to be weak Sidon. That is true: (4,5) implies weak Sidon (K3 [published]; a parallelogram gives at most 4 distances).
- But the proof never says so, and DEPENDS ON omits K3. See Problem 3.
- In T0, T1a and T2-generic the 10-set is constructed rather than exhibited. This is cosmetic.

**Pf3. P_x and |P_x| = 223.**
- 223 is the size of P_x ∖ A.
- The set as written ("midpoints (a+b)/2 and endpoints 2b−a, a ≠ b ∈ A") has 237 elements, 14 of them in A (R2).
- This does not affect the logic, since x ∉ A, but the stated number is false for the stated set. See Problem 2.

**Pf4. Case T0.** OK.
- S ∪ {x,y} is 3-AP-free.
- R3: 100 random pairs each have 12 APs and h = 10.
- R4: the generic class has h = 10.

**Pf5. Case T1, the WLOG step, and |P_ok| = 50.** OK.
- The WLOG is valid because the statement is symmetric in x and y.
- R2: the formula set equals a definition-level grid scan.
- R4: the 50 values are exactly the admissible lines X = c.

**Pf6. Case T1a.** OK.
- h(A∪{x}) = 9 for all 50 x, by SAT, by all-subset enumeration, and by the judge.
- h(B) ≥ h(A∪{x}) + 1 because S9 ∪ {y} is 3-AP-free and B is weak Sidon.
- 150 random generic y all give h = 10.

**Pf7. Case T1b.** OK.
- 11,774 candidate pairs; 1,743 are (4,5); h = 10 for all of them.
- These are identical to `results.json` and to `witnesses.json`.
- All 1,743 pair witnesses and all 50 S9 witnesses are valid.

**Pf8. Case T2, generic points.** OK.
- There are 42 distinct lines.
- α(H(A) + {a,X,Y}) = 10 for every a, by enumerating all 2^16 subsets. Equivalently, no point of A lies in all 143 maximum Sidon sets.
- Random points on the lines (R3):
  - every one has exactly 13 APs;
  - 30 lines carry (4,5) points, all with h = 10;
  - the 12 lines x + y = 2a with a interior carry none.

**Pf9. Case T2, the 498 exceptional points.** OK.
- 861 line pairs: 273 parallel, 588 not. These give 512 distinct points, and 498 after filtering.
- None of the 498 is (4,5).
- Each has at least 2 cross APs, and the 4-set {a,a',x,y} has at most 4 distances.
- The phrase "or a further AP appears" is vacuous under the T2 hypothesis. Cosmetic.

**Pf10. Exhaustiveness.** OK by hand. R4 confirms it independently, with no case split.

### "Computer-verified steps" paragraph

| # | Claim | Status |
|---|---|---|
| CV1 | `extend.py` produces `results.json` | OK (R6) |
| CV2 | The test file passes | OK (R9) |
| CV3 | `bruteforce_check.py` description and numbers | OK (R7, R8, R11) |
| CV4 | "The first referee round ... checked all 6,876 line pairs." | FALSE as worded (Problem 1) |

Notes on CV3:
- The script imports nothing from e757 or extend.py.
- Lookups use exact Fraction keys (lines 35 and 76).
- Every quoted number is reproduced.
- "(5 minutes)" is the run time of the whole script (5m32s here), not of the h(A) check. Cosmetic.

## Checks performed

All checks ran as one process at a time from `experiments/referee/L001-round3/`; logs are next to each script.

### R1. `python3 -I s1_base.py` (0.5 s, `s1_base.log`)

A_base:
- 14 distinct points; (4,5) in both numpy and pure Python.
- 12 APs, whose midpoints are exactly the 12 interior points. AP degrees: one vertex of degree 4, six of degree 3, seven of degree 2.
- 12 sum-collision sets, all of them 3-APs.

h(A) = 8, three ways:
- SAT;
- enumeration of all 2^14 subsets, which finds 143 maxima;
- pure Python, which finds 0 Sidon 9-subsets and 143 Sidon 8-subsets.

α(H(A) + {a,X,Y}) = 10 for all 14 values of a.

Small examples:
- {1,2,3,5} is not (4,5); {2,3,5,8} is.
- {1,2,3,6} is (4,5) but not Sidon.

Larger sets:
- Fibonacci sets with n = 5, 8, 10, 12, 15, 18 have h = 4, 6, 7, 8, 10, 12; SAT and brute force agree.
- All 7 sets in `data/small_records.json` are (4,5), and SAT h = brute-force h = recorded h for each.

Lemma K4 checked on all 16,384 induced subsets of A_base: Sidon ⇔ 3-AP-free.

### R2. `python3 -I s2_t1.py` (38 s, `s2_t1.log`)

P and P_ok:
- |P| = 223. The literal definition gives 237, of which 14 are in A.
- A definition-level grid scan of (1/2)Z ∩ [−1100, 2200] equals P.
- |P_ok| = 50.
- h(A∪{x}) = 9 for all 50 x (SAT and brute force agree).

T1b pairs:
- For each of the 50 x, a (1/4)Z grid scan over [2min−max, 2max−min] equals Q(x).
- 11,774 candidate pairs; 1,743 are (4,5); h = 10 for all (SAT and brute force agree).
- 997 of them have both points in P.

Against the authors' files:
- My set equals the stored set (symmetric difference 0).
- The pairs in `witnesses.json` equal my set, with 0 invalid witnesses.
- The x-values of `generic_y` equal P_ok, with 0 invalid S9.

T1a: 150 random y all give h = 10.

### R2b. `python3 -I s2b_rejections.py` (54 s)

Every decision was redone with the pure-Python definition:
- all 1,609 coordinates;
- all 2,570 pairs with both singles (4,5).

Result: 0 disagreements with numpy, and 1,743 accepted.

### R3. `python3 -I s3_t2.py` (5 s)

The figures are those given under Pf8 and Pf9. In addition:
- 42 of the 498 exceptional points have a coordinate in P, so they are T1 anyway.
- Their denominators are {1, 3}.
- No line gave mixed outcomes across its 8 samples.
- T0: 100 random pairs, all with h = 10.

### R4. `python3 -I s4_arrangement.py` (90 s, `s4_arrangement.log`): independent completeness

**Method.**
- The type of (x,y) is the set of formal relations s1+s2 = s3+s4 that hold.
- The type determines distinctness, (4,5) (since |p−q| = |r−s| iff p+s = q+r or p+r = q+s) and every Sidon subset, hence h(B).
- The type is constant on 2-cells, on each line minus the other lines, and at each vertex.
- Lines with only invalid points are pruned: X = c with c ∈ A or A∪{c} not (4,5), and X = Y.
- Test points: one generic point; one point per kept line that lies on no other line (pruned lines included); and every vertex of the kept arrangement.

**Results for A_base.**

Relations and lines:
- 12 relations are always true.
- 1,910 distinct lines: 815 X-only, 815 Y-only, 280 two-variable.
- 379 lines are kept and 1,531 pruned. No test point on a pruned line is valid.

Test points:
- The generic point has h = 10.
- Kept lines:

| Line family | Lines with h = 10 | Lines with no valid point |
|---|---|---|
| X = c | 50 | 0 |
| Y = c | 50 | 0 |
| X + Y = s | 2 | 91 |
| X − Y = d | 0 | 158 |
| X − 2Y = c | 14 | 0 |
| 2X − Y = c | 14 | 0 |

- Of the 46,460 vertices, 42,974 are invalid and 3,486 are valid (1,743 unordered). All valid ones have h = 10, and they equal `results.json` exactly.
- No valid class has h < 10.

**Positive controls.** The same code was run on A_base∖{0,246}, A_base∖{243,249} and A_base∖{528,1056}.
- It reports 332, 791 and 1,338 deficient classes respectively.
- In each case the class containing the removed pair is among them, so the method does detect deficient extensions.

### R5. Frozen judge (34 s)

Command: `python3 -I s5_make_claims.py; python3 -I s5_run_frozen.py`. The wrapper runs `judge/judge.py` on 1,794 files, each with `claimed_h` and a SAT witness.
- 1,794 × PASS NO-IMPROVEMENT, exit code 0.
- n=14 h=8: 1 file; n=15 h=9: 50 files; n=16 h=10: 1,743 files.
- 10/16 = 5/8 > 4/7 exactly, so there is no record artifact.

### R6. Authors' pipeline: `rerun/extend_copy.py` (29 s)

- Only the two output paths were changed (diff lines 141 and 144).
- The resulting `results.json` and `witnesses.json` are byte-identical to the stored ones (sha dd1244df…, 822703c7…).

### R7. Authors' brute force: `rerun/bruteforce_copy.py` (5m32s)

- An unmodified copy, run next to a copy of `results.json`.
- Its output is identical to `brute.log`:
  - 143 maximum Sidon 8-subsets; 3,305 valid singles; 16,566 pairs with both points in APs; 5,185,660 (4,5) pairs; 0 witness failures;
  - 766 non-line-generic pairs; 0 missing; 15,800 line-generic pairs;
  - 1,743 stored, 766 in the window, 766 matched, 0 unmatched.

### R8. My own window recount: `python3 -I s6_window.py` (59 s, numpy)

- 3,305 valid singles.
- 5,185,660 (4,5) pairs.
- 16,566 pairs with both points in 3-APs: 15,800 line-generic and 766 non-line-generic.
- These 766 are exactly the stored pairs in the window.

### R9. `python3 -m pytest -v tests/test_abase_extensions.py`

2 passed.

### R10. `python3 -I s7_gluing.py`

Test of the K4 reduction on generic gluings of A_base with the 12-point sets #1 and #2 and the 14-point record (n = 26, 26, 28):
- all three are (4,5);
- SAT h with all sum-collision clauses equals α with 3-AP clauses only, and both equal h(A) + h(B): 15, 15 and 16.

### R11. Code reading

**extend.py.**
- Candidate generation is complete: the three roles in a 3-AP.
- `pair_ok` together with the single tests covers all 1,820 quadruples.
- Deduplication by frozenset is correct.
- The intersection points are computed correctly.
- Witnesses are checked with `is_sidon`.

**bruteforce_check.py.**
- `ap_free`, `sidon`, `pair_ok` and the cross-AP classification are correct.
- The witnesses are checked as Sidon by the definition.
- The window is [−300, 1699.5] in half-integers, as stated.

## Problems found (in order of severity)

No mathematical or computational problem was found. The following are textual problems in the proof file.

**Problem 1. A false sentence that round 2 required to be fixed and that is still unchanged (must fix).**
- The proof says: "The first referee round ... re-derived all counts ... and checked all 6,876 line pairs."
- In round 1, 6,876 = 589 + 6,287 is the number of (4,5) pairs with both points in 3-APs in the OLD window [−60, 1120]. Only 6,287 of them are line-generic. Round 1 computed h = 10 for all 6,876.
- Round 2 (Problem 2, second half) asked for this correction. The revision 9952b59 changed only the 766 sentence.
- As written, the sentence conflicts with the README, which gives 6,287 line-generic and 589 non-line-generic pairs.

**Problem 2. P_x: the definition does not match the count (must fix; one symbol).**
- "Let P_x be the finite set of reals that form a 3-AP with two points of A (midpoints (a+b)/2 and endpoints 2b−a, a ≠ b ∈ A)" defines a set of 237 elements, which includes all 14 points of A.
- The text then states |P_x| = 223.
- Add "∖ A". Optionally rename P_x to P, since the set does not depend on x.

**Problem 3. A hypothesis of a cited theorem is not checked in the text (must fix; one phrase).**
- The cases T0, T1a and T2-generic turn 3-AP-free subsets of B (or α of H(B)) into Sidon subsets of B. That is K4, which requires B to be weak Sidon.
- The proof never says why B is weak Sidon: B is (4,5), and K3 [published] says (4,5) ⊂ weak Sidon.
- DEPENDS ON omits K3, and lists K5–K6, which the argument does not use. Pf9 decides the exceptional points by computation; linearity only explains the result.

**Problem 4. Cosmetic (optional).**
- (a) "h(A_base)=8 re-checked exhaustively (5 minutes)": the 5 minutes is the script's total run time.
- (b) "or a further AP appears" is vacuous in T2, because any further AP is {a',x,y}, i.e. a second line.
- (c) "exhibited in every case": in T0, T1a and T2-generic the 10-set is constructed.
- (d) The STATUS line mentions only round 1.
- (e) README:
  - line 8 says "~1 h" for the brute force; it takes about 5.5 min;
  - line 41 (Conclusion) still describes the old [-60,1120] window;
  - lines 44–48 are the old brute-force section, superseded but still present;
  - line 59 cites `brute.log` for the run time, which is in `brute.time`.

### Status of earlier requests

| Request | Status |
|---|---|
| Round 1 P1 (overclaim) | Fixed |
| Round 1 P2 (witnesses) | Fixed |
| Round 1 P3 (independence of the brute force) | Fixed |
| Round 2 Problem 1 ("three" → "four") | Fixed |
| Round 2 Problem 2, first half (the 766 sentence) | Fixed |
| Round 2 Problem 2, second half (the 6,876 sentence) | **Not fixed** (Problem 1 above) |
| Round 2 Problem 3 (exact keys) | Fixed and re-run; R7 and R8 confirm it |
| Round-1/2 nits P4(a, d) | Not addressed; now Problems 2 and 3 |
| Remaining nits and stale README text | Not addressed (Problem 4) |

## What is needed for ACCEPT

Edit `results/proofs/L001-abase-two-point-extensions.md` only. No computation is needed.

1. Replace "and checked all 6,876 line pairs." with: "and computed h = 10 directly for all 6,876 (4,5) pairs with both points in 3-APs in the earlier window of half-integers in [-60,1120] (589 non-line-generic, 6,287 line-generic)."
2. Make the definition read "the finite set of reals not in $A$ that form a 3-AP with two points of $A$", or append "$\setminus A$" to the formula.
3. Make two changes for K3:
   - add to DEPENDS ON: "K3 [published] ((4,5) ⊂ weak Sidon, so K4 applies to B)";
   - add after "exhibited in every case": "(B is a (4,5)-set, hence weak Sidon by K3, so its 3-AP-free subsets are Sidon by K4)".
   
   Optionally drop K5–K6, or mark them "explanatory only".

Problem 4 is optional.

All computational content of the certificate is verified by R1–R11 above. Once edits 1–3 are made, the certificate merits ACCEPT, and K13 / D6 can be tagged [verified-here]. The scope is exactly 2-point extensions, and hence 3-point ones.
