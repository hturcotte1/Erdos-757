VERDICT: NEEDS-WORK

# Referee report, round 1: L006-ext12-all-two-point-extensions

Claim: results/proofs/L006-ext12-all-two-point-extensions.md (STATUS line "submitted (2026-10-16 07:03 UTC)"). Scratch folder: experiments/referee/L006-round1/. Wall time used: about 31 minutes, at most 3 processes, nice 5 (Route L ran at nice 10 for its first 5 minutes).

## Summary

**The claim.** Each of the 54,243 extremal 12-point classes of L002 (h = 7) has only (4,5) two-point extensions with h = 9. Hence no 14-point (4,5)-set with h <= 8 contains a 12-point subset with h = 7.

**What I verified.** The mathematics and the computation are correct.
- **Case analysis.** I re-derived T0/T1a/T1b/T2 and found it sound and exhaustive.
- **Code audit.** I read `extend12_all.py` line by line. The candidate sets are exhaustive and the arithmetic is exact. Every 4-subset containing a new point is tested. Exhibited 9-subsets are asserted Sidon. The T2 generic hypergraph and all line intersections are handled correctly.
- **Stored data.** All 54,243 stored rows agree with the census and with every total quoted in the proof.
- **Reruns.** The unmodified code reproduces 314 distinct classes byte for byte, timing excepted (40 + 280 reruns, 6 classes in both). These include the classes of the three known sets and all 280 classes produced by the pre-restart code version.
- **Route L (my own design, no case analysis).** An exact deficient-locus computation over all of R^2, using only the Sidon definition. On 600 classes (the three known sets included) it finds 387,482 deficient points and 72 deficient lines. None of them gives a (4,5)-set. A positive control shows the method does detect deficient (4,5) extensions when they exist.
- **Further independent checks.** Route C re-implements all seven per-class counters with Sidon-definition h: 150 classes, all equal. A full-census Sidon-definition pass covers all 54,243 classes. The frozen judge gives h = 9 on 16 sample extensions of every case type.

**Why NEEDS-WORK.** The proof's "Acceptance checks" paragraph misdescribes the authors' brute-force cross-check:
- it says all 20,252,381 / 11,128,510 / 14,730,123 windowed (4,5) pairs were shown to have Sidon 9-subsets, but the script computes h only for about 2,800 pairs per set;
- it misstates the grid and the window that were searched;
- it cites two git-ignored log files.

These are text-only fixes. No recomputation is needed. The verdict follows the rule that a remaining false sentence in a certificate means NEEDS-WORK, as in L005 round 1.

## Steps of the proof, re-derived

1. **Affine invariance.** Being (4,5), h and the AP structure are invariant under x -> qx + t (q != 0, reflection included), and A -> A u {x,y} commutes with these maps. So one integer representative per class suffices. Correct.
2. **Upper bound.** h(B) <= h(A) + 2 = 9 holds by the definition: a Sidon subset of B meets A in a Sidon subset of A. Correct, and correctly attributed.
3. **Exhaustive split.** Any new 3-AP of B contains x or y.
   - If some new AP contains exactly one of them, that point is in P_x: case T1 (WLOG x, since the statement is symmetric).
   - Otherwise, if a new AP exists, every new AP contains both x and y, so it is {a, x, y} with a in A, in 3 roles: case T2.
   - Otherwise there is no new AP: case T0.
4. **T0.** H(B) = H(A) plus two isolated vertices, so alpha = 9. B is (4,5), hence weak Sidon (K3), so h = alpha (K4). Correct.
5. **T1a** (y in no new AP). y is isolated in H(B), so h(B) = h(A u {x}) + 1. A u {x} is (4,5) as a subset of B, so x is an admissible single. Correct.
6. **T1b** (y in a new AP). The other two points of that AP lie in A u {x}, so y lies in `candidates(A u {x})`, the midpoints and endpoints of pairs of A u {x}. The candidate set is exhaustive. The (4,5) property of B is decided completely by four tests:
   - A, asserted on all 495 4-subsets;
   - `single_ok(x)`;
   - `single_ok(y)`;
   - `pair_ok(x, y)`.
   Correct.
7. **T2 generic points.**
   - If x, y are not in P_x and (x,y) lies on exactly one of the 36 lines, then H(B) = H(A) + {a, x, y}.
   - Hence alpha = max(alpha(H) + 1, alpha(H - a) + 2), which is 9 iff some maximum independent set avoids a.
   - Every other point of a line is either in T1, or on a second line, or excluded (x = y, x in A, y in A).
   Correct.
8. **T2 intersections.**
   - Lines with the same role are parallel and distinct.
   - Lines with the same a but different roles meet only at (a, a), which is excluded. I checked all three pairings.
   - Any other intersection gives two APs {a,x,y} and {a',x,y} with a != a' sharing {x,y}. That contradicts linearity (K6), so no intersection point can be (4,5).
   - The code's exhaustive test agrees: 0 of 19,247,288 points are (4,5).
9. **Consequence.** It is correct given L002 (completeness of the census, ACCEPTED), f(12) = 7 and f(14) = 8. The one-point by-product is also correct: for x not in P_x, h(A u x) = 8 holds trivially.
10. **Remark (not load-bearing).** The arithmetic is correct: tau(H - a) = tau(H) = 5 for a universal vertex a, so 85 <= 85 - 3 deg a, which forces deg a = 0. Every vertex has degree >= 1 (C8). Henning-Yeo as cited (K8) needs only linear and F7-free, which hold for H(A) - a. The citation "Lemma E" is loose; see Problem 4.

## Code audit (experiments/20261016-0330-ext12-all/extend12_all.py, sha256 b4600c1e2966e76aaa1a8a38f36c811cf5ef495ec36d1bbe6a71f7b53d968db0)

- **`ndist`.** The 4-point fast path lists all 6 pairs and is identical to the general formula.
- **`ap_triples` / `masks_of`.** Every pair (i, k) is tested for an integer midpoint present in the set.
- **Independence searches.** `has_indep` is exact: masks are indexed by their largest vertex, every mask is checked when that vertex is added, and the pruning `size + n - i < target` is sound. `alpha_masks` increases the target until it fails. `all_max_indep` enumerates all independent sets of the given size.
- **`is_sidon_ints`.** Uses sums with i <= j, so the doubled points 2x are included.
- **`candidates`.** Covers (a+b)/2, 2a - b and 2b - a for all pairs, minus the set. Integrality is asserted, and holds because A is scaled by 4 and every x in P_x is even.
- **`h_exact_B`.** Returns 9 only together with a 9-subset whose Sidon property is asserted. Otherwise it computes the exact alpha.
- **`process`.** Asserts n = 12, (4,5) and h(A) = 7. Then:
  - T1a records hAx + 1 for every admissible x;
  - the T1b pairs are deduplicated as unordered pairs;
  - the T2 hypergraph is H(A) plus the edge {a, 12, 13}. The comment says "14,15", which is cosmetic;
  - all pairs of non-parallel lines are intersected exactly with Fractions;
  - the exclusions x = y, x in A, y in A are applied, and the (4,5) test is done after clearing denominators.
- **`main`.** Resumes from results.jsonl and aggregates from it. Asserts are active, since the run did not use `-O`. Any failed assertion would have aborted the pool, and the run completed.
- **Cosmetic.** The docstring advertises `--start K`, which is not implemented.

## Checks performed (commands run from /home/user/Erdos-757 or the scratch folder; logs there)

**C1. Stored rows vs census and the proof's totals.** Command: `python3 -I experiments/referee/L006-round1/check_rows.py` (check_rows.log).
- 54,243 rows and 54,243 census entries; class ids 0..54242 each appear exactly once; 0 `set` mismatches.
- Every row has hA = 7, t2_line_h = [9], t2_lines = 36, t2_isect_45 = 0, records = [], min_h = 9 and t2_precheck = false.
- In every row the histogram has the single key 9, with count n_single_45 + n_t1b_45 + 36.
- Totals:
  - n_single_45 = 1,887,566 (21..46 per class);
  - n_t1b_45 = 51,264,727 (424..1,395);
  - t2_isect_pts = 19,247,288 (334..356);
  - n_max_sidon 48..63;
  - evaluated values 55,105,041.

  All equal the proof and the README.
- data/ext12_all_rows.jsonl.gz equals the git-ignored results.jsonl, `secs` excepted.
- The first 280 lines of results.jsonl are exactly classes 0..279, the pre-restart run.

**C2. Classes of the known sets** (`find_known.py`, affine normal form with reflection).
- The census has 54,243 pairwise inequivalent classes.
- '12' is class 20392, '12b' (omega) is class 23942 and '12c' (omega) is class 18917.
- The census file is the one re-verified by the L002 referee, with a single commit a887219 and sha256 e0e2584b...

**C3. Unmodified authors' code, 40 classes.** Command: `nice -n 5 python3 rerun_authors.py`, which imports `extend12_all.process` without modifying it.
- The 40 classes are:
  - the 3 known classes;
  - classes 0, 1, 7, 100, 199, 279;
  - the minimum and maximum of each of the six counters;
  - three random classes from the authors' brute force;
  - seeded random classes.
- Result: 40/40 rows identical to the stored rows in all fields except `secs`.
- The three known sets, processed as given in data/small_records.json, give the same invariant counters as their census classes (max Sidon / singles / T1b / P_x / intersections):
  - '12': 62 / 34 / 893 / 159 / 356;
  - '12b': 60 / 35 / 933 / 156 / 350;
  - '12c': 60 / 36 / 974 / 151 / 348.

  These match the README table.

**C4. Provenance of the restart.**
- `git log` of extend12_all.py has two commits:
  - e94f53d (03:29:44), the code of the first run;
  - a982863 (04:23:55), whose only change is the 3-line ndist 4-point fast path.
- The file's mtime is 03:31:11, before the final run started (03:31:28 per run.log). So the final run used the current file.
- `nice -n 5 python3 rerun_first280.py` reruns the current code on all classes 0..279: 280/280 rows identical (59.8 s).

**C5. Route L, design.** `route_L.py` is my own code; it imports neither e757 nor the authors' code, and uses no 3-APs and no case analysis.
- **Reduction.** Let A have h(A) = k and let Ts be all Sidon k-subsets, found by brute force from the sums definition. On Omega = {x != y; x, y not in A}, h(A u {x,y}) <= k+1 iff every T u {x,y} with T in Ts is non-Sidon.
- **Lines.** For each T, the non-Sidon locus is the union of the lines where two of the formal sums s_i + s_j (i <= j) of T u {x,y} coincide. These are integer line triples; pairs with zero x,y-coefficients are asserted never to coincide.
- **Exact intersection.** The intersection over all T is computed exactly by iterative refinement into common lines plus a finite set of integer homogeneous points. Completeness: a deficient point that is on no final common line is generated at the step where its last surviving line drops out, and is then retained.
- **Re-verification.** Every point is re-verified against every T with the Sidon definition, and 3 points of every common line likewise.
- **Common lines.** Decided symbolically, using the line parameter: if ndist <= 4 at a generic point of the line, then ndist <= 4 at every point. Every 4-subset containing x or y is examined.
- **Points.** The (4,5) property is tested directly at every point.

**C6. Route L, positive control.** Command: `python3 -I route_L.py control 3` (control.raw, control_summary.log). The inputs are A' = A_base - {u, v} for {u,v} = {0,1056}, {243,249}, {136,596}, {286,400}; each has h = 8.
- The method flags 432, 456, 1,008 and 420 deficient (4,5) points, and 14, 13, 53 and 7 generically-(4,5) deficient common lines.
- The deleted pair lies on a flagged line in all 4 cases, and is also a flagged point in 2 of them.
- The brute-force h(B) at flagged points is 9 = h(A') + 1.

So Route L detects deficient (4,5) extensions when they exist.

**C7. Route L on 600 classes.** Command: `python3 -I route_L.py <600 ids> 3` (routeL_600.jsonl, routeL_600_summary.log). The classes are the 40 of C3 plus 560 seeded random ones, including 20392, 23942 and 18917.
- All 600 are (4,5) with h = 7, and n_max_sidon equals the stored rows.
- Each T has 312..410 lines.
- 387,482 deficient points in total (196..2,048 per class): **0 of them (4,5).**
- 72 deficient common lines in 68 classes: 64 of the form x + y = c, which break the weak Sidon property, and 4 + 4 of the form x = c or y = c. **All 72 are non-(4,5) along the whole line.**
- Known classes:
  - 20392: 570 points, 0 lines;
  - 23942: 1,304 points, 1 line;
  - 18917: 672 points, 0 lines.

  None of them gives a (4,5)-set.
- Spot check, class 13248, deficient line x = 92:
  - 92 is the midpoint of 0 and 184, so 92 is in P_x;
  - T u {92} is non-Sidon for all 55 maximum T, so h(A u {92}) = 7;
  - but {0,92,296,388} has only 4 distances, so A u {92} is not (4,5).

  The authors' admissibility filter is therefore load-bearing and correctly applied.

**C8. Full-census pass.** Command: `nice -n 5 python3 -I census_pass.py` (census_pass.log, 94 s). For all 54,243 classes I recomputed, with my own Sidon-definition code:
- (4,5) on all 495 4-subsets;
- no Sidon 8-subset, but at least one Sidon 7-subset;
- the number of maximum Sidon subsets, equal to stored n_max_sidon;
- m = 10 3-APs;
- minimum degree >= 1 (the histogram of minimum degrees is {1: 10,006, 2: 44,237});
- every point is avoided by some maximum Sidon subset.

0 failures. The last condition is exactly "every T2 line hypergraph has alpha = 9", so the T2-generic case is confirmed for the whole census independently of the authors' hypergraph code.

**C9. Route C, 150 classes.** Command: `nice -n 5 python3 -I route_C.py <150 ids> 3` (routeC_150.jsonl, routeC_150_summary.log). This is an independent re-implementation of the case-analysis counters, with h taken from the Sidon definition.
- **Counters.** Px_size, n_single_45, t1_pairs, n_t1b_45, t2_isect_pts, t2_isect_45 and n_max_sidon equal the stored rows in all 150 classes (0 mismatches).
- **h values.**
  - h(A u x) = 8 for all 5,226 admissible singles.
  - h(B) = 9, with a Sidon 9-subset exhibited, for all 141,848 (4,5) T1b pairs.
- **Classes.** These include the known classes, 13248 and 8532.

**C10. Frozen judge.** Command: `python3 judge/judge.py experiments/referee/L006-round1/jsamples/*.json` (jsamples_verdicts.log).
- 16 extensions B generated by my own code (`make_jsamples.py`): types T0, T1a, T1b and T2-generic for classes 20392, 23942, 18917 and 12070.
- Each B was checked (4,5) by my code.
- Judge verdict on all 16: `PASS NO-IMPROVEMENT n=14 h=9 ratio=9/14`.

**C11. The proof's quoted brute-force numbers vs the logs and the script.**
- The counts agree with bf_known.log and bf_random.log: singles 34/35/36, T1b 893/933/974, in-window 772/804/845, outside 121/129/129, max Sidon 62/60/60, windowed (4,5) pairs 20,252,381 / 11,128,510 / 14,730,123, and t1b_match true.
- What the script does and does not verify is described in Problems 1 and 2.

## Problems found (in order of severity)

1. **False description of the evidence (must fix).** The "Acceptance checks" bullet says: "20,252,381, 11,128,510 and 14,730,123 (4,5) pairs in the windows, all with a 3-AP-free Sidon 9-subset."
   - The cited brute force does not verify this. `bruteforce_sample.py` computes h only in two places:
     - for its T1b-type pairs (772, 804, 845), at line 58;
     - for `rnd.sample(t2like, 2000)` out of 36,891, 26,054 and 30,790 T2-type pairs, at lines 53-56.
   - The T0-type and T1a-type pairs, and the unsampled T2-type pairs, are only counted; line 44 is `elif xin and not yin: pass`. That is all but about 2,800 pairs per set.
   - The mathematical statement is true: it follows from the case analysis, and C7 confirms it independently. But the sentence credits the brute force with a check it did not perform.
2. **Inaccurate description of the brute force (must fix).** The proof says "a plain-integer brute force over all half-integer pairs in a window of twice the span on each side".
   - **Grid.** The script enumerates all integer pairs in the x4 coordinates of `extend12_all` (lines 15 and 23), i.e. quarter-integer pairs in the set's own coordinates.
   - **Window.** It is [min - span, max + span], i.e. one span on each side (line 16, DIV = 1). For example, '12' has span 2300 and window [-2300, 4600].
   - **Independence.** The script imports `extend12_all` for the h routine and for the comparison (`E.h_exact_B`, `E.process`), so "plain" overstates its independence. The README states this caveat; the proof omits it.
3. **Provenance of cited files (should fix).**
   - bf_known.log and bf_random.log are cited but git-ignored (.gitignore line 38: `experiments/20261016-0330-ext12-all/*.log`), so they will not reach the repository. Cite the tracked bruteforce_sample_results.json and bruteforce_sample_results_random.json instead (they contain the same rows), or force-add the logs.
   - The committed script names its known-sets output bruteforce_sample_results_known.json, but the stored file is bruteforce_sample_results.json. Say so, or rename the file.
   - The README mentions a class-8532 run. Its output exists only in git history (commit a982863); it was overwritten in the working tree.
   - README: "121-129 further extend12_all pairs lie outside the window" is wrong. The stored values are 121, 129, 129, 129, 106 and 130 (and 377 for class 8532). "256-975 pairs per class" includes class 8532, whose file is no longer on disk.
4. **Optional, non-blocking.**
   - **Remark.** "Lemma E" in kb/notes/extension_lemmas.md is stated for an extreme vertex a. For a general a, cite its "Remark (other roles)" or the one-line identity alpha(H + {a,x,y}) = max(alpha(H) + 1, alpha(H - a) + 2).
   - **Provenance note.** "the two code versions agree on 15 compared classes" can now say: all 280 pre-restart classes (0..279) are reproduced byte-identically by the final code (this review, C4).
   - **Run time.** "12,668 s wall clock" is the resumed run only.
   - **Code cosmetics.** The comment "vertices 14,15" should say 12, 13, and the docstring advertises an unimplemented `--start` option.

## What is needed for ACCEPT

Text edits only; no recomputation.

1. **Problems 1 and 2.** Replace the brute-force part of the "Acceptance checks" bullet with, for example:

   "cross-checked by a brute force (experiments/20261016-0330-ext12-all/bruteforce_sample.py; bruteforce_sample_results.json). It enumerates all integer pairs x<y of the x4 coordinates (quarter-integer pairs of the set itself) in the window [min A - span, max A + span]. The (4,5) property and the new 3-APs of B are computed from scratch; the h routine and the comparison are imported from extend12_all. Results: 34, 35 and 36 admissible singles ... (unchanged) ...; 20,252,381, 11,128,510 and 14,730,123 (4,5) pairs in the windows. Of these, the brute force h-checked all T1b-type pairs (772, 804, 845) and a random 2,000 of the 36,891, 26,054 and 30,790 T2-type pairs, all with h = 9. The remaining pairs (types T0 and T1a) were counted but not h-checked individually."
2. **Problem 3.** Point to tracked files and correct the README ranges.
3. **Independent evidence (optional but recommended).** Add a pointer to the independent checks of this review: Route L (C5-C7), Route C (C9), the census pass (C8), the reruns (C3, C4) and the judge (C10), all under experiments/referee/L006-round1/.
