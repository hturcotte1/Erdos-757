VERDICT: NEEDS-WORK

# Referee review, round 2: L001-abase-two-point-extensions (certificate)

## Files reviewed

| File | sha256 prefix |
|---|---|
| `results/proofs/L001-abase-two-point-extensions.md` | 4efd26fb486529da |
| `experiments/20261014-0640-abase-extensions/extend.py` | 0ee1050dcdf3da9e |
| `bruteforce_check.py` | 695070afc4bb74f9 |
| `results.json` | dd1244dfb7d23cb7 |
| `witnesses.json` | 822703c7c8490fab |
| `README.md` | 889c122c75960670 |
| `brute.log` | b8e313ee6299741d |
| `tests/test_abase_extensions.py` | 6320239000698886 |

- Repo HEAD: cff0d00.
- Round-1 review read: `results/reviews/L001-...__referee__20261014T080455Z.md`.
- Scratch directory: `experiments/referee/L001-round2/`. All new code there imports nothing from `e757/`, `judge/` or the authors' scripts; the judge was only executed, read-only.
- Nothing outside the scratch directory and this file was modified; `git status` is clean apart from the scratch directory.

## Summary

**The certified theorem is true, and I verified it completely, by two routes that share no code with the authors.** The theorem: for all distinct reals x, y ∉ A_base with B = A_base ∪ {x,y} a (4,5)-set, h(B) = 10.

- **Route 1** re-derives every computation in the authors' case split T0 / T1a / T1b / T2 with my own code:
  - candidate sets come from a definition-level 3-AP scan, not the partner formulas;
  - (4,5) is tested on all C(16,4) = 1820 quadruples;
  - h is computed by brute force over all subsets AND by an ILP (HiGHS) on equal-difference conflicts.
- **Route 2** is a line-arrangement argument in the (x,y)-plane that needs neither the case split nor the AP/weak-Sidon reduction.
  - Every formal relation u1+u2 = u3+u4 over A ∪ {X,Y} defines a line.
  - The coincidence type of B is constant on cells and on open edges of this arrangement.
  - So one generic point of the plane, one generic point per line, and all 46,460 vertices decide the question over all of R².
  - Result: exactly 1,743 unordered (4,5) non-generic pairs. This is the same set as the authors' T1b set, and every one has h = 10. Every generic class is either not (4,5) or has h = 10.
  - A positive control confirms that the same code detects deficient extensions: for A' = A_base minus two points it reports A_base itself.
- **Reproduction of the authors' artifacts.**
  - The frozen judge gives PASS with h = 10 on all 1,743 extension sets, h = 9 on all 50 one-point extensions, and h = 8 on A_base.
  - The authors' pipeline reproduces byte-identical results.json and witnesses.json.
  - Every witness in witnesses.json is a genuine Sidon set.
  - Their brute-force run reproduces brute.log exactly.

**Why NEEDS-WORK.** Every mathematical step is verified. The verdict is NEEDS-WORK only because the revised text contains three small factual inaccuracies, and the rubric allows ACCEPT only when no problem remains:
1. A self-contradictory scope sentence in the Statement ("three or more" should be "four or more").
2. A wrong description of what the "766 pairs" are.
3. A formally unsound exact-membership test in `bruteforce_check.py`, which the README calls a harmless "display artifact". Its conclusion is nevertheless true; I re-did the test exactly.

All three are text edits. No new computation is needed.

## Step-by-step check of the proof (numbered)

Notation:
- A = A_base and B = A ∪ {x,y}.
- P = {v ∉ A : {v,a,b} is a 3-AP for some distinct a, b in A} (the proof's "P_x").
- P_ok = {x ∈ P : A ∪ {x} is (4,5)}.

**St1. Main statement.** For all distinct reals x, y ∉ A with B (4,5), h(B) = 10.
- VERIFIED twice: Route 1 (C2–C5) and Route 2 (C6).

**St2. "No 16-point (4,5)-set containing A_base has h ≤ 9."**
- Equivalent to St1. OK.

**St3. "Deleting a point, no 17-point one has h ≤ 9 either."**
- If C ⊇ A has 17 points and is (4,5), delete one of the new points. The result is a 16-point (4,5)-set (heredity) with h ≤ h(C), so h(C) ≥ 10.
- Since 68/7 < 10, no 3-point extension beats 4/7. OK.

**St4. "The statement says nothing about extensions by three or more points: an 18-point ... set with h=10 ... is NOT excluded."**
- The 18-point remark is correct: 10/18 = 5/9 < 4/7.
- But "three or more" contradicts St3, which is exactly a statement about 3-point extensions. See Problem 1.

**Pf1. h(B) ≤ h(A) + 2 = 10.**
- Delete x and y from a Sidon subset of B. OK.

**Pf2. Sidon equals 3-AP-free inside B.**
- This is K4 [published]. Its hypothesis, weak Sidon, holds because a (4,5)-set has no parallelogram a+b = c+d.
- Re-derived: the only possible sum collision left is 2u = v + w, i.e. a 3-AP.
- Used only in the abstract cases T0, T1a and T2-generic. OK.

**Pf3. Definition of P_x and |P_x| = 223.**
- Re-computed: 223 (C2).
- Notation nit (round-1 P4a, still open): read literally, the definition also contains the 14 points of A (237 values). Harmless, because x ∉ A.

**Pf4. Case T0 (no 3-AP of B contains x or y).**
- S ∪ {x,y} is 3-AP-free for a maximum Sidon set S of A. OK.
- 60 random T0 points: all (4,5), h = 10, exactly 12 APs (C4).

**Pf5. Case T1 (some new AP has exactly one new point, say x).**
- WLOG is valid: the statement is symmetric in x and y.
- x ∈ P, and A ∪ {x} ⊆ B is (4,5), so x ∈ P_ok. |P_ok| = 50 (C2).
- Route 2 independently finds the same 50 values as the only admissible "special" single coordinates (C6).

**Pf6. Case T1a (y in no AP of B).**
- H(B) = H(A ∪ {x}) plus the isolated vertex y.
- h(A ∪ {x}) = 9 for all 50 x: brute force, ILP and judge (C2, C9).
- 150 random generic y: all (4,5), h = 10.
- OK.

**Pf7. Case T1b (y in some AP of B).**
- Every AP through y has its other two points in A ∪ {x}, so y lies in a finite set.
- 11,774 unordered candidate pairs; 1,743 are (4,5); h = 10 for all of them by brute force and by ILP (C2).
- The set equals results.json and witnesses.json exactly.
- All 1,743 witnesses are valid Sidon 10-subsets (C8).
- OK.

**Pf8. Case T2 generic (x, y ∉ P, exactly one new AP {a,x,y}).**
- (x,y) lies on one of 42 lines.
- α(H(A) + {a,x,y}) = 10 holds iff h(A∖{a}) = 8. Verified for all 14 values of a by brute force and ILP, and also on the abstract 16-vertex hypergraph (C1).
- Random points on the lines (C4):
  - always exactly 13 APs;
  - 30 lines carry (4,5) points, all with h = 10;
  - the 12 lines x + y = 2a with a interior carry none, because a = (b+c)/2 gives a parallelogram.
- OK.

**Pf9. T2 exceptional points.**
- 42 lines; 588 non-parallel pairs; 512 distinct intersection points; 498 after removing x = y and x or y in A. None is (4,5) (C4).
- There is also a structural reason. Two cross APs {a,x,y} and {a',x,y} with a ≠ a' give two distinct distance coincidences in {a, a', x, y}, so that 4-set has at most 4 distances.
- The proof's phrase "or a further AP appears" is vacuous under the T2 hypothesis, since any further AP contains both x and y (round-1 P4b, still open).
- OK.

**Pf10. Exhaustiveness.**
- No new AP: T0.
- Some new AP contains exactly one new point: T1, split into T1a or T1b.
- Otherwise every new AP is {a,x,y}: T2, split into one line or several lines.
- Real (not just rational) x and y are covered, because the only infinite families (T0, T1a, T2-generic) are handled abstractly.
- Route 2 confirms exhaustiveness independently. OK.

## Checks performed

All commands were run from `experiments/referee/L001-round2/` as single processes; each took under 6 minutes.

**C1. Base set.** `python3 -I s1_base.py` (log `s1_base.log`, 0.9 s).
- A has 14 distinct points and is (4,5).
- It has 12 3-APs, whose midpoints are exactly the 12 interior points.
- h(A) = 8 by brute force and by ILP. There are 143 Sidon 8-subsets and 0 Sidon 9-subsets.
- h(A∖{a}) = 8 by brute force and ILP for all 14 values of a.
- For every a, the abstract hypergraph H(A) + {a,X,Y} has an independent 10-set and no independent 11-set.

**C2. Case T1.** `python3 -I s2_t1.py` (log `s2_t1.log`, 67 s).
- Candidates are found by a numpy scan of the definition (equal gaps of the sorted triple) over all of (1/4)Z in [2min−max, 2max−min]. All candidates provably lie in that set.
- |P| = 223, all in (1/2)Z. |P_ok| = 50.
- h(A∪{x}) by (brute force, ILP) = (9, 9) for all 50 x.
- T1b: 11,774 unordered candidate pairs, of which 1,743 are (4,5) on the full 1820-quadruple test. Brute force gives {10: 1743}; ILP gives {10: 1743}.
- 997 of the pairs have both points in P.
- Compared with the authors' files: stored 1,743, mine 1,743, symmetric difference 0. witnesses.json pairs equal my set. witnesses.json `generic_y` x-values equal my P_ok.
- T1a spot check: 150 random generic y (denominator 1000003) are all (4,5) with h = 10.

**C3. Primitives.** `rc.py`:
- `is45`: all C(n,4) quadruples.
- `is_sidon`: all positive differences distinct.
- `hmax_brute`: exhaustive search over k-subsets.
- `hmax_ilp`: scipy `milp`/HiGHS. For every two distinct pairs with equal difference, the sum of z over their union is at most |union| − 1. Every optimum is re-checked as Sidon.
- Sanity (`s8_primitives_sanity.log`):
  - every set in `data/small_records.json` (n = 8, 10, 11, 12, 14, 12b, 12c) is (4,5), with brute-force h = ILP h = the recorded h;
  - Fibonacci sets {2,3,5,8,...} with n = 5, 8, 10, 12, 15 have h = 4, 6, 7, 8, 10 by both methods;
  - {1,2,3,5} is not (4,5); {2,3,5,8} is.

**C4. Case T2 and T0.** `python3 -I s3_t2.py` (log `s3_t2.log`, 5 s).
- 588 non-parallel line pairs give 512 distinct intersection points, and 498 after filtering. None is (4,5); every one lies on at least 2 lines. Their denominators are {1, 3}, so they are invisible to the authors' half-integer grid; they are decided by extend.py and by C4/C6.
- 252 random line points (6 per line) all have 13 APs.
- 30 lines have (4,5) points, with h = 10 at every one. 12 lines (x+y = 2a, a interior) have none. No line gives mixed outcomes.
- T0: 60 random pairs are all (4,5) with h = 10 and 12 APs.

**C5. Frozen judge.** Run via wrappers `run_judge.py` and `run_all_sets.py`, which call `python3 judge/judge.py <files>` (logs `judge.log`, `judge_all.log`).
- 255 files: A_base gives n=14, h=8; all 50 sets A∪{x} give n=15, h=9; 204 sampled B, including the 4 with the most extreme coordinates, give n=16, h=10.
- All 1,743 B give "PASS NO-IMPROVEMENT n=16 h=10", using the authors' witness as `witness_sidon_subset`.
- Exit code 0 in both runs.

**C6. Independent completeness via the line arrangement.** `python3 -I s4_arrangement.py` (log `s4_arrangement.log`, 65 s). This uses no AP theory and no T0/T1/T2 split.

Method:
- Symbols are the 14 points of A plus X and Y. Every pair of distinct 2-multisets gives a relation al·X + be·Y = ga.
- 12 relations are constant and true (A's own APs).
- The rest define 1,910 lines: 815 X-only, 815 Y-only and 280 two-variable, with coefficient patterns (1,1), (1,−1), (2,−1), (1,−2).
- The type of (x,y), meaning which relations hold, determines distinctness, (4,5) and h.
- The type is constant on the complement of all lines, and on each line minus the other lines. It therefore suffices to check:
  - one point on no line;
  - for each line, one point on that line and on no other;
  - every vertex.
- Lines X = c with A ∪ {c} not (4,5), or c ∈ A, and the line X = Y, carry no admissible point, and are pruned with that justification.

Results:
- The admissible special single values are exactly the 50 values of P_ok.
- 379 valid lines remain.
- Generic plane points: h = 10.
- Generic points of valid lines:
  - X = c and Y = c lines (100 samples each): h = 10;
  - 2X − Y = a and X − 2Y = −a: h = 10;
  - X + Y = 0 and X + Y = 2112: h = 10;
  - the other 91 lines X + Y = s and all 158 lines X − Y = d: not (4,5).
- 46,460 vertices, of which 30,904 are admissible and 3,486 ordered (1,743 unordered) are (4,5). h = 10 for all 1,743, and the set equals the T1b set from C2.

**C7. Positive control for C6.** `python3 -I s7_control.py` (log `s7_control.log`, 50 s). The same algorithm run on A' = A_base∖{p,q} must report (p,q), because h(A_base) = 8 < h(A') + 2 = 10.
- (0,246): reported as a vertex with h = 8; 168 deficient classes in total.
- (243,249): reported, h = 8; 402 deficient classes.
- (528,1056): reported, h = 8; 679 deficient classes.

So the method does detect deficient extensions, and for A_base it finds none.

**C8. witnesses.json.** `python3 -I s5_witness_judge.py` (log `s5_witness.log`).
- All 1,743 `pairs` entries pass: 10 distinct points, a subset of A∪{x,y}, x and y ∉ A, x ≠ y, Sidon by the definition, and B (4,5). 0 failures.
- All 50 `generic_y` entries pass: 9 distinct points, a subset of A∪{x}, Sidon, and A∪{x} (4,5). 0 failures.
- As exact Fractions, results.json `stored` equals the witnesses.json pair set.

**C9. Authors' pipeline re-run.** `rerun/extend_copy.py`; the diff from the original is only the two output paths (lines 141 and 144). Run time 27 s.
- Summary: type1_pairs 11774, type1_45 1743, Px_size 223, Px_45 50, type2_isect_pts 498, type2_isect_45 0, witness_certified 1743; all 42 line alphas are 10.
- Output results.json and witnesses.json are byte-identical to the stored ones (sha256 dd1244df…, 822703c7…).

**C10. Tests.** `python3 -m pytest -q tests/test_abase_extensions.py` gives 2 passed.

**C11. Authors' brute force re-run, and an exact redo of its window statistics.**
- `rerun/bruteforce_copy.py`, an unmodified copy run in a directory holding an identical results.json, took 5m14s. `brute_rerun.log` is identical to `brute.log`: 143 / 3305 / 5,185,660 / 0 failures / 766 / 0 missing / 15,800 / "stored total 1734".
- My own numpy re-implementation (`s6_window.py`, 18 s) reproduces 3,305 valid singles, 5,185,660 (4,5) pairs, 15,800 line-generic pairs and 766 non-line-generic both-in-AP pairs.
- With EXACT Fraction comparison, 0 of the 766 are missing from results.json.
- The authors' truncated lookup set has 1,734 keys, but only 1,467 stored pairs are genuinely half-integral, so 267 keys are spurious (see Problem 3).
- All 766 pairs are re-confirmed (4,5) with the pure-Python test.

## Problems found (in order of severity)

No mathematical problem was found. All remaining issues are textual, and each is fixable in a few minutes.

**Problem 1. Self-contradictory scope sentence in the Statement (must fix).**
- The Statement says: "(and, deleting a point, no 17-point one has h ≤ 9 either). The statement says nothing about extensions by three or more points: ..."
- The parenthetical is correct (St3) and is exactly a statement about 3-point extensions: none beats 4/7, since 68/7 < 10. The next sentence denies this.
- Fix: "The statement says nothing about extensions by **four** or more points: an 18-point ... is NOT excluded here."
- Round 1's P1 was about scope. This sentence was introduced by the revision, and should be exact, because D6 in kb/dead_ends.md will be read from it.

**Problem 2. Wrong description of the "766 pairs" (must fix).**
- "Computer-verified steps" says: "the 766 pairs with both points in APs are all contained in results.json".
- In the window there are 766 + 15,800 = 16,566 (4,5) pairs with both points in APs.
- The 766 are those that are NOT generic points of a single T2 line. The 15,800 line-generic ones are not, and need not be, in results.json.
- Fix: "the 766 (4,5) pairs with both points in APs that are not generic points of a single T2 line are all contained in results.json (exact comparison)".
- Similarly, "checked all 6,876 line pairs" (citing round 1) should read "all 6,876 pairs with both points in APs (589 + 6,287 line-generic)".

**Problem 3. The membership test in bruteforce_check.py is not exact, and the README misdescribes it (should fix).**
- Line 35 builds the lookup set with `int(2*F(a))`, which truncates the quarter-integer stored coordinates. This creates 267 spurious keys, so the test `frozenset((x, y)) not in stored` could report a missing pair as present.
- The README calls "stored total 1734" "a display artifact ... it does not affect the check". In fact the truncated set is the one used for the check.
- The conclusion "0 missing" is nevertheless TRUE: I re-did it exactly (C11).
- Fix: use exact keys, e.g. `{frozenset((2*F(a), 2*F(b))) ...}`, compare with `frozenset((F(x), F(y)))`, and re-run (5 min). Alternatively, correct the README sentence and cite C11 of this review.

**Problem 4. Optional nits carried over from round 1 (P4), still open.**
- (a) "P_x" does not depend on x. Read literally, its definition includes the 14 points of A (237 values), while |P_x| = 223 counts only the non-A ones. Add "∖ A".
- (b) "or a further AP appears" is vacuous in T2.
- (c) "A 3-AP-free subset of size 10 is exhibited in every case": in T0 and T2-generic the subset comes from an abstract argument, and in T1a it is S9 ∪ {y}.
- (d) DEPENDS ON lists K5–K6, which are not used. The intersection points are decided by computation; the linearity argument in Pf9 is only an explanation.

**Problem 5. Cosmetic: stale README text.** The README "Conclusion" still describes `bruteforce_check.py` as a sanity test over [-60, 1120]. The later "Referee round 1 fixes" section supersedes it; delete it or mark it superseded.

## Status of the round-1 requests

| Round-1 item | Status |
|---|---|
| P1 (overclaim) | Fixed. The revision introduced Problem 1. |
| P2 (witnesses not stored) | Fixed. witnesses.json is complete and correct (C8). |
| P3 (independence of the brute force) | Fixed: the new script imports nothing from e757 or extend.py and witnesses every pair in a larger window. It now carries Problems 2 and 3. |
| P4 (optional) | Not addressed (Problem 4). |

## What is needed for ACCEPT

- Edit the proof file for Problems 1 and 2.
- Fix Problem 3, either by making the lookup exact and re-running, or by correcting the README sentence and citing C11.
- Problems 4 and 5 are optional.

No new mathematics or computation is required. This review's C1–C11 verify all computational content of the certificate, including an independent completeness proof (C6) with a positive control (C7). A round-3 referee only needs to check the text edits.
