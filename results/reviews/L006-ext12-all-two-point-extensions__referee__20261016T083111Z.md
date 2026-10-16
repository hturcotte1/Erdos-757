VERDICT: ACCEPT

# Referee report, round 3: L006-ext12-all-two-point-extensions

Claim: results/proofs/L006-ext12-all-two-point-extensions.md (revised 07:38 UTC after round 1; commit 209a04c). Scratch folder: experiments/referee/L006-round3/ (all scripts, logs and outputs named below are there). Wall time used: about 50 minutes. Resources: at most 2 processes, nice 5, every foreground command under 10 minutes.

## Summary

**The claim.** Each of the 54,243 extremal 12-point classes of L002 (h = 7) has only (4,5) two-point extensions with h = 9. Hence no 14-point (4,5)-set with h <= 8 contains a 12-point subset with h = 7.

**Verdict.** I re-derived the T0/T1a/T1b/T2 case analysis and found it sound and exhaustive. I audited extend12_all.py line by line and found no defect: the candidate sets are complete, the arithmetic is exact, the (4,5) tests are complete, and every exhibited 9-subset is asserted Sidon. The proof's quoted totals all match the stored rows, and the stored rows match the census.

**Reruns.** The unmodified code reproduces 64 classes of my own choosing byte for byte (`secs` excepted).

**Independent checks.** I ran three checks of my own design. None imports the authors' code or e757, and all use only the Sidon definition.
- **Route X, full census.** All 54,243 classes, organised by the point in P_x rather than by AP hypergraphs. It needs no T1a/T1b split and no enumeration of (4,5) pairs; together with an empty "core" it covers all of R^2.
  - Result: 0 deficient (4,5) pairs; every class has an empty core.
  - A positive control is included.
- **Route V.** An exact line-by-line deficient-locus computation over all of R^2, with no case analysis.
  - Result, on 429 classes: 0 deficient (4,5) extensions.
  - 12/12 positive controls are detected, 6 of them in the claim's own family.
  - Where it overlaps round 1's Route L, the two computed loci agree exactly (common lines on 80 classes; point sets off the common lines on 8).
- **Recount.** A re-implementation of the per-class counters: 32 classes, all 7 counters equal to the stored rows.

**Further checks.**
- On the 2,910 saturated 14-point classes, the Consequence holds directly: all 264,810 two-point deletions have h = 8.
- The frozen judge passes 9/9 sample extensions with h = 9.

**What remains.** The round-1 text problems are fixed. Only non-blocking editorial remarks are left (below).

## The case analysis, re-derived (numbered steps)

1. **Affine invariance.** Being (4,5), h and the AP structure are invariant under x -> qx + t, q != 0, reflection included, and A -> A u {x,y} commutes with these maps. So one integer representative per class suffices. The census classes are pairwise inequivalent: 54,243 distinct normal forms under my own normal form (rerun_unmodified.log).
2. **Upper bound.** h(B) <= h(A) + 2 = 9, since a Sidon subset of B meets A in a Sidon subset of A.
3. **Exhaustive split.** Every new 3-AP of B contains x or y.
   - If some new AP contains exactly one of them, that point is in P_x: case T1 (WLOG x).
   - Else, if a new AP exists, every new AP is {a,x,y} with a in A, in one of 3 roles: case T2.
   - Else: case T0.
4. **T0.** H(B) is H(A) plus two isolated vertices, so alpha = 9. B is (4,5), hence weak Sidon (K3), so h = alpha (K4).
5. **T1a** (y in no AP of B). y is isolated in H(B), so h(B) = h(A u x) + 1. A u x is (4,5) as a subset of B, so x is admissible. The code computes h(A u x) = 8 for every admissible x. This also follows from f(13) = 8, which is Henning–Yeo.
6. **T1b** (y in an AP of B). The other two points of that AP lie in A u {x}, so y is in `candidates(A u x)`; this set is finite and integral at scale 4, because every x in P_x is even. The (4,5) property of B is decided completely by four tests:
   - A, asserted;
   - `single_ok(x)`;
   - `single_ok(y)`;
   - `pair_ok(x,y)`.

   For every (4,5) pair, `h_exact_B` either returns 9 with a 9-subset whose Sidon property is asserted, or computes the exact alpha. The histogram shows 9 for all 51,264,727 pairs.
7. **T2 generic.** Suppose x, y are not in P_x and (x,y) lies on exactly one of the 36 lines. Then H(B) = H(A) + {a,x,y}, since the three lines of one a meet only at (a,a), which is excluded. Hence alpha = max(alpha(H)+1, alpha(H-a)+2), which is 9 iff some maximum independent set avoids a. The code computes 9 for all 36 line hypergraphs of every class.
8. **T2 intersections.**
   - Same-role lines are parallel and distinct.
   - Any other intersection with a != a' gives two APs sharing {x,y}, so B is not linear and not (4,5) (K6).
   - The code tests all of them exactly anyway: 0 of 19,247,288 points are (4,5).
9. **Consequence.** Let C be a 14-point (4,5)-set with h(C) <= 8, and A a 12-point subset of C. Then h(A) >= f(12) = 7. If h(A) = 7, then A is a census class (L002) and h(C) = 9 by the theorem, a contradiction. Hence h(A) = 8.

   By-product: for x in P_x, h(A u x) = 8 is computed; for x not in P_x, x is isolated in H(A u x). In both cases h = 8.
10. **Remark (not load-bearing).**
    - The arithmetic of Lemma U is correct: 85 <= 85 - 3 deg a forces deg a = 0, and every vertex of a saturated set has degree >= 1.
    - Henning–Yeo applies to H(A) - a, which is linear and F7-free.
    - Lemma E of kb/notes/extension_lemmas.md is stated for an extreme a. However, its proof's identity holds for any a, and the note's next paragraph covers all roles. So the citation is acceptable.

## Code audit (experiments/20261016-0330-ext12-all/extend12_all.py)

The file's sha256 is b4600c1e2966e76aaa1a8a38f36c811cf5ef495ec36d1bbe6a71f7b53d968db0, the same file round 1 audited; its last commit is a982863, which only adds the 4-point `ndist` fast path.

- **`ndist`.** The fast path lists all 6 pairs.
- **`ap_triples`.** Tests every pair i<k with k >= i+2 for an integer midpoint in the set.
- **`has_indep`.** Each mask is indexed by its largest vertex and checked when that vertex is added. The pruning `size + n - i < target` is sound.
- **`alpha_masks`.** Exact.
- **`all_max_indep`.** Complete.
- **`is_sidon_ints`.** Includes the doubled elements (sums with i <= j).
- **`candidates`.** Covers (a+b)/2, 2a-b and 2b-a; the integrality assert holds at scale 4.
- **T2 lines.**
  - x the midpoint: y = 2x - a;
  - y the midpoint: y = (x+a)/2;
  - a the midpoint: y = 2a - x.

  The 432 non-parallel pairs are intersected exactly with Fractions; the exclusions x = y, x in A, y in A are applied; denominators are cleared before the (4,5) test.
- **Resume logic.** It appends to results.jsonl and skips classes already done. My check confirms exactly one row per class (C1).
- **Assertions.** They are active, since the run did not use -O. A failed assertion would have crashed the pool, and the run completed (run.log).
- **Cosmetic only.** The docstring advertises `--start`, which is not implemented. The comment "vertices 14,15" should read 12, 13. Line 241 is a no-op expression.

## Checks performed

Commands were run from experiments/referee/L006-round3/ unless stated otherwise.

**C1. Stored rows vs census and quoted totals.** Command: `nice -n 5 python3 -I check_rows.py` (check_rows.log).
- 54,243 rows, one per class 0..54242; 0 `set` mismatches against the census.
- In every row:
  - hA = 7;
  - t2_line_h = [9];
  - t2_lines = 36;
  - t2_isect_45 = 0;
  - records = [];
  - min_h = 9;
  - t2_precheck false;
  - in_all_max_sidon = [];
  - hist = {9: n_single_45 + n_t1b_45 + 36};
  - n_2ext = n_t1b_45.
- Totals:
  - singles 1,887,566 (21..46 per class);
  - T1b 51,264,727 (424..1,395);
  - intersection points 19,247,288 (334..356), of which 0 are (4,5);
  - evaluated values 55,105,041;
  - n_max_sidon 48..63.

  These equal summary.json and every number in the proof.
- sha256 values:
  - census: e0e2584b... (the L002 file);
  - data/ext12_all_rows.jsonl.gz: 6564edc7...

**C2. Unmodified rerun.** Command: `nice -n 5 python3 -B rerun_unmodified.py` (rerun_unmodified.log). It imports a byte-identical copy of extend12_all.py (sha256 asserted) and does not write into the authors' folder.
- **Sample (64 classes, rerun_ids.json):**
  - the first and last class attaining the minimum and maximum of each of 6 counters;
  - classes 54240-54242, 27121, and 3, 141, 277 (pre-restart);
  - the three known-set classes;
  - seeded random classes (seed 3141592).
- **Result.** 64/64 rows are identical to the stored rows in all fields except `secs` (22.9 s with 2 processes).
- **Known sets.** My own affine normal form maps them to classes 20392 ('12'), 23942 ('12b') and 18917 ('12c'). Processed as given in data/small_records.json, their counters equal those of their census classes and the README table (max Sidon / singles / T1b / P_x / intersections):
  - '12': 62/34/893/159/356;
  - '12b': 60/35/933/156/350;
  - '12c': 60/36/974/151/348.

**C3. Route X: full census, independent (route_X.py, rx/full_p*.jsonl; sha256 in code_hashes.txt).**
- **Method.** Uses only the Sidon definition. Let Ts be all Sidon 7-subsets, enumerated by brute force, with h(A) = 7 re-checked: no T u {a} is Sidon.
  - **(i) x in P_x.** This covers every pair with a point in P_x, by symmetry. Let G_x be the T with T u {x} Sidon. Then (x,y) is deficient iff y is in Y_x = the intersection over T in G_x of K(T u {x}), where K(S) = {s2+s3-s1 : s1 not in {s2,s3}} u {(s1+s2)/2 : s1 != s2} minus S.
    - K(S) is finite, so every real y is covered and no T1a/T1b split is needed.
    - Every y in Y_x is tested for (4,5) of B.
    - x with x + a = b + c is skipped, since A u {x} then contains a parallelogram and no (4,5) set contains it.
    - An empty G_x with A u {x} (4,5) would be flagged.
  - **(ii) x, y not in P_x and B (4,5).** B is weak Sidon (K3), so the only coincidences in T u {x,y} are 3-APs {x,y,t}. Two such APs violate linearity (K6). A single one is deficient only if its point a lies in every T; I checked that the intersection of all Ts is empty.
- **Speed-ups.** These are exact.
  - Y_x is filtered with precomputed K(T), differences, sums and T.
  - A weak-Sidon pre-filter is applied before the full (4,5) test.
  - On every 25th class, Y_x is recomputed directly from K_of and must agree, and each deficient pair is re-verified against all T with the Sidon definition.
  - The optimised and unoptimised versions give identical rows on 300 classes (rx/t*, rx/u*).
- **Result.** All 54,243 classes, in two seeded random halves (`nice -n 5 python3 -I route_X.py perm 0 2 rx/full_p0.jsonl` and `... perm 1 2 rx/full_p1.jsonl`, 793 s and 790 s; `python3 -I summarize_X.py`, routeX_full_summary.log).
  - **0 flags.** No deficient (4,5) pair has a point in P_x, and no admissible x has h(A u x) = 7.
  - **Core.** The intersection of all maximum Sidon sets is empty in every one of the 54,243 classes.
  - **Deficient pairs.** 1,716,162 deficient ordered pairs (x in P_x passing the filter, y in Y_x) were tested for (4,5): **none is (4,5)**.
  - **Spot classes.** All 2,170 passed both slow-path assertions.
  - **Agreement with the stored rows.** In every class, the number of maximum Sidon sets and |P_x| equal the stored n_max_sidon and Px_size.
  - **Conclusion.** Together with steps 3 and 8, this independently re-establishes the theorem for the whole census, using only K3 and K6 (both published and elementary) in case (ii).
- **Positive control.** Command: `python3 -I control_X.py` (control_X.log). It calls the unmodified `run_class` on A = A_base - {p,u,v} with h(A) = 7, where B = A_base - {p} is a deficient (4,5) extension (h = 8). Out of 12 controls:
  - in all 9 where u or v lies in P_x(A), the deleted pair (4u,4v) is flagged as a deficient (4,5) pair;
  - in the 3 where neither does, Route X reports a non-empty core: x4 coordinates 4224, 2384, 544, i.e. 1056, 596, 136. The deleted pair forms an AP with that vertex, so the extension is deficient through case (ii). This is exactly the situation the empty-core check excludes for every census class.

**C4. Route V: exact deficient locus over R^2, line by line (route_V.py; drivers drive_V.py, compare_V.py).**
- **Method.** Uses only the Sidon definition. (x,y) in Omega is deficient iff T u {x,y} is non-Sidon for every maximum Sidon T. Each "non-Sidon" locus is the union of the integer lines on which two formal sums of T u {X,Y} coincide.
  - Every deficient point lies on a line l of U_{T1}.
  - If l is in every U_T, it is a common line. I decide it symbolically: the generic ndist of every 4-subset along l, with differences as affine functions of the parameter.
  - Otherwise every deficient point of l lies in l cap U_{T'} for some T' with l not in U_{T'}. Each such point is re-tested numerically against all T and then tested for (4,5).
- **Positive controls (controls.log).** All 12 deleted pairs are detected:
  - A_base minus {0,1056}, {243,249}, {200,528}, {246,272}, {136,596}, {298,323} (k = 8);
  - the three 12-point records minus a pair with h = 6 (k = 6), two each. Here the deleted pair is found as a deficient (4,5) point, and brute force gives h(B) = 7.
- **Results.** 429 classes:
  - batch 1, 229 classes (routeV_main.jsonl): the 64 rerun classes, the 68 classes where round 1 found common lines, and 100 fresh seeded classes;
  - batch 2, 200 new classes (routeV_batch2.jsonl): 80 with a degree-1 vertex, the 40 largest and 40 smallest spans, and 40 seeded random;
  - in total, 216 classes have a degree-1 vertex.

  Findings:
  - 394,528 deficient points, **0 of them (4,5)**;
  - 170 deficient common lines (156 of the form x+y = c, 7 of the form x = c, 7 of the form y = c), **all with generic min ndist 4, i.e. non-(4,5) along the whole line**;
  - the number of maximum Sidon sets equals the stored n_max_sidon in all 429 classes.
- **Cross-implementation (exact_VL.py, exact_VL.log).**
  - On the 80 classes shared with round 1's Route L, the sets of common lines are identical.
  - On 8 classes (1, 12146, 13248, 23942, 0, 20392, 962, 16812), the deficient point sets off the common lines are identical as exact rational sets. The counts the two programs report differ only by how many points lying on a common line each happens to list.
  - Known classes: 20392 has 570 points and no line; 18917 has 672 points and no line; 23942 has one line x+y = 298, which is non-(4,5).

**C5. Independent recount of the counters (recount.py, recount.log; 32 classes, every 2nd of C2).**
- Px_size, n_single_45, t1_pairs, n_t1b_45, t2_isect_pts, t2_isect_45 and n_max_sidon are equal to the stored rows (0 mismatches).
- Every one of the 1,060 admissible singles has a Sidon 8-subset T u {x}.
- Every one of the 28,090 (4,5) T1b pairs has a Sidon 9-subset T u {x,y}.

**C6. Consequence on the 14-point data (conseq14.py, conseq14.log, 55 s).**
- For all 2,910 saturated extremal 14-point classes of L004, (4,5) and h = 8 were re-checked.
- All 264,810 two-point deletions have h = 8, i.e. none has h = 7. This agrees with the Consequence and with K47.

**C7. Frozen judge (from the repository root).** Command: `python3 judge/judge.py experiments/referee/L006-round3/jsamples/*.json` (jsamples_verdicts.log).
- The 9 extensions were made by my own code (make_jsamples.py): types T1a, T1b and T2-generic for classes 54242, 2 and 30954.
- Verdict on all 9: `PASS NO-IMPROVEMENT n=14 h=9`.

**C8. Round-1 problems.**
- **Problems 1-2.** The brute-force paragraph now matches bruteforce_sample.py:
  - integer pairs in the x4 coordinates, window [min - span, max + span];
  - h-checks only on all T1b-type pairs and on 2,000 sampled T2-type pairs;
  - the imports from extend12_all are acknowledged.

  It also matches the two JSON files: 772/804/845 in-window; 121/129/129 outside the windows, plus 129/106/130 for the random classes; t1b_match true.
- **Problem 3.** bf_known.log and bf_random.log are now tracked (`git ls-files`). The README range "106-130" is correct.

## Problems found (in order of severity)

No blocking problem. Non-blocking editorial remarks, none affecting any step:

1. **README provenance (not the proof).** README section (2) still says "256-975 pairs per class ... also class 8532 with a smaller window".
   - The class-8532 output survives only in git history (`git show a982863:experiments/20261016-0330-ext12-all/bruteforce_sample_results.json`). The known-sets run later overwrote it; that file name differs from the `_known` name in the committed script.
   - The six on-disk classes give 715-975.
   - Suggest citing the git object or dropping 8532.
2. **Run time.** "12,668 s wall clock" in the proof is the final, resumed run only. The README says so; the proof could add "final (resumed) run".
3. **Code cosmetics in extend12_all.py.**
   - The docstring advertises `--start`;
   - the comment says "vertices 14,15", where 12, 13 is meant;
   - line 241 is a no-op.

   None of these has any effect on results.

## Dependencies

- **L002, the completeness of the census.** It is ACCEPTED and was not re-audited here. I checked that the census file is the one L002's referee verified: sha256 e0e2584b..., 54,243 pairwise inequivalent classes, each (4,5) with h = 7 (asserted by the authors' run, by Route X on all classes, and by round 1's census pass).
- **K3, K4, K6 [published].** All three are elementary; I re-derived them.
