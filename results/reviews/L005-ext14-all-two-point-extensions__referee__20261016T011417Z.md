VERDICT: NEEDS-WORK

# Referee review, round 1: L005-ext14-all-two-point-extensions (certificate)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-16, 00:12 to 01:14 UTC.
- **Claim reviewed:** `results/proofs/L005-ext14-all-two-point-extensions.md`, the version with STATUS "submitted (2026-10-16 00:07 UTC)".
- **Files reviewed.** sha256 prefixes, identical at the start and end of the review:

| File | sha256 prefix |
|---|---|
| proof `L005-...md` | 87ef1643c09c01dd |
| `extend_all.py` | 2f01a10abf32587c |
| `results.json` | 71bd0cf7c0103dff |
| `results.jsonl` | 7dfd7223b1f90c36 |
| `data/census_n14_m12_classes.jsonl.gz` | 7890395ed215ec27 |
| `judge/judge.py` | e061f0e2072e7d09 (= judge.sha256) |

- **README.** The experiment README was edited by the main session during the review: a brute-force section was added (be21d7ff -> 4a2c2f87). The proof does not cite that section, and nothing below relies on it.
- **Scratch folder:** `experiments/referee/L005-ext14-all-two-point-extensions/`.
- **Independence.**
  - My verifiers (`check_data.py`, `cases.py`, `locus.py`, `ilp_check.py`) import nothing from `e757/`, `judge/` or the authors' experiment folder.
  - `rerun_authors.py` deliberately imports the authors' `extend_all.process`. That is the requested rerun.
  - The frozen judge was only executed, on claim files in my scratch folder.
- **Load.** Every computation ran at nice 15 (effectively 19). Foreground commands took under 10 minutes; the two long runs ran in the background.

## Summary

The certified Statement is true, and every number in the proof that I checked is reproduced exactly. For each of the 2,910 census classes A, every pair of distinct reals x, y not in A with B = A u {x,y} a (4,5)-set has h(B) = 10.

I verified this in two independent and complete ways.

**Route L (no case analysis, no 3-AP reduction).**
- Since h(A) = 8, h(B) = 10 iff S u {x,y} is Sidon for some maximum Sidon set S of A.
- So the deficient pairs form the exact locus D, the intersection over all S of the union of the relation lines of S u {X,Y}.
- I computed D over all of R^2 for all 2,910 classes. In every class, every whole line of D is excluded by hypothesis (X=a, Y=a, X=Y) or is identically non-(4,5). D has 174 to 1,350 isolated points per class, none of them a (4,5)-set.

**Route C (my own re-implementation of the T0/T1a/T1b/T2 analysis, all 2,910 classes).**
- h is computed from maximum Sidon sets by the difference and sum definitions, never from the 3-AP hypergraph.
- Every per-class counter of `results.jsonl` is reproduced exactly: P_x, the admissible singles, the T1 pairs, the (4,5) T1b pairs, the T2 intersection points, and the number of maximum Sidon sets.
- I found no deficient extension.

**Further checks.**
- CP-SAT on the Sidon definition gives h = 10 on 4,420 random (4,5) extensions.
- The frozen judge passes 16 of them.
- The authors' code, rerun on 37 classes, reproduces the stored rows byte-for-byte.
- I re-derived the case analysis and found it sound and exhaustive. The T2 generic-point argument is correct, and the treatment of line intersections is correct; in fact it is forced by linearity K6.

**Why NEEDS-WORK.** The proof text contains two false factual sentences and one unfinished placeholder:
- the claim of "498 intersection points per class" is false; the per-class counts range from 480 to 498;
- "m=12 ... recomputed inside extend_all.py" is false: that code never computes m;
- the "Independent cross-check" bullet is still a "to be added" stub.

All of these are text-only fixes; the exact edits are listed at the end. No mathematical or computational problem was found.

## Steps of the proof, re-derived

1. **Affine invariance.** Being (4,5), h, H(A) and m are invariant under x -> qx+t with q != 0, including reflection, and A -> A u {x,y} commutes with these maps. So one representative per class suffices. Correct.
2. **h(B) <= h(A)+2 = 10.** Correct, but it follows from the definition, not from K4 (Problem 4).
3. **Exhaustive split.**
   - A new 3-AP of B contains x or y.
   - If some new AP contains exactly one of them, that point is in P_x: case T1, and WLOG x is in P_x because the Statement is symmetric.
   - If not, but a new AP exists, every new AP contains both x and y, so it is {a,x,y} with a in A, in one of 3 roles: case T2.
   - Otherwise no new AP exists: case T0.
   - The split is exhaustive.
4. **T0.** H(B) = H(A) plus two isolated vertices, so alpha = 10. Since B is (4,5), K3 and K4 give h(B) = alpha. Correct.
5. **T1a** (y in no 3-AP of B). H(B) = H(A u {x}) plus the isolated vertex y, so h(B) = h(A u {x}) + 1. This needs A u {x} to be (4,5), which holds because it is a subset of B. Correct.
   - The "always 10" part also follows from f(15) = 9.
   - The check is not vacuous. In 5 classes (729, 857, 960, 1951, 2437) some v in P_x has h(A u {v}) = 8, but A u {v} is not (4,5) (`extra_whole_lines.log`). These v are correctly excluded from the 141,153 admissible singles.
6. **T1b** (y in some 3-AP of B). The other two points of that AP lie in A u {x}, so y ranges over the midpoints and endpoints of pairs of A u {x}. That is exactly `candidates(Ax)`, so the candidate set is exhaustive. Correct.
7. **T2 generic points.**
   - If x, y are not in P_x and (x,y) lies on exactly one of the 42 lines, then H(B) = H(A) + {a,x,y} exactly.
   - Hence alpha = max(alpha(H)+1, alpha(H-a)+2), which is 10 iff a lies outside some maximum independent set.
   - There is nothing else non-generic on a line: a point is either in T1, on a second line, or excluded (x=y, x or y in A). Correct.
8. **T2 intersections.**
   - Lines with the same role are parallel.
   - Lines with the same a but different roles meet only at (a,a), which is excluded.
   - Any other intersection gives two APs {a,x,y} and {a',x,y} with a != a' sharing the pair {x,y}. That contradicts linearity (K6 [published]), so no intersection point can be (4,5).
   - The code's exhaustive test (0 such points are (4,5)) agrees. Correct, and in fact forced.
9. **"Consequently" clause.** It is correct given L004, since a 14-point (4,5)-set with h = 8 has m in {11, 12} by K5 and K8. It inherits L004's completeness, which is ACCEPTED; L004's completeness was checked by sampling, not by a full second enumeration. The proof states this dependency.

## Checks performed

Commands run in the scratch folder unless stated otherwise. CENSUS denotes `/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz`.

### D. Input and output integrity (`check_data.py`, 31 s)

Command: `python3 check_data.py CENSUS .../results.jsonl .../results.json ../L004/my_realizable.txt.gz check_data_out.json`

**Census file.**
- All 2,910 lines are valid:
  - 14 distinct integers;
  - (4,5) on all 1,001 4-subsets;
  - the computed 3-APs equal the stored `edges`, and there are 12 of them;
  - every non-extreme point is a midpoint;
  - h = 8 by a DFS on the difference definition, with no Sidon 9-subset.
- There are 2,910 distinct affine normal forms (translation, scaling and reflection). They coincide exactly, in both directions, with the 2,910 sets realized independently by the L004 referee (`experiments/referee/L004/my_realizable.txt.gz`). So the data file is the certified class list.
- A_base is class 2440, literally {0,136,...,1056}.
- No class has a vertex lying in every maximum Sidon set. This independently confirms the T2 pre-check and Lemma U1.
- The number of maximum Sidon sets ranges from 137 to 150 and equals the authors' count in every class.

**results.jsonl / results.json.**
- 2,910 rows with class ids 0..2909; each set equals its census line.
- In every row: hA = 8, min_h = 10, no records, t2_line_h = [10], 42 lines, and t2_isect_45 = 0.
- The histogram total equals n_single_45 + n_t1b_45 + 42 in every row.
- results.json equals results.jsonl.
- Totals: 141,153 singles (range 32 to 61) and 4,970,208 (4,5) pairs (range 854 to 2,496), as claimed.
- **t2_isect_pts is not constant.** It ranges from 480 to 498 with this distribution: 498: 1,884 classes; 496: 443; 494: 340; 492: 114; 490: 67; 488: 26; 486: 21; 484: 10; 482: 4; 480: 1.

### R. Rerun of the authors' code (`rerun_authors.py`, 47 s)

The authors' `extend_all.process`, unmodified, was run on 37 classes:
- 24 seeded-random classes, 0, 2909 and 2440;
- the minimum and maximum of every counter: Px_size, n_single_45, t1_pairs, n_t1b_45, n_max_sidon and t2_isect_pts (classes 590, 1215, 712, 1352, 1660, 1524, 2564, 1, 121, 0, 2879).

Every output equals its stored row (all fields except `secs`): 0 mismatches. The `--abase-test` input gives |P_x| = 223, 50 singles, 11,774 T1 pairs, 1,743 (4,5) T1b pairs, 42 lines all 10, 498 intersection points, 0 of them (4,5), and 143 maximum Sidon sets. These are the L001 numbers.

### C. Route C, independent case analysis on all 2,910 classes (`cases.py`, 3,062 CPU-s)

Command: `python3 cases.py CENSUS cases_all.jsonl --range 0:2910`. Summary in `summary.json` (`summarize.py`).

**Method.**
- Scale by 12, plain integers.
- h(A u {x}) = 9 iff S u {x} is Sidon for some maximum S.
- h(B) = 10 iff S u {x,y} is Sidon for some maximum S (sums test). The fallback, a full DFS, was never needed.
- T2 intersections are computed in closed form (3x = 2a+b, a+2b, 4b-a).

**Result.**
- All seven counters equal the stored values in all 2,910 classes. Sums: P_x 648,605; singles 141,153; T1 pairs 33,283,559; (4,5) T1b pairs 4,970,208; T2 intersection points 1,444,980, of which 0 are (4,5); maximum Sidon sets 417,955.
- The T1b h-histogram is {10: 4,970,208}.
- No class has a T1a deficit, a T1b deficit, a universal vertex or a T2-intersection deficit.

### L. Route L, the exact deficient locus over all of R^2, all 2,910 classes (`locus.py`, 4,578 CPU-s)

Commands: `python3 locus.py census CENSUS locus_all.jsonl --range 0:2910 --selftest-every 97`, run in three segments: rows 0..1723, 1720..1949 and 1950..2909. The 4 overlapping rows agree.

**Method.**
- L(S) is generated by brute force over all pairs of multisets in S u {X,Y}.
- Whole lines of D are the lines common to all L(S).
- For each other line l of L(S_0), the points of l lying in L(S) for all S are found by intersecting l with the lines of up to 4 sets S_j for which l is not in L(S_j), and then filtering by membership in every L(S).
- Every point found is re-checked against the definition: S u {x,y} is not Sidon for every S.
- In 30 classes, the membership predicate is checked against the definition (sums test, 8 of the S per point) on up to 600 points each: random points, points built from midpoints and endpoints, and points of D.
- Whole lines other than X=a, Y=a, X=Y must carry a 4-subset of A u {X,Y} with at most 4 distinct |differences| identically along the line. This is checked symbolically with linear forms in t.
- Isolated points are tested exactly for (4,5).

**Result.**
- 0 anomalies.
- Every class has the 29 excluded lines (14 + 14 + 1).
- 5 classes (729, 857, 960, 1951, 2437) also have the pair of whole lines X=v and Y=v. Each carries a symbolic witness: A u {v} is not (4,5) (for example, for class 729, v = 168 and 0 + 272 = 104 + 168).
- Isolated points: 174 to 1,350 per class, 1,176,308 in total, 0 of them (4,5).
- For A_base: 29 whole lines and 702 isolated points, identical to the L001 round-4 referee's independent locus computation.

### Controls for Route L and Route C (the referee's own code)

- **PC2** (`locus.py controls`, 6 classes). For A' = A minus p with h(A') = 8, the lines X=p and Y=p are detected as whole lines with (4,5) generic points: 6/6.
- **PC3** (`pc3.py`, 9 thirteen-point sets A minus one point, which have many genuine deficient extensions, i.e. 15-point sets with h = 9). The two routes agree exactly:
  - T1a deficits correspond to flagged vertical and horizontal whole lines;
  - every Route-C deficient (4,5) pair (37 to 106 per set) lies in D;
  - every isolated (4,5) point of D (0 to 43 per set) is a Route-C deficient pair;
  - X+Y = b+c whole lines carry parallelogram witnesses. All ok.
- **PC4** (`pc4.py`, Fibonacci prefixes of lengths 7, 9 and 11, which have universal vertices). The T2 lines 2X-Y=a and X-2Y=-a of the universal vertices a appear as flagged whole lines. The deficient pairs agree in both directions (176 / 219 / 99 Route-C deficient pairs). All ok.
- **Robustness** (`robust_locus.py`, 10 classes). Recomputing D with the maximum Sidon sets in reversed order (a different S_0 and different seeds) and NT = 1 gives identical whole lines and identical isolated-point sets.

### CP-SAT and the frozen judge

- **CP-SAT** (`ilp_check.py 40 10 4242` and `ilp_check.py 400 10 99`). The model forbids every equal-difference coincidence directly and maximises the number of chosen points. Results:
  - h(A) = 8 in all 401 + 41 sampled classes;
  - h = 10 for all 4,420 random (4,5) T1b extensions;
  - every optimal set was re-checked Sidon.
- **Frozen judge** (`make_jclaims.py`, then from the repo root `python3 judge/judge.py experiments/referee/L005-ext14-all-two-point-extensions/jclaims/*.json`):
  - 16/16 random T1b extensions from 8 classes, including 2440, give PASS NO-IMPROVEMENT with n=16, h=10;
  - 3/3 deficient-locus points of A_base give FAIL (not a (4,5)-set), as Route L predicts.

### Code review of `extend_all.py`

- **Candidate sets** are exhaustive.
  - `candidates(P)` adds (a+b)/2, 2a-b and 2b-a for every pair and removes P; it is used for P_x and for the T1b partners of A u {x}.
  - At scale 4, integrality is asserted, and the assertion holds because x is even.
- **Arithmetic** is exact throughout: integers and Fractions. `random` is imported but never used.
- **The (4,5) test** covers every 4-subset of B:
  - A's own 4-subsets are asserted;
  - `single_ok(x)` and `single_ok(y)` cover {v,a,b,c};
  - `pair_ok` covers {x,y,a,b}.
- **Search routines.**
  - `has_indep` checks each edge when its highest vertex is added, so it is correct for any vertex labelling.
  - `alpha_masks` is exact.
  - `all_max_indep` enumerates all maximum independent sets.
- **Exhibited 10-subsets** are asserted Sidon by the sums definition, including 2x. The run completed, so all 4,970,208 assertions held.
- **T2.** The hypergraph is H(A) + {a,14,15}, and the label order is irrelevant. All 588 pairs of non-parallel lines are intersected; the 42 pairs with the same a meet at (a,a), which is excluded. The exclusions x=y, x in A and y in A are applied. The (4,5) test of the intersection points is done after scaling by the lcm of the denominators.
- **Minor.** The code never computes m (see Problem 2).

## Problems found (in order of severity)

1. **False count in the T2 step.** The proof says "the 498 pairwise intersection points per class were tested exactly". The number of intersection points, after removing x=y and x or y in A, is 498 only in 1,884 classes. It ranges from 480 to 498 (distribution in check D), with 1,444,980 in total. The authors' rows and my Route C agree class by class. The conclusion is unaffected, since none of these points is (4,5) and by K6 none can be. The sentence is still false as written.
2. **False evidence pointer in "Sanity checks".** "Every class has h(A)=8, m=12, 14 points (recomputed inside extend_all.py)" is false. `extend_all.py` asserts n = 14 and recomputes h(A), but it never computes or checks m: `masks_of(A)` is used only for alpha, and `ap_triples(A)` only for T2. The fact itself is true: it is part of L004, and I re-checked it for all 2,910 lines in `check_data.py`. The text must point to the right evidence.
3. **Unfinished placeholder.** The "Independent cross-check: (to be added by the referee round ...)" bullet is a stub. A certificate should name its independent evidence:
   - this review's Route L and Route C, with their folder;
   - and/or the brute-force section now in the experiment README (`bruteforce_sample.py`), which the proof does not mention.
4. **Misattributed justification.** "h(B) <= h(A)+2 = 10 trivially (K4: ...)". The bound follows from the definition, because a Sidon subset of B meets A in a Sidon subset of A. K4 is what turns the exhibited 3-AP-free 10-subsets into Sidon sets.
5. **Imprecise wording.** "Lemma U1 predicts T2 empty". U1 predicts that every T2 line has alpha = 10, i.e. no T2 line is deficient. It does not predict that case T2 is empty.
6. **Optional fixes, non-blocking.**
   - The Remark applies Henning–Yeo to H(A)-a without stating its hypotheses (linear, F7-free). They hold by K6 and K7, and the Remark is not load-bearing.
   - "Scaled by 4 so that all midpoints and endpoints of pairs below are integers" does not cover the T2 intersection points, which are thirds and are handled with Fractions.
   - The T2-intersection step could cite K6 (two APs sharing {x,y}), which makes "none is (4,5)" a theorem rather than an observation.

## What is needed for ACCEPT

1. Replace the 498 sentence with, for example: "the pairwise intersection points of the 42 lines (480 to 498 per class after removing x=y and x,y in A; 1,444,980 in total; 498 for A_base) were tested exactly; none of them gives a (4,5)-set in any class, as linearity (K6) forces: two APs {a,x,y}, {a',x,y} with a != a' share the pair {x,y}."
2. In "Sanity checks", replace "(recomputed inside extend_all.py)" with a correct pointer. For example: "n = 14 asserted and h(A) = 8 recomputed in extend_all.py; m = 12 and saturation from L004, re-checked for all 2,910 lines by the referee (experiments/referee/L005-ext14-all-two-point-extensions/check_data.py)".
3. Fill in the "Independent cross-check" bullet with the actual evidence, for example: "referee round 1 (this review): Route L, the exact deficient locus over all of R^2, and Route C, an independent re-implementation of the case analysis, both on all 2,910 classes with all counters equal; CP-SAT on 4,420 random extensions; frozen judge 16/16".
4. Fix the K4 parenthesis (Problem 4) and the "T2 empty" wording (Problem 5).

No recomputation is required. The numbers in the proof are correct except the 498 sentence.
