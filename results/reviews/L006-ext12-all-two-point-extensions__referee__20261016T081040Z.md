VERDICT: ACCEPT

# Referee report, round 2: L006-ext12-all-two-point-extensions

Claim: results/proofs/L006-ext12-all-two-point-extensions.md (revised 07:38 UTC after round 1). Scratch folder: experiments/referee/L006-round2/. Wall time: about 32 minutes. Resources: at most 2 processes, nice 5 (the sweep script renices itself to 5).

## Summary

**The claim.** Every (4,5) two-point extension of each of the 54,243 extremal 12-point classes of L002 has h = 9. Hence no 14-point (4,5)-set with h <= 8 contains a 12-point subset with h = 7.

**Verdict.** I re-derived the case analysis and found it sound and exhaustive. I re-audited `extend12_all.py` and found no defect. The stored data reproduce every number in the proof.

**Checks performed.**
- **Rerun.** I reran the unmodified script end to end on 437 classes of my own choosing, none of which round 1 touched. All 437 rows are identical to the stored rows.
- **Route V (my own design).** It enumerates the complete line arrangement of all sum relations of A u {X, Y}, so it uses no T0/T1/T2 split and no hand-written candidate formulas. It computes h from the Sidon definition alone.
  - On 201 classes it agrees exactly with the authors' code: the same set of 188,413 (4,5) extension pairs, the same admissible singles, the same counters, and h = 9 at every one of 395,936 evaluated (4,5) types.
  - A positive control detects the deficient extensions of A_base minus 2 points in 7 of 7 cases.
- **Further independent checks.**
  - A CP-SAT ILP gives h = 9 on 1,005 sampled extensions.
  - The frozen judge passes 9 of 9 samples.
  - A full-census pass with my own Sidon code confirms (4,5), m = 10, h = 7 and "no universal vertex", which is exactly what decides every T2 line, for all 54,243 classes.
  - All 91 two-point deletions of each of the 2,910 saturated 14-point classes have h = 8, consistent with the theorem's consequence and with K47.
- **Round-1 issues.** All required fixes of round 1 have been made correctly.

**What remains.** Only non-blocking editorial remarks: the scope of one count, one loose citation in a non-load-bearing remark, a missing K8 in DEPENDS ON for a parenthetical gloss, and a README range. None affects a step or misstates the evidence.

## Steps of the proof, re-derived

1. **Affine invariance.** Being (4,5), h and the AP structure are invariant under x -> qx + t (q != 0, reflection included), and A -> A u {x,y} commutes with these maps. So one representative per class suffices. Correct.
2. **Upper bound.** h(B) <= h(A) + 2 = 9: a Sidon subset of B meets A in a Sidon subset of A. Correct.
3. **Exhaustive split.** Every 3-AP of B that is not an AP of A contains x or y. If it contains exactly one of them, that point forms a 3-AP with two points of A, so it lies in P_x. Hence either some new AP has exactly one new point (case T1, WLOG x in P_x), or every new AP contains both new points, so it is {a, x, y} with a in A in one of 3 roles (case T2), or there is no new AP (case T0). Correct.
4. **T0.** H(B) = H(A) plus two isolated vertices, so alpha = 9. B is (4,5), hence weak Sidon (K3), so h = alpha (K4). Correct.
5. **T1a** (y in no new AP). h(B) = h(A u {x}) + 1, and A u {x} is (4,5) as a subset of B. The value h(A u {x}) = 8 is computed for every admissible x. It also follows without computation from Henning-Yeo: every 13-point (4,5)-set has h >= ceil(123/17) = 8. Correct.
6. **T1b** (y in a new AP).
   - That AP's other two points lie in A u {x}, so y is in `candidates(A u {x})`; the candidate set is complete.
   - The (4,5) property of B is decided by four tests: A (asserted), `single_ok(x)`, `single_ok(y)` and `pair_ok(x, y)`. Together they cover all 4-subsets.
   - Each exhibited 9-subset is asserted Sidon directly (`h_exact_B`), so this case does not even need K4.
   - Correct.
7. **T2, generic point of a line.**
   - If x, y are not in P_x and (x, y) lies on exactly one of the 36 lines, then H(B) = H(A) + {a, x, y}.
   - Hence alpha = max(alpha(H) + 1, alpha(H - a) + 2), which is 9 iff some maximum independent set avoids a.
   - By Lemma U this holds for every vertex of every class. The lemma applies Henning-Yeo (K8) to H - a, which is 3-uniform, linear (K6) and F7-free (K7), with (n, m, tau) = (12, 10, 5) and minimum degree >= 1. My census pass confirms it numerically for all 54,243 classes (check R10).
   - So this case is proved both by theory and by computation. Correct.
8. **T2, non-generic points.**
   - At a non-generic point, either x or y lies in P_x (case T1), or the point lies on a second T2 line. Two APs {a,x,y} and {a',x,y} with a != a' would share {x,y}, which contradicts linearity (K6). The code also tests every intersection point exactly.
   - The 10 lines x + y = 2a with a non-extreme are parallelogram lines, since a is the midpoint of some b, c in A and then x + y = b + c. No point on them is (4,5). Route V finds exactly 26 lines with (4,5) generic points in every class, as this predicts.
   - Correct.
9. **Exhaustiveness.** Correct; it is also confirmed by Route V, which does not use the split (check R5).
10. **Consequence.**
    - Let A be a 12-point subset of a 14-point (4,5)-set B with h(B) = 8. Then A is (4,5) and h(A) >= f(12) = 7 (K41, or Henning-Yeo).
    - h(A) = 7 is impossible: A would be a census class (L002) with a (4,5) extension B of h = 8.
    - Hence h(A) = 8.
    - The gloss "non-saturated (m=11)" uses m >= 11, which is Henning-Yeo (see E3).
    - The by-product about one-point extensions is also immediate from f(13) = 8.
    - Correct.
11. **Remark arithmetic.** 85 <= 55 + 30 - 3 deg a forces deg a = 0. Every vertex has degree >= 1: non-extreme points are midpoints (m = 10), and the two extreme points are endpoints of the APs whose midpoints are the second smallest and second largest points. Correct.

## Code audit (experiments/20261016-0330-ext12-all/extend12_all.py, sha256 b4600c1e...d968db0, as in round 1)

I read the code line by line, independently of round 1, and reached the same conclusions.
- **`ndist`.** The 4-point fast path lists all 6 pairs.
- **`ap_triples`.** Uses integer midpoints of sorted distinct integers; negative values are handled correctly by Python's `%` and `//`.
- **`has_indep`.** Masks are bucketed by their largest vertex and checked when that vertex is added. The pruning `size + n - i < target` is sound. `alpha_masks` and `all_max_indep` are exact.
- **`candidates`.** Covers (a+b)/2, 2a - b and 2b - a for every pair, minus the set. Integrality is asserted; x in P_x is even after the x4 scaling.
- **T1b deduplication.** `seen` deduplicates unordered pairs. A non-(4,5) pair is skipped consistently in both orders.
- **T2.**
  - The lines are y = 2x - a, y = (x + a)/2 and y = 2a - x.
  - Same-slope lines are distinct, so only lines of different slopes meet.
  - The exclusions x = y, x in A and y in A are applied before the (4,5) test, which is done in integers after clearing denominators.
- **Driver and data.**
  - Asserts are active (no `-O`), and the resume-from-jsonl logic is correct.
  - Class ids form a permutation of 0..54242 (R1).
  - `git diff e94f53d a982863`: the only change between the first 280 classes and the rest is the 3-line ndist fast path. The file is unchanged since a982863.
  - The census file realized_n12.json.gz (sha256 e0e2584b...) has a single commit, a887219 (2026-10-14 11:00 UTC), which predates the three L002 referee reviews.

## Checks performed (all scripts and logs in experiments/referee/L006-round2/)

**R1. Stored rows vs census and the proof's numbers.** Command: `python3 -I check_rows.py` (check_rows.log). Results:
- 54,243 rows; class ids 0..54242; 0 set mismatches against the census; 0 failures of the per-row invariants:
  - hA = 7, t2_line_h = [9], t2_lines = 36, t2_isect_45 = 0, records = [], min_h = 9, no core vertex;
  - the histogram has the single key 9, with count n_single_45 + n_t1b_45 + 36.
- Totals and ranges:
  - n_single_45 = 1,887,566 (21..46 per class);
  - n_t1b_45 = 51,264,727 (424..1,395);
  - t2_isect_pts = 19,247,288 (334..356);
  - t2_isect_45 = 0;
  - n_max_sidon 48..63;
  - T2 line hypergraphs 1,952,748;
  - evaluated values 55,105,041.

  All equal the proof and summary.json.
- data/ext12_all_rows.jsonl.gz equals the local results.jsonl, `secs` excepted.
- results.json and results.jsonl are git-ignored (.gitignore lines 37 and 39), as the proof says.

**R2. Unmodified rerun on 437 classes of my own choosing.** Commands: `python3 -I make_subset.py`, then `python3 experiments/20261016-0330-ext12-all/extend12_all.py experiments/referee/L006-round2/rerun_subset.json.gz experiments/referee/L006-round2/rerun_out 2`, which runs the whole script, including main and Pool, unmodified. Then `python3 -I compare_rerun.py` (compare_rerun.log).
- **Class choice.** All classes are disjoint from the 875 classes round 1 touched:
  - 400 random classes (seed: the first 8 bytes of sha256("L006 referee round 2, 2026-10-16"));
  - 38 stress classes: the 3 smallest and 3 largest remaining values of each of n_single_45, n_t1b_45, t2_isect_pts, n_max_sidon, Px_size, t1_pairs and secs, plus classes 280-283 (the first ones after the restart), 54240 and 54242;
  - 437 distinct classes after one overlap.
- **Run.** 111 s with 2 processes. Summary: hist_min_h {9: 437}, 0 record candidates, all hA = 7.
- **Result.** 437/437 rows identical to the stored rows in all fields except the class index (re-mapped) and secs.

**R3. Acceptance mode.** Command: `python3 extend12_all.py x known_out 1 --known` (known_mode.log).
- '12': 62 maximum Sidon subsets / 34 singles / 893 T1b pairs; '12b': 60 / 35 / 933; '12c': 60 / 36 / 974.
- All three: T2 alpha [9], min_h 9, no core vertex, no records.

These match the proof and the README table.

**R4. The revised brute-force description vs bruteforce_sample.py and its JSONs.**
- The wording requested by round 1 is now accurate:
  - the grid is integer pairs in x4 coordinates (lines 15 and 23);
  - the window is [min - span, max + span] (DIV = 1, line 16);
  - h is checked only for T1b-type pairs (line 58) and for 2,000 sampled T2-type pairs (lines 53-56);
  - the h routine is imported from extend12_all.
- Every quoted number agrees with bruteforce_sample_results.json and bruteforce_sample_results_random.json:
  - 20,252,381 / 11,128,510 / 14,730,123 (4,5) pairs in the windows;
  - 772 / 804 / 845 T1b pairs in the windows, with 121 / 129 / 129 outside;
  - 36,891 / 26,054 / 30,790 T2-type pairs;
  - 106..130 T1b pairs outside the window over the six classes.
- bf_known.log and bf_random.log are now tracked (`git ls-files`; force-added in 209a04c).

**R5. Route V, design.** Script: route_V.py, my own code; it imports neither e757, the authors' code nor the judge.
- **Relations.** B = A u {X, Y} is symbolic: points are linear forms in (x, y, 1). For all 105 x 104 / 2 pairs of distinct multisets {p,q} != {r,s}, the relation p + q = r + s is classified after cancellation:
  - DEG: it reduces to u = v;
  - AP: 2u = v + w with u, v, w distinct;
  - PAR: u + v = w + z with 4 distinct points.

  Each relation involving X or Y defines a line in the (x, y)-plane. The program groups relations by normalized line: 843 to 1,255 lines per class.
- **What depends on the relations.** Distinctness, the (4,5) property and the Sidon property of every subset depend only on which relations hold.
- **Pruning.** A PAR relation gives |u - w| = |z - v| and |u - z| = |w - v|, hence at most 4 distances. So no point on a DEG or PAR line is a distinct (4,5) extension.
- **Completeness.** A distinct (4,5) point lies on no line (the generic type), on exactly one line, which must be a pure-AP line (then it has that line's generic type), or on two or more pure-AP lines (then it is a vertex).
- **What is evaluated.** One generic point of the plane, one generic point on each pure-AP line (verified exactly to lie on no other line), and every intersection of two non-parallel pure-AP lines. At each point, distinctness and (4,5) are tested from scratch (all 4-subsets containing x or y, with A asserted (4,5)). h is computed by an exact maximum-Sidon branch-and-bound (distinct positive differences), with no use of 3-APs.

**R6. Route V, positive control.** Command: `python3 -I route_V.py '[[0,1056],[243,249],[136,596],[286,400],[246,528],[200,298],[272,323]]' routeV_control.jsonl 2 --control`, then `check_control.py` (routeV_control_summary.log).
- The inputs are A' = A_base - {u, v}. For each, h(A') = 8 and the target is 10.
- Route V reports 614 to 2,853 deficient types per set, with min h = 8.
- In 7/7 cases, (u, v) itself is reported as a deficient vertex: there B = A_base and h = 8. The lines through (u, v) are reported deficient with h = 9.

So the method detects deficient extensions when they exist.

**R7. Route V on 201 classes, with an exact comparison.**
- **Classes.** The 3 known classes 20392, 23942 and 18917, the 38 stress classes, and 160 random classes from R2 (seed 4242).
- **Commands.** `python3 -I route_V.py routeV_ids.json routeV_main.jsonl 2` (630 s, routeV_main.log). Then `python3 -I compare_V.py routeV_main.jsonl` (compare_V.log). compare_V.py imports the authors' `process(..., want_pairs=True)` only to obtain their exact pair sets.
- **Results.** 201/201 classes agree on every check:
  - hA = 7;
  - min h = 9 and 0 deficient types;
  - the generic cell has h = 9;
  - the number of (4,5) generic vertical lines equals n_single_45, and so does the number of horizontal ones;
  - the number of (4,5) vertices equals 2 x n_2ext ordered, n_2ext unordered;
  - **the set of (4,5) vertex pairs equals the authors' T1b set exactly** (as unordered pairs of rationals), and t2_isect_45 = 0;
  - the x-values of the (4,5) generic vertical lines equal the authors' admissible singles exactly.
- **Totals.**
  - 188,413 (4,5) pairs compared exactly;
  - 1,064,239 vertices tested: 376,826 (4,5), 634,846 not (4,5) and 52,567 not distinct;
  - h histogram over all 395,936 evaluated (4,5) types: {9: 395,936};
  - exactly 26 diagonal lines are pure-AP in every class, all with (4,5) generic points.

**R8. ILP for h (OR-tools CP-SAT, 1 worker).** Command: `python3 -I ilp_h.py` (ilp_h.log).
- **Model.** Maximize the sum of z over B, with one constraint z_S <= |S| - 1 for every sum coincidence p + q = r + s with distinct multisets; this is the Sidon definition. The optimal subset is re-checked Sidon.
- **Samples.** 1,005 extensions over the 201 classes: 402 random vertex pairs, 201 T1a-type points (admissible x, generic y) and 402 T2-type generic points (x the midpoint of a and y; x + y = 2 min A). All are (4,5) by a check of all 1001 4-subsets.
- **Results.** The ILP gives h = 9 for all 1,005, and h = 8 for A_base.

**R9. Frozen judge.** Command: `python3 judge/judge.py experiments/referee/L006-round2/jsamples/*.json` (jsamples_verdicts.log).
- 8 extensions from classes 280 and 281 (vertex, T1a and T2 types) give PASS NO-IMPROVEMENT n=14 h=9.
- The A_base control gives PASS NO-IMPROVEMENT h=8.
- Exit status 0.

**R10. Full-census pass and K47 consistency.** Command: `python3 -I census_pass2.py` (census_pass2.log, 81 s, 2 processes, own code).
- **n = 12.** All 54,243 sets are (4,5) with exactly 10 3-APs. Each has no Sidon 8-subset but at least one Sidon 7-subset, so h = 7. Each point is avoided by some maximum Sidon subset (no universal vertex, i.e. every T2 line hypergraph has alpha = 9). The number of maximum Sidon subsets equals the stored n_max_sidon in all 54,243 classes.
- **n = 14.** All 2,910 classes of data/census_n14_m12_classes.jsonl.gz have h = 8. All 91 two-point deletions of each keep h = 8, confirming K47 as cited in the Statement; maximum Sidon subsets number 137..150. This is a consistency test of the theorem's consequence: a deletion with h = 7 would be an extremal 12-point set with a (4,5) extension of h = 8.

**R11. Scope of the T2 intersection count.** Command: `python3 -I isect_count.py` (isect_count.log).
- On 14 classes, the 36 lines have 368 distinct pairwise intersection points in every class.
  - The 432 pairs of non-parallel lines include 36 same-a pairs, which meet at the 12 points (a, a).
  - Each of the 20 ordered APs a + b = 2c of A gives a triple point at ((2a+b)/3, (a+2b)/3).
  - This leaves 396 - 40 = 356 other points, and 356 + 12 = 368.
- After removing x = y and points with x or y in A, the counts equal the stored t2_isect_pts (4,954 = 4,954).
- So 19,247,288 counts the tested, non-degenerate points; all distinct intersection points number 368 x 54,243 = 19,961,424. See E1.

## Status of round-1 issues

1. **Problems 1-2 (brute-force description).** Fixed and accurate (R4).
2. **Problem 3 (provenance).**
   - The logs are now tracked.
   - The README range "106-130" is corrected.
   - The README explains that bruteforce_sample_results.json is the known-sets run.
   - Still remaining: the README's "256-975 pairs per class" (E4).
3. **Optional items.**
   - The provenance note now cites the round-1 byte-for-byte reproduction. Done.
   - The Remark's "Lemma E" citation is unchanged (E2).
   - The runtime phrase is unchanged: 12,668 s is the resumed run, and the provenance note explains the restart. Acceptable.
   - Code cosmetics: they should stay as they are, since editing the code would detach it from the run.

## Problems found (in order of severity)

No blocking problem. Every step is verified, and every number in the proof is reproduced. The following editorial remarks are non-blocking: none affects a step, and none overstates what was verified.

- **E1 (wording).** The T2 paragraph says "the pairwise intersection points of the 36 lines (19,247,288 in total over all classes) were tested exactly". There are 19,961,424 distinct intersection points; 19,247,288 is the number remaining after removing x = y and points with x or y in A, which are not extensions. The Totals bullet ("19,247,288 T2 line-intersection points tested") is correct. Suggested wording: "(after removing x = y and points with x or y in A: 334 to 356 per class, 19,247,288 in total)", as in L005.
- **E2 (citation, non-load-bearing Remark).** "Lemma E" in kb/notes/extension_lemmas.md is stated only for extreme a. The identity alpha(H + {a,x,y}) = max(alpha(H) + 1, alpha(H - a) + 2), used for every a, is proved inside Lemma E's proof and in its "Remark (other roles)". Cite the identity, or "Lemma E and its Remark". This was round 1's optional item 4.
- **E3 (dependencies).** DEPENDS ON lists K3-K6. The parenthetical "non-saturated (m=11)" uses m >= 11, which is Henning-Yeo (K8); the Remark uses K7 and K8. L005 lists K8 for the analogous clause. Add K7 and K8, marked as not load-bearing for the main statement.
- **E4 (README only).** In "(256-975 pairs per class; 106-130 further extend12_all pairs lie outside the window; also class 8532 with a smaller window)", the value 256 belongs to class 8532. Its result file was overwritten and survives only in commit a982863 (window [-127, 635], 256 in-window pairs, 377 outside, match true). The six on-disk classes give 715-975, and "106-130" excludes 8532. Either say so or drop 8532.
- **Observation (optional strengthening).** T1a follows from f(13) = 8 (Henning-Yeo), and the T2 cases follow from Lemma U and K6. Only the 51,264,727 T1b pairs rest on the computation alone. Saying so would make clear where the sweep is load-bearing. That part is independently confirmed: by Route V's exact pair-set equality on 201 classes (188,413 pairs) and the unmodified rerun of 437 further classes here, and by round 1's Route C (150 classes) and Route L (600 classes).
