VERDICT: ACCEPT

# Referee review, round 2: L005-ext14-all-two-point-extensions (certificate)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-16, 01:17 to 01:40 UTC.
- **Claim reviewed:** `results/proofs/L005-ext14-all-two-point-extensions.md`, the version revised after round 1. Its STATUS reads "revised 2026-10-16 01:17 UTC". The file changed on disk once at the start of this review; everything below refers to the revised version.
- **Scratch folder:** `experiments/referee/L005-round2/`.
- **Independence.** My verifiers (`check_data.py`, `routeF.py`, `t1_brute.py`, `pc_control.py`, `l004_compare.py`) import nothing from `e757/`, `judge/`, the authors' experiment folder or the round-1 referee folder. Two exceptions:
  - `rerun_authors.py` deliberately imports the authors' `extend_all.process`; that is the requested rerun.
  - `compare_routeF.py` reads round 1's stored locus output only to compare counts.
- **Load.** All runs used nice 10 and at most 2 processes, and every foreground command took under 10 minutes.
- **Files reviewed.** sha256 prefixes, identical at the start and end of the review:

| File | sha256 prefix |
|---|---|
| proof (revised) | a72d65ec438734b5 |
| `extend_all.py` | 2f01a10abf32587c |
| `results.json` | 71bd0cf7c0103dff |
| `results.jsonl` | 7dfd7223b1f90c36 |
| `data/census_n14_m12_classes.jsonl.gz` | 7890395ed215ec27 |
| `bruteforce_sample.py` | 35aa86c8ff0d04dc |
| experiment `README.md` | 4a2c2f870a00145a |
| `judge/judge.py` | e061f0e2072e7d09 (= judge.sha256) |

## Summary

The Statement is true and the revised text is accurate. For each of the 2,910 saturated extremal 14-point classes A, every pair of distinct reals x, y not in A with B = A u {x,y} a (4,5)-set has h(B) = 10.

**Case analysis.** I re-derived the T0/T1a/T1b/T2 analysis from scratch and found it sound and exhaustive. The T2 intersection step is in fact forced by linearity (K6): two APs inside 4 points give two coincidences among the 6 distances.

**Authors' code.** I audited `extend_all.py` and found no defect. Rerun unmodified on 14 classes of my choosing (including A_base = class 2440), it reproduces the stored rows exactly. The `--abase-test` reproduces the L001 numbers.

**Route F, my own independent check.** It needs no case analysis:
- It computes the exact deficient locus over all of R^2 by filtering through the relation-line arrangement of one maximum Sidon set, with membership decided by the plain difference definition of Sidon.
- I ran it on 100 classes: 43,388 deficient points, none of them (4,5); no unexplained whole line; a self-test agrees on 392,976 points.
- Its per-class counts agree exactly with round 1's separately written Route L in all 100 classes.
- A positive control shows the detector is not vacuous.

**Further checks.**
- My own T1 enumeration reproduces the counters in 6 classes.
- Brute force on the Sidon definition, with no 3-AP reduction, gives h(B) = 10 for 2,697 (4,5) pairs. That is every T1b pair of classes 2440 and 1524, plus 100 sampled pairs from 4 more classes.
- The frozen judge passes 12/12 sample extensions.
- The census is intact and coincides with the L004 referee's independently realized class list.

**Problems.** I found nothing blocking: only three cosmetic wording or citation notes, plus a note about a kb file outside the claim.

## Steps of the proof, re-derived

1. **Affine invariance.** Being (4,5), h, H(A) and m are invariant under x -> qx+t with q != 0, including q < 0, and A -> A u {x,y} commutes with these maps. So one integer representative per class (classes taken modulo reflection) suffices. Correct.
2. **Upper bound.** h(B) <= h(A)+2 = 10, because a Sidon subset of B meets A in a Sidon subset of A. Correct; the text now justifies it this way.
3. **Lower bound.** Since B is (4,5), it is weak Sidon (K3), so its Sidon subsets are exactly its 3-AP-free subsets (K4), and h(B) = alpha(H(B)). Correct.
4. **New APs.** A 3-AP of B that is not in A contains x or y. If it contains exactly one of them, the other two points lie in A, so that point is in P_x. If it contains both, it is {a,x,y} with a in A in one of 3 roles. Hence:
   - T0: no new AP;
   - T1: x or y in P_x; WLOG x, because the Statement is symmetric in x, y;
   - T2: otherwise.

   The split is exhaustive. Correct.
5. **T0.** H(B) = H(A) plus two isolated vertices, so alpha = 10. Correct.
6. **T1a** (y in no 3-AP of B). y is isolated, so h(B) = h(A u {x}) + 1, which is valid because A u {x}, a subset of B, is (4,5). This is 10 for all 141,153 admissible x. It is also automatic from Henning–Yeo, since f(15) = 9. Correct.
7. **T1b** (y in a 3-AP of B). The other two points of that AP lie in A u {x}, so y lies in the finite set of midpoints and endpoints of pairs of A u {x}, which is exactly `candidates(Ax)`. Correct and exhaustive.
8. **T2 generic points.** Suppose x, y are not in P_x and (x,y) lies on exactly one of the 42 lines (y = 2x-a, y = (x+a)/2, y = 2a-x). Then H(B) = H(A) + {a,x,y} exactly. Its alpha is 10 iff a misses some maximum independent set of H(A). The "core" (the intersection of all maximum Sidon sets) is empty in all 2,910 classes; I recomputed this independently.
9. **T2 other points.**
   - Every other point of a line is either in T1 or on a second line.
   - Lines with the same a meet only at (a,a), which is excluded.
   - Any other intersection gives two APs {a,x,y} and {a',x,y}, i.e. two distinct coincidences among the 6 distances of {a,a',x,y}. That is at most 4 distinct distances, so the point is not (4,5) (K6).
   - The code's exhaustive test agrees. The intersection points have denominator 3 at scale 4, i.e. denominators dividing 12 in original coordinates, as stated.
10. **"Consequently" clause.**
    - "No 16-point (4,5)-set with h <= 9 contains a saturated extremal 14-subset" is immediate.
    - "Equivalently, every 14-subset with h = 8 has m = 11" also needs m in {11,12} for such subsets. That follows from K5 (m <= 12) and K8 (Henning–Yeo: 102 <= 70 + 3m gives m >= 11), and is part of L004's statement ("necessarily with m = 11"). Correct.
    - A 3-point extension (17 points) is also covered, by monotonicity of h.
11. **Remark (Lemma U1, not load-bearing).** A universal vertex a would give tau(H-a) = 6 on 13 vertices with at most 12 - deg(a) edges, and Henning–Yeo would then require 102 <= 101 - 3·deg(a), which is impossible. Correct, and consistent with the computed empty core.

## Checks performed

All commands were run in `experiments/referee/L005-round2/` unless stated otherwise. CENSUS denotes `/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz` and RES denotes the authors' `results.jsonl`.

### 1. Census integrity and the proof's numbers (`check_data.py`, 15 s, all 2,910 classes)

Command: `python3 -I check_data.py CENSUS RES check_data_out.json`

**Census.** For each line, my code checks:
- 14 distinct ints;
- (4,5) on all 1,001 4-subsets;
- 12 APs, equal to the stored `edges`;
- saturation;
- h = 8, by a DFS on the difference definition of Sidon (no 3-AP reduction).

Results:
- `bad = []`.
- 2,910 distinct affine normal forms (translation, scale and reflection).
- A_base is index 2440.
- Every row of results.jsonl agrees with my computation of `set`, `hA`, `n_max_sidon` and `in_all_max_sidon`.
- The number of maximum Sidon sets ranges over 137..150, with sum 417,955; the core is empty in 0/2,910 exceptions.

**The proof's numbers, recomputed from results.jsonl.** All match the text:
- singles: 32..61 per class, 141,153 in total;
- (4,5) T1b pairs: 4,970,208, ranging over 854..2,496;
- T1 pairs: 33,283,559;
- T2 intersection points: 480..498 per class, 1,444,980 in total, 0 of them (4,5);
- 122,220 T2 lines, all with alpha = 10;
- min_h = 10 in every class; hA = 8 in every class; 0 records; 0 classes where the T2 pre-check is true.
- The histogram total equals singles + T1b + intersections + 42 in every class, with the single key 10.

**L004 list** (`l004_compare.py`). The census normal forms equal the 2,910 classes realized independently by the L004 referee (`experiments/referee/L004/my_realizable.txt.gz`): `equal True`.

### 2. Rerun of the authors' code (`rerun_authors.py`, about 20 s)

The authors' `extend_all.process`, unmodified, was run on 14 classes:
- 2440;
- the extremes of t1_pairs, n_t1b_45 and secs: max t1_pairs 1660, max and min n_t1b_45 2564 and 1524, max secs 634;
- 9 classes drawn with seed 1016 (700, 1428, 1494, 1599, 2235, 2294, 2634, 2677, 2701).

Result: 0 differences from the stored rows in all fields except `secs`.

`python3 extend_all.py x <tmp> 1 --abase-test` gives:
- |P_x| = 223, 50 singles, 11,774 T1 pairs, 1,743 (4,5) T1b pairs;
- 42 lines, all with alpha = 10;
- 498 intersection points, 0 of them (4,5);
- 143 maximum Sidon sets; hist {10: 1835}.

These are the L001 numbers. `python3 -m pytest -q tests/test_ext14_all.py` passes (2 tests).

### 3. Code audit of `extend_all.py`

- **Candidates.** `candidates()` adds (a+b)/2, 2a-b and 2b-a for every pair and removes P. At scale 4 every candidate is an integer (x is even), and the assert holds.
- **(4,5) test.** It covers every 4-subset of B:
  - A's own 4-subsets are asserted;
  - `single_ok` covers {v} u 3 points of A, for v = x and v = y;
  - `pair_ok` covers {x,y} u 2 points of A.
- **Search routines.**
  - `has_indep` checks each edge when its highest vertex is added, so it is correct for any labelling.
  - `alpha_masks` is exact.
  - `all_max_indep` enumerates every maximum independent set.
- **Exhibited 10-subsets.** Each is asserted Sidon by the sums definition, including 2x. The run completed, with no `-O` flag and PYTHONOPTIMIZE unset, so all asserts were active.
- **T2.** The hypergraph is H(A) + {a,14,15}. All non-parallel line pairs are intersected with exact Fractions. The exclusions x=y, x in A and y in A are applied, and the (4,5) test is done after scaling by the lcm of the denominators.
- **run.log** shows all 2,910 classes processed in 1,844 s, with 0 record candidates.

### 4. Route F: my own exact deficient locus over all of R^2 (`routeF.py`, 100 classes, 794 CPU-s)

Commands: `python3 -I routeF.py CENSUS routeF_{0,1}.jsonl <classes>` (two halves of `routeF_picked.json`), then `python3 compare_routeF.py` (output in `routeF_summary.json`).

**Method** (scale 12; plain integers):
- Since h(A) = 8, h(B) = 10 iff S u {x,y} is Sidon for some maximum Sidon set S of A.
- K(S) := {(x,y) admissible: S u {x,y} not Sidon} is the union of these lines:
  - x = v and y = v, for v in V(S) = {q+r-p : p not in {q,r}} u {(q+r)/2 : q != r};
  - x + y = p + q;
  - x - y = q - p;
  - 2x - y = p;
  - 2y - x = p;
  - x = y.
- D is contained in K(S_0). For each line l of K(S_0):
  - if l is a line of K(S) for every S, then l is a whole line of D. It must be excluded (x=a, y=a, x=y) or carry a 4-point witness with at most 4 distinct |differences| identically in t, checked with exact linear forms;
  - otherwise D n l is contained in l n K(S*), a finite set. Each of its points is filtered by the definition (S u {x,y} not Sidon for every S, via distinct differences).
- Every surviving admissible point is tested exactly for (4,5).

**Classes.** 100 in total:
- 2440;
- the five classes with extra whole lines (729, 857, 960, 1951, 2437);
- the minimum and maximum of six counters;
- the minimum and maximum of round 1's isolated-point counts;
- 85 classes drawn with seed 20261016.

**Results.**
- The self-test of the line description against the definition passes on 392,976 random and special points, with 0 mismatches.
- 21,259,918 candidate points were generated, all integral at scale 12.
- 43,388 deficient points (174 to 1,350 per class), **0 of them (4,5)**.
- No flagged whole line. The five special classes each have the 2 lines X=v and Y=v, with a parallelogram witness; for class 729 this is {Y,0,104,272} with v = 168, i.e. 0+272 = 104+168.
- A_base has 702 deficient points, equal to L001 round 4 and L005 round 1.
- **Cross-implementation agreement.** The number of deficient points equals round 1's Route L `n_isolated_pts` in all 100 classes (0 mismatches). nS equals the authors' `n_max_sidon` in all 100.

**Positive control** (`pc_control.py`). For A' = A_base minus {a}, with a in {0, 272, 1056} (13 points, h = 8), deficient (4,5) extensions do exist:
- Route F flags the whole lines X=a and Y=a, which have no witness, in all three cases;
- it finds 36, 68 and 110 (4,5) deficient points, each with h = 9 by brute force.

So the detector is not vacuous.

### 5. Own T1 enumeration and pure-definition h (`t1_brute.py`)

Commands: `python3 -I t1_brute.py CENSUS RES t1_brute_{0,1}.jsonl jclaims 20 <3 classes each>` and `... t1_full_{0,1}.jsonl jclaims_full 100000 2440|1524`.

**Classes:** 2440, 1524, 403, 729, 2564 and 2131.

**Counters.** In all 6 classes, my P_x, admissible singles, T1 pairs and (4,5) T1b pairs equal the stored values, e.g. 223/50/11,774/1,743 for class 2440 and 221/61/13,928/2,496 for class 2564.

**h(B) on the plain definition.** For each pair, all C(16,11) = 4,368 11-subsets are scanned and none is Sidon, and a Sidon 10-subset is found. Sampled pairs: h = 10 for 20/20 in each of the 6 classes. Full runs: h = 10 for **all 1,743** T1b (4,5) pairs of class 2440 and **all 854** of class 1524.

### 6. Frozen judge

From the repo root: `python3 judge/judge.py experiments/referee/L005-round2/jclaims/*.json` (`judge.log`). Result: 12/12 `PASS NO-IMPROVEMENT ... n=16 h=10 ratio=5/8`, two T1b extensions from each of the 6 classes. This agrees with my verifier.

### 7. Other evidence cited by the proof

- **`bruteforce_sample_results.json`.** 41 classes; 105,720,197 (4,5) pairs; 0 failures; 0 fallbacks; 502,942 explicit verifications; `singles_match_inside` true in 41/41; wall time 699.9 s. In `bruteforce_sample.py`, extend_all is imported only after the brute-force part (line 150). This matches the text.
- **Round-1 review.** Its Route L, Route C, CP-SAT and judge numbers are quoted correctly.

## Problems found (in order of severity)

None blocking. The case analysis, the code, the data and every number in the revised text check out. Non-blocking notes:

1. **"Totals" wording (cosmetic).** "4,970,208 (4,5) two-point extensions" should read "4,970,208 enumerated (4,5) T1b pairs". The set of all (4,5) two-point extensions is infinite: cases T0, T1a and T2 contain continua. The T1b paragraph of the proof already states it correctly.
2. **Citation (cosmetic).** The "equivalently ... m = 11" clause uses m in {11,12} for 14-point (4,5)-sets with h = 8, i.e. K5 together with K8 (Henning–Yeo). K8 is not in DEPENDS ON. The fact is part of L004's statement ("necessarily with m = 11"), so it is inherited, but citing K8 would be cleaner. Likewise, the DEPENDS ON parenthetical for K3-K6 does not mention linearity (K6), which the T2 step invokes.
3. **Outside the claim (for the kb, not this certificate).** kb/notes/extension_lemmas.md, lines 31-32, still says "case T2 of the sweep is empty by theory". The correct statement, now used in the proof, is that no T2 line is deficient: every T2 line hypergraph has alpha = 10.
4. **Inherited dependency (not a defect of L005).** The Statement's restriction to the 2,910 census classes rests on L004's completeness (ACCEPTED). L004's completeness was re-checked by sampling (28% of prefixes), not by a full second enumeration. I verified only that the data file equals the L004 referee's independently realized class list.
