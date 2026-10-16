VERDICT: ACCEPT

# Referee report, round 3: L003-census-small-n-extremal-sets (certificate: exhaustive enumeration with exact realization)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-14, round 3. This is my own verdict. I wrote new code and did not reuse code from rounds 1 or 2.
- **Claim reviewed:** `results/proofs/L003-census-small-n-extremal-sets.md` as revised in eadf338 (unchanged at HEAD c9ad201). Evidence: `experiments/20261014-1430-small-counts/`, including the gitignored `n11/results/`.
- **Scratch:** `experiments/referee/L003-round3/` (11 MB in total; largest file 4.8 MB, gzipped).
- **Independence:**
  - My programs (`sat3.c`, `patc3.c`, `defcheck.py`, `dbgcheck.py`, `dbgcheck2.py`, `compare3.py`, `nonsat3.py`, `small_n3.py`) import nothing from `e757/`, `judge/` or earlier referee directories.
  - Census files and `data/small_records.json` were read only as data.
  - The census engine ran only inside the claim's own test (C12).
  - The frozen judge was run read-only on claim files in my scratch directory.
- **Load:** one `nice -n 10` process at a time, on a machine shared with the 4-worker n = 14 census. The longest computation took 317 s (n = 11, linearity-only pruning).

## Summary

The Statement is correct. I verified all of it myself, except the n = 12 bullet, which is cited from the accepted certificate L002 (its statement says exactly this).

**Saturated counts.** A new enumerator reproduces the counts 1, 4, 66, 1,262, 6,644 and 466,961. Its design:
- outside-in variable order;
- a float LU candidate that is accepted only after an exact integer certificate, with a Bareiss fallback;
- the Sidon number computed from the definition (all pairwise differences distinct).

It ran in these pruning modes:
- n ≤ 9: no pruning at all, all ∏ j(n−1−j) midpoint maps;
- n = 10: K30 only, linearity only, and both;
- n = 11: linearity only (582,628,416 maps, no K30) and K30 plus linearity.

For every n = 6..11 my list of affine classes is set-equal to the census's realized list. I re-checked against the definitions in pure Python:
- every ordered leaf verdict at n = 10;
- every excluded set with h > 7 at n = 11, plus a 1-in-20 sample of all other n = 11 verdicts.

**Non-saturated part.** I verified it with my own witnesses for every n = 6..11, none taken from the census. They come from a gluing, from a saturated set plus a generic point, and from my own random search at n = 8 and n = 10. For each witness an exact argument shows that it lies in a one-parameter family of pairwise inequivalent extremal sets.

**Small n.** The n ≤ 5 assertions hold for every real x > 4, by a symbolic coincidence analysis. Also f(4) = 3 and f(5) = 4, because every linear 3-graph on 4 or 5 vertices has τ ≤ 1.

**Text.** Round 2's wording fixes are in place, and the text now matches the evidence. Only editorial points remain (the title, two missing tags, one loose phrase in Step 4). None of them changes the truth of any sentence of the Statement or invalidates a proof step, so I accept.

## Steps and status

| # | Step | Status |
|---|---|---|
| S1 | Saturated affine classes with h = f(n): 1, 4, 66, 1,262, 6,644, 466,961 for n = 6..11 | **Verified** (C1–C5) |
| S2 | For each n = 6..11 a realizable non-saturated extremal pattern exists; each gives infinitely many affine classes | **Verified** (C7, C10) |
| S3 | Up to affine equivalence: infinitely many for 4 ≤ n ≤ 11; exactly one for n = 1, 2, 3; exactly 54,243 for n = 12, the smallest n ≥ 4 with finitely many | **Verified** for n ≤ 11 (C7, C8). n = 12 cited from L002 (ACCEPT; C11) |
| 1 | Reduction to class O, α ≤ f(n), 1 ≤ m ≤ n−2 | **Verified** (C10) |
| 2 | DFS enumeration by (n, m) | Saturated cells **verified** with my own pattern counter (C6). Non-saturated cells not redone: the Statement does not use them, and round 1 (C5) matched every cell |
| 3 | Exact realization, rigidity, bijection with affine classes, judge checks | **Verified** (C1–C5, C9, C11) |
| 4 | Non-saturated existence; genericity argument; record sets | **Verified** (C7, C10, C11). The "exact counts for n ≤ 10" and the n = 11 samples were not redone; the Statement does not use them (round 1, C6). Wording: E3 |

## Checks performed

All commands are run from `experiments/referee/L003-round3/` unless stated otherwise.

### C1. Saturated sets by brute force over ALL midpoint maps, n = 6..9 (`sat3.c`)

**Mathematical basis.** A saturated (4,5)-set gives every interior rank j exactly one AP (L(j), j, R(j)) (C10).

**Search.** `sat3` enumerates all maps with 0 ≤ L(j) < j < R(j) ≤ n−1, assigning j in the order 1, n−2, 2, n−3, …. With `k30=lin=0` nothing is pruned.

**Each leaf** runs these steps:
1. **Solve.** Solve 2x_j = x_L + x_R with x_0 = 0 and x_{n−1} = 1 by float LU with partial pivoting. Then round X = D·x, with D = |det|.
2. **Certify.** Accept X only if the exact integer identities 2X_j = X_L + X_R, X_0 = 0 and X_{n−1} = D hold. Otherwise run an exact fraction-free Bareiss solve (`__int128`); a singular system is counted.
3. **Check order and normalise.** Require strict order, then divide by the gcd.
4. **Check the AP set.** Count the 3-APs exactly; there must be exactly n−2. This is equivalent to "AP set = map", because every map AP is present.
5. **Check the set.** Test weak Sidon and (4,5) on every 4-subset.
6. **Compute h.** h is the largest Sidon subset, by DFS over subsets with a used-difference table.
7. **Output.** Print the set if h = T and X ≤lex its reflection, so that each class is printed once.

**Commands:** `./sat3 N T 0 0`.

| n | maps | singular | fallback | orderfail | extra AP | not (4,5) | (4,5) | h histogram | classes |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 576 | 0 | 0 | 411 | 60 | 103 | 2 | 4:2 | **1** |
| 7 | 14,400 | 0 | 0 | 12,301 | 957 | 1,134 | 8 | 5:8 | **4** |
| 8 | 518,400 | 0 | 0 | 483,830 | 18,016 | 16,422 | 132 | 5:132 | **66** |
| 9 | 25,401,600 (7.1 s) | 0 | 0 | 24,698,668 | 398,634 | 301,774 | 2,524 | 6:2,524 | **1,262** |

**Validation of the exact path.** The Bareiss path was never needed above, so I forced it on every leaf (`./sat3 N T 0 0 -1 1`, n = 6, 7, 8, all 533,376 maps). The output is byte-identical to the float-plus-certificate path.

**Other observations.**
- No saturated (4,5)-set with n ≤ 9 has h ≠ f(n).
- None is reflection-symmetric (sym = 0).
- The largest primitive coordinate is 2^{n−2}.

### C2. n = 9 and n = 10 with pruning (each rule proved in C10)

**n = 9.**
- K30 only: 1,506,374 leaves.
- Linearity only: 138,208 leaves.
- Both: 10,264 leaves.

All modes give the same 2,524 (4,5)-sets and the same 1,262 class lines, identical to the brute force after sorting.

**n = 10.**

| mode | leaves | time |
|---|---|---|
| K30 + linearity | 338,595 | 0.7 s |
| linearity only | 7,887,520 | 4.0 s |
| K30 only | 51,841,968 | 33 s |

In every mode:
- singular = 0 and fallback = 0;
- (4,5)-sets = 51,412, with h histogram 6:13,288, 7:38,106, 8:18;
- **6,644 classes**, with sorted lists identical across modes (md5 e612ab47…).

The leaf counts equal those reported independently by rounds 1 and 2.

### C3. n = 11 (`./sat3 11 7 1 1`, `./sat3 11 7 0 1`)

| mode | leaves | orderfail | extra AP | not (4,5) | (4,5) | h histogram | classes | time |
|---|---|---|---|---|---|---|---|---|
| K30 + linearity | 13,860,888 | 11,226,432 | 934,582 | 492,978 | 1,206,896 | 7:933,922 8:272,960 9:14 | **466,961** | 25 s |
| linearity only (no K30) | 582,628,416 | 579,993,960 | 934,582 | 492,978 | 1,206,896 | same | **466,961** | 317 s |

- In both runs singular = 0, fallback = 0 and sym = 0.
- The sorted class lists are identical (md5 362ba25d…).
- In each row the categories sum exactly to the leaf count.

So the n = 11 count needs neither K30 nor any filter; linearity alone suffices (K6 [published], re-proved in C10). Rounds 1 and 2 independently ran K30-only (2,195,189,896 maps) with the same result.

### C4. Set-level comparison with the census (`compare3.py`)

**Census data read:**
- n ≤ 10: `results/n{n}_m{n-2}_real.json.gz`;
- n = 11: all 418 `n11/results/post/real_*.json.gz` batches (466,961 records).

Each census set is normalised by my own code: min 0, divide by the gcd, then the lexicographic minimum of the set and its reflection.

**Results.** For n = 6, 7, 8, 9, 10, 11:
- census records = census classes = 1, 4, 66, 1,262, 6,644, 466,961;
- **mine − census = census − mine = 0**;
- no duplicate lines.

### C5. My checks re-done from the definitions in pure Python

1. **Output sets (`defcheck.py`).** Checked: all output sets for n ≤ 10 (7,977 sets) and a random 3,000 at n = 11 (seed 757). Result: **0 bad**. For each set it verifies:
   - strictly increasing, min 0, gcd 1, and ≤ its reflection;
   - every 4-subset has ≥ 5 distinct distances;
   - exactly n−2 APs, one per interior point;
   - no Sidon (T+1)-subset, and some Sidon T-subset.
2. **Every ordered leaf at n = 10, K30 + linearity (`dbgcheck.py`).** Result: **0 bad**.
   - 51,412 (4,5)-sets, each with h recomputed exhaustively. This includes the 38,124 with h > 6, which are correctly excluded.
   - 31,614 sets flagged "extra AP", each confirmed to have an AP count ≠ n−2 and to fail (4,5).
   - 13,854 sets with the right AP set, each confirmed to fail (4,5).
3. **n = 11, K30 + linearity, piped (`dbgcheck2.py`, 227 s).** Result: **0 bad**.
   - All 272,974 excluded (4,5)-sets with h ∈ {8, 9} were re-checked exhaustively.
   - A 1-in-20 sample of the rest was re-checked: 46,926 extra-AP, 46,405 with h = 7, and 24,812 not-(4,5) verdicts.

So a wrong h or a wrong (4,5) rejection cannot hide a missing class.

### C6. Saturated-cell pattern counts (`patc3.c`; Step 2's DFS completeness on the cells the Statement uses)

**Method.**
- Search: K30 + linear maps.
- F7 test: my own. For a centre vertex of degree ≥ 3 and three of its edges, it tries every choice of two complementary transversals and asks whether both are edges.
- α ≤ T test: every (T+1)-subset must contain an edge.

**Results** (labelled / reflection-symmetric / up to reflection, F7-free):

| n | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|
| labelled | 2 | 10 | 260 | 8,570 | 79,488 | 9,871,248 |
| reflection-symmetric | 0 | 0 | 0 | 22 | 42 | 454 |
| up to reflection | 1 | 5 | 130 | 4,296 | 39,765 | 4,935,851 |
| F7-containing (labelled) | 0 | 10 | 110 | 1,656 | 11,946 | 819,030 |

- All F7-free values equal the README, `results/summary.json` and `dfs_n11_m9.json`.
- The F7-containing counts equal round 1's.
- Total time: 14 s.

### C7. Non-saturated existence and the infinite families, exact (`nonsat3.py`, `nonsat3.log`)

**Per witness x0** (Fractions throughout):
1. **Definitions.** (4,5) holds, m < n−2, and h = f(n) by exhaustive Sidon search.
2. **Solution space.** The AP system has rank m. A null-space vector v is chosen with x0, v and **1** linearly independent.
3. **Order interval.** I computed the exact open interval I ∋ 0 on which x0 + s·v stays strictly increasing.
4. **Coincidences.** For every pair of distance forms:
   - The forms that vanish identically along the line are exactly the AP coincidences of x0's pattern; this is asserted.
   - x0 has no other coincidence.
   - Every other form has at most one root.
5. **Spot check.** Six rational s ∈ I outside the roots were re-checked from the definitions (same AP set, (4,5), h = f(n)). The seven normal forms (x0 and the six) are pairwise distinct.

**Witnesses** (`ALL_OK 8`):

| n | witness (integer form) | m | dim V | order interval I | roots in I |
|---|---|---|---|---|---|
| 6 | gluing {0,1,2} ∪ ((13/7)·{0,1,2}+50) = {0,7,14,350,363,376} | 2 | 4 | (−∞, 7) | 9 |
| 7 | saturated {0,4,7,8,9,14} + point 332599/7919 | 4 | 3 | (−∞, 39595) | 11 |
| 8 | own random search (25 tries): {0,268323,273292,336646,400000,536646,568323,800000} | 5 | 3 | (−9938/7, 31677) | 4 |
| 8 | record set (data/small_records.json) | 5 | 3 | (−266443, 267053) | 4 |
| 9 | saturated {0,4,7,8,9,14,20,40} + point 950281/7919 | 6 | 3 | (−∞, 158380) | 22 |
| 10 | own random search (1,839 tries): {0,6500000,6866028,7704131,8168936,8542234,8633741,8725248,10584468,13000000} | 7 | 3 | (−366028/5, 746596/3) | 8 |
| 11 | saturated {0,10,11,20,22,29,34,48,85,170} + point 4038691/7919 | 8 | 3 | (−∞, 673115) | 37 |
| 11 | record set | 8 | 3 | (−222590/7, 111865/3) | 3 |

**Conclusion of the argument.**
- **Same structure along the line.** For s ∈ I outside the roots, x(s) has exactly the coincidences of x0. Hence it is a (4,5)-set with the same AP set and h = f(n).
- **Same orientation.** Two members related by x ↦ qx + t with q > 0 force q = 1, s = s′ and t = 0, because x0, v and **1** are independent.
- **Reflection.** For each s, x(s′) ∈ span(J·x(s), **1**) holds for at most one s′; otherwise span(x0, v, **1**) would lie in a 2-dimensional space. Here J reverses the coordinate order.
- **Count.** So each affine class contains at most two members of the family, and there are infinitely many classes for every n = 6..11.

### C8. n ≤ 5 (`small_n3.py`)

- **{0,1,2,x} and {0,1,2,x,3x}.** The points are linear forms in x.
  - The only identically equal distance pair is the AP (0,1,2).
  - Every other coincidence has its root at x ≤ 4 (the maximum root is exactly 4).
  - The order holds for x > 2.
- **Consequence.** For **every real x > 4** both sets are (4,5)-sets whose only AP is (0,1,2), with h = 3 and h = 4 respectively. Re-checked at x = 41/10, 5, 6, 17 and 1001/3.
- **Inequivalence.** The gap vectors (1, 1, x−2) and (1, 1, x−2, 2x) determine x up to reflection. A reflection would need x = 3 or x = −2. So distinct x > 4 give distinct classes.
- **f(4) = 3 and f(5) = 4.** All linear 3-graphs on 4 vertices (4 of them) and on 5 vertices (25) have τ ≤ 1. With h = α for weak Sidon sets, this gives h ≥ 3 and h ≥ 4. Note that the Henning–Yeo bound gives only 3 at n = 5.
- **n = 3.** h({a < b < c}) = 2 iff the set is a 3-AP, so all extremal 3-sets are affinely {0,1,2}. For n = 1, 2 the claim is trivial.

### C9. Frozen judge

From the repo root, `python3 judge/judge.py experiments/referee/L003-round3/spot/*.json` gives **18/18 `PASS NO-IMPROVEMENT`**, each with h = f(n). The 18 sets are:
- 16 random saturated classes from my enumeration (1 at n = 6, 3 at each of n = 7..11, seed 20261014);
- my two own non-saturated witnesses (n = 8, 10).

(My first call failed only because the claim ids did not equal the file names; I renamed the files and re-ran.)

### C10. Mathematics re-derived

1. **(4,5) ⟹ weak Sidon.** Suppose x_a + x_d = x_b + x_c with a < b < c < d. That gives two distance coincidences inside 4 points, so at most 4 distinct distances.
2. **Midpoints.** Midpoints are injective (two APs with midpoint j give a sum coincidence on disjoint pairs) and never extreme. Hence m ≤ n−2, and m = n−2 iff every interior rank is the midpoint of exactly one AP. So the map enumeration covers every saturated set.
3. **Linearity.** Two distinct APs sharing two points span 4 points. Their coincidences involve different pairs of distances, so those 4 points have at most 4 distinct distances.
4. **K30.** If i ≤ i′, k ≤ k′ and (i,k) ≠ (i′,k′), then x_j = (x_i + x_k)/2 < (x_{i′} + x_{k′})/2 = x_{j′}. The pruning rule "j < t forbids L(j) ≥ L(t) and R(j) ≥ R(t)" is its contrapositive. Equal endpoint pairs would force equal midpoints.
5. **Rigidity.** M = 2I − B is weakly chained diagonally dominant: follow R(j) upwards to a row with R = n−1. So M is a nonsingular M-matrix, and every saturated map has a unique solution. Observed: singular = 0 everywhere.
6. **Classes.** Rational rigid sets have a unique primitive integer normal form up to reflection. So realizable saturated patterns up to reflection correspond bijectively to affine classes; sym = 0 at every n.
7. **h = α for weak Sidon sets (K4).** A Sidon failure x + w = y + z must have x = w or y = z, which is a 3-AP.
8. **Values of f.** The published bound h ≥ ⌈(9n+6)/17⌉ (Henning–Yeo via Ma–Tang) gives 4, 5, 5, 6, 6, 7 for n = 6..11. Each value is attained by the sets above, so f(6..11) are exact. This does not depend on K24/K29.
9. **Positive dimension.** For a non-saturated realizable pattern, rank ≤ m ≤ n−3, so dim V ≥ 3. The realizations form a nonempty open subset of V, because the order and the "no extra coincidence" conditions are open. Affine orbits have dimension 2, so there are infinitely many classes (C7 does it explicitly).

### C11. Text audit against the evidence

- **DEPENDS ON figures.**
  - 3,263,957 = 4,935,851 − 1,671,894 (`n11_m9_postprocess_summary.json`).
  - 2,195,189,896 is round 1's K30-only leaf count.
- **Step 3 judge sentence.** I replayed the census sampler (`random.seed(757)`, 20 per n). The pools are 29, 508, 764, 55,712, 13,749 and 724, and the draws contain 0, 0, 1, 0, 9 and 0 saturated sets for n = 6..11. So "20/20 per n over the realized sets (mostly non-saturated ones)" is accurate. `n11_m9_judge_spotcheck50.txt` has 50 PASS lines. Round 2's 26/26 includes saturated sets at every n, so the sentence about the referees' spot checks is accurate.
- **Step 3 filter sentence** ("n ≤ 10 every saturated pattern decided exactly; n = 11 pre-filters, then exact"). It matches `counts.py` (realize_fast for m = n−2, fallback 0) and the n = 11 pipeline summary.
- **Step 2 provenance** ("prefix-split driver with P=1 only for (11,9)"). It matches `run_all.sh`.
- **Record sets.**
  - The n = 10 record's normal form (0,47,62,74,78,87,94,101,124,174) is in my list.
  - The n = 8 record has m = 5 and is non-saturated (C7).
  - The n = 11 record has m = 8 (C7).
- **n = 12.** L002's latest review starts `VERDICT: ACCEPT`. Its Statement gives exactly 54,243 affine classes, each with m = 10 and rigid, which is what the bullet cites.
- **Round-2 requests.** All three are implemented, and the Statement uses round 2's replacement text:
  - P1: "up to affine equivalence";
  - P2: driver attribution;
  - P3: filter and judge wording.

### C12. The claim's own test

`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_small_counts.py` reports 4 passed (109 s). Afterwards `git status` shows only my scratch directory.

### C13. Reproducibility of my own runs

`sat3.c` gained a debug print mode after the main runs. With the final source, the outputs of n = 6..9 (brute force), n = 10 (K30 + linearity) and n = 11 (K30 + linearity) are byte-identical to the earlier ones. md5 of the sources: sat3.c 8037c141…, patc3.c 006dde29…, nonsat3.py 02f58287….

## Problems found (in order of severity)

None blocks acceptance. The following are editorial. None changes the truth of a sentence in the Statement, and none requires a computation.

- **E1. Title.** "Exact counts of extremal (4,5)-sets for n = 6..11" omits "saturated". For these n the number of affine classes of extremal sets is infinite, as the Statement itself says.
  - Suggested title: "Exact counts of saturated extremal (4,5)-sets for n = 6..11 (all other extremal classes: infinitely many)".
  - When recording this result in the LEDGER or FINAL_REPORT, copy the Statement's wording, not the title.
- **E2. Missing tags.** In DEPENDS ON, K24/K29 still lack their tags ([derived-here], [verified-here]). This is not load-bearing: f(6..11) follows from the published bound and the sets enumerated here (C10.8).
- **E3. Loose phrase in Step 4.** "A generic point of it is again a (4,5)-set with the same pattern" holds for generic points of the realization region, near the given realization, inside the order cone. It does not hold for the whole normalised solution space, where the rank order, and hence the ordered pattern, can change.
  - The conclusion is unaffected, and the Statement's own argument ("its realizations form a family of positive dimension modulo x -> qx+t") is correct.
  - Suggested wording: "a generic point of it near the given realization".
- **E4. Outside the claim, optional.** K43 in `kb/known_results.md` says the smallest m is "one more than the Henning–Yeo minimum for 7 ≤ n ≤ 12". At n = 7 this holds only with the README's clamped m_HY = 1, as rounds 1 and 2 noted.

**Not redone by me.** The Statement does not depend on any of these:
- the exact non-saturated realizable counts for n ≤ 10 and the n = 11 "first 300" samples (round 1, C6, reproduced them);
- a lemma-free brute force at n = 10 (round 2);
- a K30-only run at n = 11 (rounds 1 and 2).

My n = 10 runs depend on one proved rule each (K30-only and linearity-only agree), and my n = 11 run depends on linearity only.

## Reproduction (from `experiments/referee/L003-round3/`)

```
gcc -O2 -o sat3 sat3.c -lm; gcc -O2 -o patc3 patc3.c
for nt in "6 4" "7 5" "8 5" "9 6"; do set -- $nt; ./sat3 $1 $2 0 0 | tail -1; done          # C1 brute force
for n in 6 7 8; do ./sat3 $n 5 0 0 -1 1 | tail -1; done   # C1 forced exact path (use T=4 for n=6)
./sat3 10 6 1 1; ./sat3 10 6 0 1; ./sat3 10 6 1 0                                              # C2
nice -n 10 ./sat3 11 7 1 1 | gzip > sat_n11_k1_l1.txt.gz                                       # C3, 25 s
nice -n 10 ./sat3 11 7 0 1 | gzip > sat_n11_k0_l1.txt.gz                                       # C3, 317 s
python3 -I compare3.py N <sat output files>                                                    # C4
python3 -I defcheck.py N T <file> [sample seed]                                                # C5.1
./sat3 10 6 1 1 -1 0 1 | gzip > dbg_n10.txt.gz; python3 -I dbgcheck.py 10 dbg_n10.txt.gz       # C5.2
./sat3 11 7 1 1 -1 0 1 | python3 -I dbgcheck2.py 11 7 20                                       # C5.3, 227 s
for nt in "6 4" "7 5" "8 5" "9 6" "10 6" "11 7"; do ./patc3 $nt; done                          # C6
python3 -I nonsat3.py; python3 -I small_n3.py                                                  # C7, C8
(repo root) python3 judge/judge.py experiments/referee/L003-round3/spot/*.json                 # C9
(repo root) PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_small_counts.py   # C12
```
