VERDICT: NEEDS-WORK

# Referee review: L001-abase-two-point-extensions (certificate)

Reviewed: `results/proofs/L001-abase-two-point-extensions.md` (sha256 prefix 738b262a201cfbd0), `experiments/20261014-0640-abase-extensions/` (extend.py 9ad5e923e4c2b2f1, results.json dd1244dfb7d23cb7, bruteforce_check.py, brute.log, README.md), `tests/test_abase_extensions.py`; repo HEAD 03dd847. Review time 2026-10-14T08:04:55Z. Referee scratch: `experiments/referee/L001/`.

## Summary

The certified statement is true and I verified all of it. For every pair of distinct reals x, y not in A_base with B = A_base ∪ {x,y} a (4,5)-set, h(B) = 10. The case split T0 / T1a / T1b / T2 is exhaustive; each step is checked below.

I reproduced every finite computation with three implementations of my own, none sharing code with e757/ or the judge:
1. A formula-based enumeration using a full 1,820-quadruple (4,5) test and a branch-and-bound over Sidon sets that tracks used differences.
2. CP-SAT on the equal-difference conflict structure.
3. A numpy integer scan over exact grids that provably contain every candidate.

All three give:
- |P| = 223 and |P_ok| = 50;
- h(A ∪ {x}) = 9 for all 50 x in P_ok;
- 11,774 T1b candidate pairs;
- exactly the same 1,743 (4,5) pairs as the stored set, with h = 10 for every one.

The frozen judge agrees on 51 sampled sets. The authors' pipeline reproduces a JSON-equal results.json, and their test passes.

The verdict is NEEDS-WORK only because the write-up states things the evidence does not support:
- **The statement overclaims.** It ends "i.e. A_base cannot be extended to a new record", but only 2-point extensions (and, as a corollary, 3-point ones) are covered. An 18-point extension with h = 10 is not excluded.
- **The witnesses are not where the proof says.** It says the explicit 10-subsets are "stored in results.json". They are not; only their count is stored.
- **The cross-check is overstated.** The brute-force check is called "independent", but it imports extend.py's primitives and checked h on only 1 in 500 line-generic pairs.

All three are text fixes. Once they are made the certificate merits ACCEPT, and K13 can be tagged [verified-here].

## Step-by-step check of the argument

Notation:
- A = A_base and B = A ∪ {x,y}.
- P = {v not in A : {v,a,b} is a 3-AP for some distinct a, b in A}. This is the proof's "P_x".
- Q(x) is the same set with A ∪ {x} in place of A.

**S1. Upper bound.** h(B) <= h(A) + 2 = 10, because removing x and y from a Sidon subset of B leaves a Sidon subset of A. h(A) = 8 is [published] (K11) and re-verified here three ways: my branch-and-bound gives 8 with 143 maximum Sidon subsets, CP-SAT gives 8, and the judge gives 8. OK.

**S2. Sidon equals 3-AP-free.** A (4,5)-set B is weak Sidon, so its Sidon subsets are exactly its 3-AP-free subsets (K4 [published], Ma–Tang Lemma 2.3). I re-derived this: in a weak Sidon set the only possible sum collision is 2u = w + z. S2 is needed only for the infinite families (T0, T1a, T2-generic). Every finite case was decided by direct Sidon computations that do not use S2. OK.

**S3. Shape of the new APs.** Every 3-AP of B not inside A contains x or y.
- If it contains exactly one of them, that point lies in P.
- If it contains both, it is {a,x,y} with a in A.

OK.

**S4. Case T0 (no new AP).** Take a maximum Sidon subset S of A. Then S ∪ {x,y} is 3-AP-free, hence Sidon by S2, so h = 10. OK.

**S5. Case T1 (x in P).** "WLOG x" is valid because the statement is symmetric in x and y. (4,5) is hereditary, so A ∪ {x} must be (4,5). Hence x lies in P_ok, and |P_ok| = 50 (re-verified). OK.

**S6. Case T1a (y in no AP of B).** H(B) is H(A ∪ {x}) plus the isolated vertex y, so h(B) = h(A ∪ {x}) + 1.
- h(A ∪ {x}) = 9 for all 50 x, re-verified by branch-and-bound and by CP-SAT, and by the judge on 10 of them.
- This is also forced by Henning–Yeo: f(15) >= ceil(141/17) = 9.

OK.

**S7. Case T1b (y in some AP of B).** Every AP through y has its other two points in A ∪ {x}, so y lies in the finite set Q(x).
- Enumerating {x,y} with x in P_ok and y in Q(x) gives 11,774 unordered pairs.
- 1,743 of them are (4,5), and all have h = 10.

Re-verified three ways (C2, C4, C8). OK.

**S8. Case T2 (x, y not in P, some AP {a,x,y}).** (x,y) lies on one of 42 lines: 14 choices of a, times the choice of which of a, x, y is the midpoint.
- The three roles give slopes 2, 1/2 and -1. So distinct (role, a) give distinct lines, and lines with the same role are parallel.
- Any further new AP must again contain both x and y (otherwise x or y is in P), so it defines a second line.

S8a. **(x,y) on exactly one line.** Then H(B) = H(A) + {a,x,y}, and alpha = 10 iff some maximum Sidon set of A avoids a. This holds for all 14 values of a, re-verified two ways:
- branch-and-bound on A \ {a};
- brute force over all 10- and 11-subsets of the abstract 16-vertex hypergraph.

OK.

S8b. **(x,y) on two or more lines.** After removing x = y and x or y in A, these are 498 ordered intersection points (249 unordered). None is (4,5) (re-verified). The structural reason is linearity (K6): two APs sharing {x,y} give two independent distance coincidences in the 4-set {a, a', x, y}, so it has at most 4 distinct distances. OK.

**S9. Exhaustiveness.**
- No new AP: T0.
- Some new AP contains exactly one new point: that point is in P, so T1. It is T1a or T1b depending on whether the other point lies in an AP.
- Otherwise every new AP contains both points: T2, either S8a or S8b.

Real (not only rational) x, y are covered. The only infinite families (T0, T1a, S8a) are handled by the abstract arguments S4, S6 and S8a. OK.

## Checks performed

All scripts are in `experiments/referee/L001/` and were run from that directory. Each ran as a single process in under one minute.

**C1. Independent primitives (`rcore.py`).** No imports from e757/ or judge/. It provides:
- exact Fraction-to-integer scaling;
- `is45`, a full test of every 4-subset;
- `max_sidon`, a branch-and-bound over points that keeps the set of used positive differences. This is a definition-level Sidon test, not an AP-hypergraph alpha.

Output:
- A_base: 14 distinct points, (4,5), 12 APs, h = 8, 143 maximum Sidon subsets.
- The 12 midpoints are exactly the 12 non-extreme points.
- {1,2,3,5} is not (4,5); {2,3,5,8} is.

**C2. `python3 -I t1_enum.py`** (log `t1_enum.log`; data `t1_out.json`, with a Sidon 10-witness for every pair).
- |P| = 223 and |P_ok| = 50.
- h(A ∪ {x}): {9: 50}.
- T1b candidate unordered pairs: 11,774.
- (4,5) pairs: 1,743, using the full 1,820-quadruple test with no decomposition.
- h distribution: {10: 1,743}.
- Stored 1,743, mine 1,743, symmetric difference 0.
- 997 of the 1,743 pairs have both points in P.

**C3. `python3 -I t2.py`** (log `t2.log`).
- Abstract alpha = 10 for all 14 values of a.
- Intersection points: 512 ordered, 498 after filtering (249 unordered). None is (4,5), and all 498 have at least 2 APs through {x,y}.
- 126 random rational points on the 42 lines (denominator 1,000,003) all have exactly 13 APs. 90 are (4,5) with h = 10. The other 36 are not (4,5); see O1.
- 100 random T1a points (x in P_ok, y generic): all (4,5), h = 10.
- 50 random T0 points: all (4,5), h = 10.

**C4. `python3 cpsat_check.py`** (log `cpsat_check.log`). OR-tools CP-SAT with 1 worker maximizes the number of chosen points, subject to: for every two pairs at equal distance, not all of their points are chosen.
- A: 8, with 12 conflict constraints.
- A ∪ {x}: {9: 50}.
- All 1,743 T1b pairs: (h from branch-and-bound, h from CP-SAT) = (10, 10).

**C5. Frozen judge on 51 sets.** `make_jin.py` writes them to `jin/`: A, 10 sets A ∪ {x} and 40 sets B, each with `claimed_h`. Command: `python3 judge/judge.py experiments/referee/L001/jin/*.json`. Result:
- 51 x "PASS NO-IMPROVEMENT"; any mismatch with `claimed_h` would have been a FAIL.
- A: n=14, h=8, ratio=4/7.
- 10 x n=15, h=9.
- 40 x n=16, h=10.

**C6. Authors' pipeline re-run from a copy** (`rerun/extend_copy.py`). The only change is the output path (diff: line 135 only).
- Same summary: type1_pairs 11,774; type1_45 1,743; Px_size 223; Px_45 50; type2_isect_pts 498; type2_isect_45 0; witness_certified 1,743; all 42 line alphas = 10.
- The new results.json is JSON-equal to the stored one.

**C7. `python3 -m pytest -q tests/test_abase_extensions.py`:** 1 passed.

**C8. `python3 -I scan_check.py`** (log `scan_check.log`). numpy int64 on exact scaled grids; it does not use the partner formula.
- **Part A.** Scan every half-integer in [-1100, 2200]; P lies in [-1056, 2112]. A direct test "v + w = 2u or u + w = 2v" gives exactly the formula sets P (223) and P_ok (50).
- **Part B.** For each x in P_ok, scan every quarter-integer y in [-1912, 3824]. This is the hull of [2 min - max, 2 max - min] over A ∪ {x}, so it contains Q(x), which lies in Z/4.
  - It finds exactly 1,743 (4,5) pairs with y in an AP of B, identical to C2 and to the stored set.
  - A further 1,097,115 (4,5) grid pairs have y isolated (T1a type).
- **Part C (the authors' grid: half-integers in [-60, 1120]).**
  - 1,781 valid singles and 1,455,177 (4,5) pairs.
  - 589 non-line-generic pairs with both points in APs, 0 of them missing from the stored set.
  - 6,287 line-generic pairs.
  - These are exactly brute.log's numbers. I computed h directly for all 6,876: {10: 6,876}. The authors sampled only 1 in 500 of the 6,287.
  - 400 of the numpy (4,5) decisions were re-confirmed by the full pure-Python test.

**C9. Code reading of extend.py.** Correct:
- candidate generation;
- the `pair_ok` decomposition (A, A ∪ {x}, A ∪ {y}, plus the 91 quadruples containing both new points);
- frozenset dedup;
- the intersection solver;
- `witness10` (a 3-AP-free 10-subset, re-checked with `is_sidon`).

Two harmless oddities: the line `if role == 'x_mid': e = (ai, 15, 14)` is immediately overwritten, and `rec_h(h) if False else None` is dead code. As a result the line hypergraphs are not counted in hdist, which matches the README.

## Problems found (in order of severity)

**P1. The statement overclaims (must fix).** The statement reads: "In particular no 16-point (4,5)-set containing A_base has h <= 9, i.e. A_base cannot be extended to a new record."
- Only 2-point extensions are proven.
- 3-point extensions follow as a corollary. A 17-point (4,5)-set containing A_base contains a 2-point extension (heredity), so h >= 10 > 68/7.
- 4-point extensions are not addressed. An 18-point (4,5)-set containing A_base with h = 10 (ratio 5/9 < 4/7) is consistent with h(A ∪ {x,y}) = 10 for every pair.

Fix: replace the "i.e." clause with "i.e. no extension of A_base by two (hence also three) points beats 4/7". This matters because kb/dead_ends.md or STATE could otherwise record a much stronger dead end than was proven.

**P2. False statement about the evidence (must fix).** The proof says each of the 1,743 pairs has "an explicit 3-AP-free 10-subset stored in results.json". In fact:
- results.json stores only [x, y, h] triples. Its keys are Px_45, Px_size, hdist, n_stored, stored, type1_*, type2_* and witness_certified.
- extend.py computes the witnesses (line 129), asserts them, and discards them, saving only the count.

Fix: either store the witnesses, or reword to "recomputed and checked by extend.py (witness_certified = 1,743)". Storing them is cheap; this review's `t1_out.json` already holds a Sidon 10-witness for every pair.

**P3. The cross-check is overstated (should fix).** The proof calls `bruteforce_check.py` an "independent brute-force cross-check", but:
- the script does `from extend import *` and reuses single_ok, pair_ok, witness10 and e757.core, so it is an independent enumeration route, not an independent implementation;
- it checked h on only 1 in 500 line-generic pairs;
- its window [-60, 1120] does not contain most of P or of Q(x).

Its reported numbers are correct: my own code reproduces them exactly in C8, with h computed for all 6,876 pairs. Fix: reword, and optionally cite this review's C2, C4 and C8 as the independent implementations.

**P4. Minor wording and notation (optional).**
- (a) "P_x" does not depend on x. Its definition ("midpoints (a+b)/2 and endpoints 2b-a") omits "minus A", while |P_x| = 223 counts only points outside A. With A included the set has 237 elements.
- (b) T2 refers to "the 498 exceptional points (where two such lines meet, or a further AP appears)". Under the T2 hypothesis any further AP must contain both x and y, so it is a second line. The "or a further AP appears" alternative is therefore empty or belongs to T1. Say so explicitly, as the README already does.
- (c) "A 3-AP-free subset of B of size 10 is exhibited in every case." For T0, T1a and T2-generic the subset comes from an abstract construction (via K4), not exhibited point by point. Say so.
- (d) DEPENDS ON lists K5 (midpoint injectivity), which is not used, and K6 (linearity), which is replaced by computation in S8b. Harmless.

None of P1–P4 affects the truth of the certified statement.

## Observations (not errors)

**O1. Twelve of the 42 lines contain no (4,5) points.** These are the lines x + y = 2a with a in A non-extreme. A_base is midpoint-saturated, so a = (b + c)/2 for some b, c in A. Then x + y = b + c, which gives |x - b| = |c - y| and |x - c| = |b - y| in {x, y, b, c}.
- T2-generic is therefore vacuous on those lines. C3 confirms it: all 36 sampled points on them fail (4,5).
- The live T2 families are the 28 x_mid / y_mid lines plus the two a_mid lines with a = 0 or a = 1056.

**O2. Bookkeeping.** All 1,743 non-line-generic (4,5) extensions with both new points in APs come from T1b; no intersection point is (4,5). There are 30 non-vacuous line families and 50 T1a families. The omega counts (124 / 6,484 / 6,609) cannot be reconciled from material on disk, and the README says so honestly.

**O3. Where a counterexample could have lived.** T1a could not produce a record, since h(A ∪ {x}) >= 9 is forced by Henning–Yeo. The only possible locations were T1b and S8a, and both are verified.

## What is needed for ACCEPT

Edit the proof file:
- fix P1 by restricting the "i.e." clause;
- fix P2 by storing the witnesses or rewording;
- fix P3 by rewording "independent";
- optionally fix P4.

No new computation is needed; this review verifies all of the computational content.
