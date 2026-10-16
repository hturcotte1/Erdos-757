VERDICT: ACCEPT

# Referee review, round 3: L005-ext14-all-two-point-extensions (certificate)

- **Referee:** referee subagent, round 3, 2026-10-16, 01:18 to 01:41 UTC.
- **Claim reviewed:** `results/proofs/L005-ext14-all-two-point-extensions.md`, the version with STATUS "revised 2026-10-16 01:17 UTC after referee round 1".
- **Files reviewed.** sha256 prefixes, identical at the start and at the end of this review:

| File | sha256 prefix |
|---|---|
| proof `L005-...md` | a72d65ec438734b5 |
| `experiments/20261015-2340-ext14-all/extend_all.py` | 2f01a10abf32587c |
| `results.jsonl` / `results.json` | 7dfd7223b1f90c36 / 71bd0cf7c0103dff |
| `data/census_n14_m12_classes.jsonl.gz` | 7890395ed215ec27 |
| `bruteforce_sample.py` / `bruteforce_sample_results.json` | 35aa86c8ff0d04dc / df5bdd10b38affc6 |
| experiment `README.md` | 4a2c2f870a00145a |
| `tests/test_ext14_all.py` | 126dcb7bb50f5b16 |
| `judge/judge.py` | e061f0e2072e7d09 (= judge.sha256) |

- **Scratch folder:** `experiments/referee/L005-round3/`.
- **Independence.**
  - `ate.py` (my independent check) imports nothing from `e757/`, `judge/` or the authors' folder.
  - `rerun_authors.py` and `compare_sets.py` deliberately load the authors' `extend_all.py` by path. The first is the requested rerun; the second regenerates the authors' pair sets for a set-level comparison.
  - The frozen judge was only executed, on claim files in my scratch folder.
- **Load.** Everything ran at nice 10 with at most 2 processes. Every foreground command took under 10 minutes; total compute was about 7 CPU-minutes.

## Summary

The certified Statement is correct: for every one of the 2,910 saturated extremal 14-point classes A of L004, and every pair of distinct reals x, y not in A such that B = A u {x,y} is a (4,5)-set, h(B) = 10. Its two corollary sentences are also correct, given L004 and Henning–Yeo.

**What I verified.**
- **Case analysis.** I re-derived the T0/T1a/T1b/T2 split. It is sound and exhaustive. In T2, linearity makes H(B) = H(A) + {a,x,y} at *every* (4,5) point, so the 42 abstract line computations alone settle T2.
- **Code audit.** I audited `extend_all.py` line by line. Arithmetic is exact, the candidate sets are complete, the (4,5) tests cover every 4-subset, and every T1b value h = 10 is backed by an asserted Sidon witness.
- **Rerun.** I reran the authors' code, unmodified, on 31 classes of my choosing. These include A_base (class 2440) and the five classes 729, 857, 960, 1951 and 2437, which have a non-admissible point v with h(A u {v}) = 8. All stored fields were reproduced exactly (0 mismatches).
- **Independent check of my own design (ATE).** This is an arrangement-type enumeration over the whole (x,y)-plane:
  - it uses every additive relation line, not only 3-AP relations, and no T0/T1/T2 split;
  - (4,5) is tested by counting distances in all 1,820 4-subsets;
  - h(B) is computed from the Sidon definition over all C(16,10) and C(16,11) subsets.

  On 13 classes I found 0 deficient types. In all 13 classes, the set of (4,5) pairs equals the authors' T1b set exactly (22,330 pairs in total), and the admissible single extensions equal the stored `n_single_45`.
- **Controls and judge.** Positive controls (13-point sets "A minus one point") confirm that ATE detects deficits when they exist. The frozen judge agrees on 9 samples: 7 PASS with h = 10, and 2 expected FAILs.
- **Numbers and fixes.** Every number quoted in the proof matches the stored outputs. All round-1 text problems have been fixed.

I found no mathematical or computational problem. Only optional editorial remarks remain; none of them makes a load-bearing sentence false.

## The proof, step by step (re-derived)

1. **Affine invariance.** Being (4,5), h, H(A) and m are invariant under x -> qx+t with q != 0, including reflection, and A -> A u {x,y} commutes with these maps. L004's classes are taken up to reflection as well, so one integer representative per class suffices. Correct.
2. **h(B) <= h(A)+2 = 10.** A Sidon subset of B meets A in a Sidon subset of A. Correct; this is the round-1 fix.
3. **K3 and K4.**
   - B is (4,5), so B is weak Sidon. Re-proved: if a+b = c+d with a, b, c, d distinct, then |a-c| = |d-b| and |a-d| = |c-b|, so that 4-set has at most 4 distances.
   - Hence a subset of B is Sidon iff it is 3-AP-free.

   Correct.
4. **The split.**
   - A new 3-AP contains x or y.
   - If it contains exactly one of them, that point is in P_x (case T1; we may assume it is x, by the symmetry of the Statement).
   - Otherwise every new AP contains both x and y, so it is {a,x,y} with a in A, in 3 possible roles (case T2).
   - If there is no new AP at all, we are in case T0.
   - x in P_x puts x in a new AP, so T0 and T1 are disjoint.

   The split is exhaustive. Correct.
5. **T0.** S u {x,y} is 3-AP-free for any maximum S. Correct.
6. **T1a.** y is an isolated vertex of H(B), so alpha(H(B)) = alpha(H(A u {x})) + 1. A u {x} is a subset of B, hence (4,5), hence h = alpha. Correct. The computed value 9 for all 141,153 admissible x is also implied by f(15) = 9.
7. **T1b.** The AP through y has its other two points in A u {x}, so y is in candidates(A u {x}). This set is finite and is enumerated exactly. Correct.
8. **T2.**
   - Two APs {a,x,y} and {a',x,y} with a != a' share the pair {x,y}. That contradicts K6. Re-proved: the 4-set {a,a',x,y} then has at most 4 distances.
   - So at every (4,5) T2 point, not only at generic points, H(B) = H(A) + {a,x,y} for exactly one of the 42 lines.
   - alpha(H(A)+e) = max(alpha(H)+1, alpha(H-a)+2). This equals 10 iff some maximum independent set avoids a.
   - Hence the 42 abstract computations per class cover all of T2. The test of the line intersection points is redundant, but consistent: 0 of the 1,444,980 points are (4,5).

   Correct.
9. **The corollary.**
   - Suppose C is a 16-point (4,5)-set with h <= 9 containing a 14-point A with h = 8 and m = 12. Then C = A u {x,y} with C (4,5), which contradicts the Statement.
   - "Equivalently" uses the fact that m is 11 or 12 for 14-point (4,5)-sets with h = 8: m <= 12 by K5, and m >= 11 by K8 (17*6 <= 70 + 3m).
   - Also, h <= 9 at n = 16 is exactly h/16 < 4/7.

   Correct; see remark N1.
10. **Remark U1** (not load-bearing).
    - Suppose a lies in every maximum independent set.
    - Then tau(H-a) = 13 - 7 = 6, and H-a is linear and F7-free as a subhypergraph, with at most 12 edges.
    - Henning–Yeo then gives 102 <= 65 + 36 = 101, a contradiction.

    Correct, and it holds even if a is isolated.
11. **Scaling.** At scale 4, A is a subset of 4Z, every x in P_x is even, and all candidates of A u {x} are integers. The code asserts this. Correct.

## Checks performed

All commands were run from `experiments/referee/L005-round3/` unless stated otherwise.

### C1. Stored outputs against every number in the proof (inline python over results.jsonl and results.json)

- **Rows.** 2,910 rows with ids 0..2909, and `results.json` rows equal `results.jsonl`.
- **Counters.** All match the proof:
  - singles: 141,153 in total, 32 to 61 per class;
  - (4,5) T1b pairs: 4,970,208;
  - T2 lines: 122,220, all with alpha = 10;
  - T2 intersection points: 1,444,980 in total, 480 to 498 per class, 498 for class 2440; 0 of them (4,5);
  - maximum Sidon sets: 137 to 150 per class, 143 for class 2440.
- **Histogram.** {10: 5,233,581}, which equals 141,153 + 4,970,208 + 122,220.
- **Per-row flags.** Every row has hA = 8, min_h = 10, no records, t2_line_h = [10] and t2_precheck false. No RECORD_CANDIDATES.txt exists.
- **Timing.** `run.log` ends at 1,843.8 s wall clock. The per-class seconds sum to 3,677.6 s, about 1.0 CPU-hour, as claimed.
- **A_base.** Class 2440 is literally A_base. The figure of 143 maximum Sidon sets is in L001's experiment outputs and reviews, and in K17.

### C2. Rerun of the authors' code (`rerun_authors.py`, 19 s wall clock with 2 processes)

The unmodified `extend_all.process` was run on 31 classes:
- a fixed list: 2440, 729, 857, 960, 1951, 2437, 2879 (480 intersection points), 1524 (min singles and min T1b), 2564 (max T1b), 2096, 2621, 1631 (max P_x), 1007, 235 (137 maximum Sidon sets), 2892 (150), 2697, 226;
- 14 random classes (seed 20261016): 405, 548, 715, 948, 1220, 1688, 1826, 2118, 2165, 2253, 2306, 2412, 2734, 2804.

Every output field except `secs` equals the stored row: **0 mismatches** (`rerun_authors_out.json`).

The `--abase-test` literal set gives:
- |P_x| = 223, 50 singles, 11,774 T1 pairs, 1,743 (4,5) T1b pairs;
- 42 lines, all with alpha = 10;
- 498 intersection points, 0 of them (4,5);
- 143 maximum Sidon sets;
- histogram {10: 1835} = 50 + 1,743 + 42.

### C3. Regression test

From the repo root, `python3 -m pytest -q tests/test_ext14_all.py`: 2 passed.

### C4. Independent check of my own design: arrangement-type enumeration (`ate.py`; 287 CPU-s in total)

**Method.**
- **Relation lines.** For B = A u {X,Y}, every relation u1+u2 = u3+u4 between two different 2-multisets of the 16 symbols that involves X or Y is a line aX+bY = c. I generated all 9,180 multiset pairs and normalized and de-duplicated the lines.
- **Why types suffice.** Every distance equality in B, and every Sidon failure of any subset of B, is such a relation. So distinctness, the (4,5) property and h(B) depend only on the set of lines through (x,y).
- **Line classes.**
  - E: the relation reduces to u = v, giving X = a, Y = a or X = Y. Asserted to be exactly these 29 lines in every class.
  - F: some relation on the line has 4 distinct symbols. Then that 4-set has at most 4 distances, so no point of the line is (4,5).
  - G: the line carries only 3-AP relations.
- **Coverage.** A non-excluded point is in one of three situations:
  - it lies on no line: covered by one generic plane point;
  - it lies on exactly one line: covered by a representative of that line, which is verified exactly to lie on no other line;
  - it lies on two or more lines: it is either on an F line, hence not (4,5), or an intersection of two G lines. All G x G intersections are enumerated.
- **Direct tests.** Every representative and every non-excluded G x G point was tested directly:
  - (4,5) by counting distinct distances in all 1,820 4-subsets (numpy, exact int64);
  - h(B) from the definition (Sidon iff all positive differences are distinct): a Sidon 10-subset exists among all C(16,10), and none exists among all C(16,11).
  - h(A) = 8 was computed the same way, from all 8-subsets and 9-subsets.

  This uses neither the 3-AP reduction, nor h(A) = 8 for the upper bound, nor the T-case split.

**Scope.**
- Classes: 2440, 729, 2879, 1524, 2564, 405, 2804, plus six classes drawn with seed 777: 941, 1107, 1511, 1828, 1829, 2360.
- Command: `python3 ate.py ate_*.jsonl <idx list>`.

**Results** (0 deficits in every class):

| class | lines E/F/G | vertical G lines, (4,5) / stored n_single_45 | slanted G lines (4,5) | G x G points | (4,5) pairs, unordered / stored n_t1b_45 | h values |
|---|---|---|---|---|---|---|
| 2440 | 29/1715/166 | 50 / 50 | 30/30 | 8,948 | 1,743 / 1,743 | all 10 |
| 729 | 29/1565/124 | 36 / 36 | 30/30 | 5,277 | 1,066 / 1,066 | all 10 |
| 2879 | 29/1625/142 | 45 / 45 | 30/30 | 6,744 | 1,462 / 1,462 | all 10 |
| 1524 | 29/1279/116 | 32 / 32 | 30/30 | 4,677 | 854 / 854 | all 10 |
| 2564 | 29/1809/180 | 61 / 61 | 30/30 | 10,373 | 2,496 / 2,496 | all 10 |
| 405 | 29/1753/168 | 49 / 49 | 30/30 | 9,149 | 1,749 / 1,749 | all 10 |
| 2804 | 29/1827/168 | 53 / 53 | 30/30 | 9,149 | 2,013 / 2,013 | all 10 |
| 941 | 29/1739/152 | 47 / 47 | 30/30 | 7,621 | 1,597 / 1,597 | all 10 |
| 1107 | 29/1533/138 | 41 / 41 | 30/30 | 6,400 | 1,285 / 1,285 | all 10 |
| 1511 | 29/1715/180 | 49 / 49 | 30/30 | 10,373 | 1,749 / 1,749 | all 10 |
| 1828 | 29/1731/180 | 58 / 58 | 30/30 | 10,373 | 2,230 / 2,230 | all 10 |
| 1829 | 29/1811/176 | 54 / 54 | 30/30 | 9,957 | 2,105 / 2,105 | all 10 |
| 2360 | 29/1671/168 | 54 / 54 | 30/30 | 9,149 | 1,981 / 1,981 | all 10 |

**Further results.**
- **Generic plane point.** It is (4,5) with h = 10 in all 13 classes.
- **Representatives.** All 21,773 F-line representatives are non-(4,5), as the lemma requires. All 1,648 (4,5) G-line representatives have h = 10.
- **The F-line lemma at intersection points.** Of the 108,190 G x G points, 29,622 lie on an F line. Each of these was tested directly, and none is (4,5).
- **Symmetry.** Every (4,5) point (x,y) has its mirror (y,x) in the set.
- **Slanted G lines.** There are always exactly 30 of the 42 T2 lines. The 12 lines X+Y = 2a with a a midpoint of A are F lines, because X+Y = b+c. Generic points of those 12 lines are therefore never (4,5); the authors' abstract alpha = 10 for them is harmless, since it covers a superset.

### C5. Set-level comparison (`compare_sets.py`, log `compare_sets.log`)

For each of the 13 classes, the authors' (4,5) T1b pairs were regenerated with their own `candidates` and `ndist`, replicating their loop.

My ATE pair set equals the authors' set exactly, as sets of unordered rational pairs in the original coordinates, in **13/13** classes. The ATE count of vertical G lines with a (4,5) representative equals the stored `n_single_45` in 13/13 classes. Result: "ALL OK".

### C6. Positive controls (`ate.py --control`)

For classes 2440 and 729, I ran ATE on A minus min(A) and on A minus the 6th smallest point. Each is a 13-point set with h = 8, so the target is 10, and deficits must exist; for example, the line X = p gives A u {y}, which has h = 9.

ATE flagged 52, 53, 38 and 38 deficient types. Each list includes the whole lines X = p and Y = p and dozens of isolated points with h = 9. So the pipeline does detect deficiencies.

### C7. Frozen judge

From the repo root I ran `python3 judge/judge.py experiments/referee/L005-round3/jclaims/<file>` (`judge_results.txt`).

- **PASS NO-IMPROVEMENT, n = 16, h = 10 (7 of 7):**
  - ATE pairs from classes 2440, 1524, 2564, 1829 and 941;
  - a T1a sample: A_base plus the admissible x = 521/2 and a generic y;
  - a T2 sample: A_base plus a generic point of the line y = 2x - 136.
- **FAIL, not a (4,5)-set (2 of 2 expected negatives):**
  - a point of the F line X - Y = -136;
  - x = 349, which lies on the F line 246 + X = 272 + 323. This was my first, mistaken T1a pick, and it shows that not every point of P_x is admissible.

### C8. Census hypotheses

Over all 2,910 lines of the census, every line has:
- 14 distinct sorted integers;
- exactly 12 3-APs, whose midpoints are exactly the 12 non-extreme points;
- the stored fields n = 14, m = 12 and h = 8.

0 bad lines. h = 8 and (4,5) were also recomputed from the definitions for the 13 ATE classes.

### C9. The cited supplementary evidence

**Brute force** (`bruteforce_sample_results.json`). The file confirms the proof's figures:
- 41 classes, 105,720,197 (4,5) pairs, 0 failures, 0 fallbacks;
- 502,942 explicit witness verifications;
- `singles_match_inside` is true in all 41 classes;
- 700 s.

Code read: the brute-force part imports neither `e757` nor `extend_all`, and its bitmask witness logic is sound.

**Round-1 artifacts** (`experiments/referee/L005-ext14-all-two-point-extensions/summary.json`). They exist and say what the proof says:
- Route C: 2,910 classes, 0 counter mismatches, T1b histogram {10: 4,970,208};
- Route L: 2,910 classes, 1,176,308 isolated locus points, 0 of them (4,5).

## Code audit of `extend_all.py`

- **Candidate sets.** `candidates(P)` adds (a+b)/2, 2a-b and 2b-a for every pair, then removes P. It is used both for P_x and for the T1b partners of A u {x}, so both sets are complete. The integrality assertion holds at scale 4.
- **The (4,5) test** is complete:
  - A's own 1,001 4-subsets are asserted;
  - `single_ok` covers {v,a,b,c} for v = x and v = y;
  - `pair_ok` covers {x,y,a,b}.
- **Search routines.**
  - `has_indep` checks each edge when its largest vertex is added, which is correct for any labelling.
  - `alpha_masks` is exact.
  - `all_max_indep` enumerates every maximum independent set.
- **T1b.** Each value h = 10 rests on an exhibited 10-subset asserted Sidon by the sums test, including the 2x sums. The run completed, so all 4,970,208 assertions held.
- **T2 hypergraph.** It is H(A) + {a,14,15}, with a's index taken in sorted A, which is correct. The labels of x and y do not matter.
- **Line intersections.** All non-parallel pairs of lines are intersected, and the points with x = y or with x or y in A are excluded.
- **Bookkeeping.** `seen` only de-duplicates unordered pairs and does not affect coverage. `random` is imported but unused, and there is no randomness.
- **Resume logic.** It cannot have produced duplicates: the 2,910 class ids are all distinct.

## Problems found (in order of severity)

**No blocking problem.** Every load-bearing step is verified, and every quoted number is reproduced. The remarks below are optional editorial improvements. None of them makes a load-bearing sentence false.

- **N1. A dependency left implicit.** The "equivalently ... m = 11" clause needs m >= 11 for 14-point (4,5)-sets with h = 8. This comes from Henning–Yeo (K8, [published]). It is available through L004's Statement ("necessarily with m=11"), and L004 is in DEPENDS ON. Citing K8 explicitly would make L005 self-contained.
- **N2. Compressed wording, cross-check (i).** The proof says "each with a certified 3-AP-free Sidon 10-subset". In `bruteforce_sample.py`:
  - for most pairs, 3-AP-freeness is certified by the (sound) bitmask argument, and Sidon then follows by K4;
  - the explicit Sidon check covers 502,942 pairs (pairs with an AP through x and y, plus every 997th pair).

  The README states this precisely. Non-load-bearing.
- **N3. Ambiguous wording, cross-check (ii).** In round 1, it was Route C that reproduced the seven per-class counters. Route L computed the deficient locus (0 (4,5) points) and matched only the counts of maximum Sidon sets. The sentence "both on all 2,910 classes, with all seven per-class counters ... reproduced" can be read as crediting both routes.
- **N4. Loose bound.** "Denominators dividing 12" is true but not tight. In the original integer coordinates the T2 intersection points are (2a+b)/3, (a+2b)/3 or (4b-a)/3, with denominators dividing 3. Harmless.
- **N5. Inherited risk (declared).** The Statement covers all saturated extremal 14-point sets only through L004's completeness. L004 is ACCEPTED, but its completeness was checked independently by sampling (719 prefixes and cube refutations), not by a full second enumeration. L005 states this dependency correctly, and nothing in L005 adds to the risk.

## Verdict rationale

ACCEPT. Four lines of evidence support the claim:
- the case analysis is mathematically complete, and in case T2 it is even forced by linearity;
- the certificate code is correct by audit and reproduces exactly on 31 classes chosen by this referee;
- a check of my own design that shares no reduction with the authors' (whole-plane line arrangement, definitional (4,5) and Sidon tests) agrees as sets with the authors' enumeration on 13 classes and finds no deficiency;
- round 1's two independent full-census routes, whose artifacts I confirmed, cover all 2,910 classes.

The remaining remarks N1 to N4 are editorial, and N5 is a declared dependency.
