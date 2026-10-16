VERDICT: NEEDS-WORK

# Referee report, round 2: L003-census-small-n-extremal-sets (certificate: exhaustive enumeration with exact realization)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-14, round 2. I formed my own verdict and did not rely on round 1's code.
- **Claim reviewed:** `results/proofs/L003-census-small-n-extremal-sets.md` at HEAD 8ecc7c7, the revision after round 1. Evidence: `experiments/20261014-1430-small-counts/`, including the gitignored `n11/results/`.
- **Scratch:** `experiments/referee/L003-round2/`, 19 MB on disk. The largest file is 25.5 MB uncompressed, and the n = 11 outputs are gzipped (gitignored).
- **Independence:**
  - My programs (`satcheck.c`, `patcount2.c`, `compare.py`, `nonsat.py`, `small_n.py`, `spot.py`) import nothing from `e757/`, `judge/` or `experiments/referee/L003/`.
  - Census and round-1 outputs were read only as data.
  - The census binary was re-run only in count mode, writing to stdout (R4). The claim's own test was run with bytecode and cache writing disabled (R10).
  - The judge was run read-only, on claim files in my scratch directory.
- **Load:**
  - One `nice -n 10` process at a time.
  - Longest single computation: 533 s (the n = 10 pure brute force).
  - The n = 11 runs were sequential steps of at most 340 s each.
  - One brief overlap: the n = 6, 7, 8 brute force plus the comparison script (a few seconds) ran while the n = 10 brute force was in the background.

## Summary

**The numbers are correct.** Every number in the Statement holds, and I re-verified each one with my own code.

- **Saturated counts.** The counts 1, 4, 66, 1,262, 6,644 and 466,961 are confirmed by a new enumerator of all midpoint maps. It uses an exact integer certificate at each leaf, and it computes h from the definition of a Sidon set.
  - For n ≤ 10 it ran with no pruning at all: all ∏ j(n−1−j) maps, which is 1,625,702,400 at n = 10.
  - At n = 11 it ran in three pruning modes: K30 only, linearity only (no K30) and both. All three outputs are identical.
  - For every n = 6..11 my list of classes is set-equal to the census list and to round 1's list.
- **Existence of non-saturated sets.** For each n = 6..11 a realizable non-saturated extremal pattern exists. I proved infinitude exactly for 34 witnesses, including my own census-free gluing constructions for n = 6, 7, 9, 11. Each witness's realizations contain a line of pairwise inequivalent extremal sets, with only finitely many exceptional parameter values.
- **Small and boundary cases.**
  - The n = 4, 5 families work for every real x > 4.
  - n = 1, 2, 3 have exactly one class each.
  - The n = 12 finiteness follows from L002.
- **Census engine.** The census DFS counts for the saturated cells are reproduced both by my own pattern counter and by a re-run of the census engine.

**What remains.** The claim stays at NEEDS-WORK for wording only.

- **The Statement's last clause is still literally false.** "The set of all extremal n-point (4,5)-sets … n = 12 is the smallest n ≥ 4 at which it is finite".
  - The set of extremal 12-point sets is infinite, since it is closed under x ↦ qx + t. What is finite is the number of affine classes (54,243).
  - Round 1 flagged exactly this and proposed adding "up to affine equivalence". The revision adopted the n-range but not that phrase.
- **Two smaller inaccuracies from round 1 remain.**
  - Step 2 attributes "prefix-split driver with P=1" to every n.
  - Step 3's description of the pre-filters and of the judge spot check does not match what was run.

No computation needs to be redone. With the text fixes below I would expect to accept.

## Steps and status

| # | Step | Status |
|---|---|---|
| S1 | Saturated affine classes with h = f(n): 1, 4, 66, 1,262, 6,644, 466,961 (n = 6..11) | **Verified** (R2, R3) |
| S2 | For each n = 6..11, a realizable non-saturated extremal pattern exists and gives infinitely many affine classes | **Verified** (R5) |
| S3 | Infinite for 4 ≤ n ≤ 11 (n = 4, 5 families); one class for n ≤ 3; n = 12 is the first finite case | **True up to affine equivalence** (R5–R7). **As worded, false** (P1) |
| 1 | Reduction to class O, α ≤ f(n), 1 ≤ m ≤ n−2 | **Verified** (R1) |
| 2 | DFS enumeration by (n, m) | Saturated cells **verified** (R4). Non-saturated cells: not redone by me; round 1 (C5) matched every cell, and the Statement does not use them. Provenance wording: P2 |
| 3 | Exact realization, rigidity, bijection with affine classes, judge | **Verified** (R1–R3, R8). Wording: P3 |
| 4 | Non-saturated existence; genericity argument; record sets | **Verified** (R5, R9). The "exact counts for n ≤ 10" were not redone by me (round 1, C6); the Statement does not use them |

## Checks performed

All commands are run from `experiments/referee/L003-round2/` unless stated otherwise.

### R1. Mathematics re-derived by hand

1. **(4,5) ⟹ weak Sidon.** Suppose x_a + x_d = x_b + x_c for distinct points with a < b < c < d. Then x_b − x_a = x_d − x_c and x_c − x_a = x_d − x_b, which are two coincidences inside 4 points.
2. **Coincidences in a weak Sidon set.** Every equality of two distances x_b − x_a = x_d − x_c (with {a,b} ≠ {c,d}) is an AP coincidence. Disjoint pairs give a sum relation, which weak Sidon forbids. Pairs sharing an index force an AP or a repeated point.
   - Hence the midpoint map is injective, min and max are never midpoints, and m ≤ n − 2.
   - Saturated means every interior rank j is the midpoint of exactly one AP (L(j), j, R(j)).
3. **(4,5) ⟹ linear.** Two APs that share two points span 4 points and give two distinct coincidences there, so those 4 points determine at most 4 distances.
4. **K30 and K31.**
   - K30: x_j = (x_i + x_k)/2 < (x_{i'} + x_{k'})/2 = x_{j'}.
   - K31: x_a + x_q = x_b + x_p. I checked that a, b, p, q are distinct, including q ≠ a: q = a would give a second AP with midpoint a. So this contradicts weak Sidon.
   - Both are sound pruning rules.
5. **Rigidity.** Write the system as (2I − B)x = b. It is weakly chained diagonally dominant: follow R(j) upwards until it reaches n − 1. So it is nonsingular, the map determines the set, and singular = 0 was observed everywhere.
   - For m < n − 2 no rank argument is needed: rank ≤ m ≤ n − 3, so dim V ≥ 3 > 2 = the dimension of an affine orbit.
6. **Normal form.** The normal form is: translate the min to 0, scale to a primitive integer vector, then take the lexicographic minimum of the set and its reflection. It is a complete invariant for x ↦ qx + t with q ≠ 0.
   - Saturated sets are rigid, and a set determines its own pattern. So "realizable patterns up to reflection" equals "affine classes".
7. **h = α.** For weak Sidon sets, a failure of the Sidon property must be 2y = x + z, so h = α(AP hypergraph) (K4).
8. **Values of f.**
   - f(n) ≥ ⌈(9n+6)/17⌉ = 4, 5, 5, 6, 6, 7 for n = 6..11 [published]. Each value is attained (R2), so f(6..11) are exact.
   - f(4) = 3 and f(5) = 4: two APs on at most 5 points must meet (linearity), and a linear triangle needs 6 points, so τ ≤ 1.

### R2. Saturated sets with my own enumerator: `satcheck.c`

**Method.**
- **Search.** Midpoint maps are assigned in ascending j, which is the reverse of round 1's order.
- **Leaf solve.**
  - A float LU solve, followed by an exact integer certificate: X_0 = 0, X_{n−1} = D, and 2X_j = X_{L(j)} + X_{R(j)} for all j.
  - If the certificate fails, the map is printed as FALLBACK for exact treatment.
- **Checks on each solution:**
  - strict order;
  - weak Sidon, using a sums bitmap;
  - (4,5) on every 4-subset, from the definition;
  - the 3-AP set recomputed from the set and compared with the map;
  - h computed by exhaustive branch and bound on the definition of a Sidon set (all positive differences distinct), not via APs;
  - the canonical form.
- **Output.** Each class is printed once, from its lexicographically canonical orientation.

**Commands:** `./satcheck n k30 lin [r1]`. Logs: `run_n9.log`, `run_n10.log`, `run_n10_brute.log`, `run_n11.log`.

| n | maps (no pruning) | leaves K30 only | leaves lin only | leaves K30+lin | saturated (4,5)-sets | h histogram | classes with h = f |
|---|---|---|---|---|---|---|---|
| 6 | 576 | 180 | 8 | 2 | 2 | 4:2 | **1** |
| 7 | 14,400 | 2,684 | 120 | 20 | 8 | 5:8 | **4** |
| 8 | 518,400 | 55,438 | 3,280 | 396 | 132 | 5:132 | **66** |
| 9 | 25,401,600 (7.7 s) | 1,506,374 | 138,208 | 10,264 | 2,524 | 6:2,524 | **1,262** |
| 10 | 1,625,702,400 (533 s) | 51,841,968 | 7,887,520 | 338,595 | 51,412 | 6:13,288 7:38,106 8:18 | **6,644** |
| 11 | not run | 2,195,189,896 (9 chunks by R(1), 29–189 s each) | 582,628,416 (340 s) | 13,860,888 (26 s) | 1,206,896 | 7:933,922 8:272,960 9:14 | **466,961** |

- In every run: singular = 0, fallback = 0, apbad = 0, and no reflection-symmetric set.
- **n = 4 and 5:** there are no saturated (4,5)-sets, as linearity requires.
- **Agreement across modes.** For each n, the sorted class lists of all modes are identical:
  - n = 10: md5 a4f5fcaf… in all 4 modes;
  - n = 11: 856102b3… in all 3 modes (`compare_n11_modes.log`).
- **Agreement with round 1.**
  - My K30-only leaf counts equal round 1's in every row, including 2,195,189,896, which is the sum of my 9 chunks.
  - My n = 11 K30+lin leaf count equals round 1's lin run.
- **What this establishes.**
  - n ≤ 10 rests on no lemma beyond R1 items 2 and 5.
  - n = 11 is confirmed separately without K30 and without linearity.

### R3. Set-level comparison with the census and with round 1 (`compare.py`)

**Method.**
- My own normal form is applied to the census realized sets:
  - n ≤ 10: `results/n{n}_m{n-2}_real.json.gz`;
  - n = 11: all 418 `n11/results/post/real_*.json.gz` batches, which hold 466,961 records.
- The same is done for round 1's `sat_n*_k30.txt` and `job_n11_k30/sat_n11_k30.txt.gz`.

**Results** (`compare_n6_10.log`, `compare_n11.log`):
- n = 6, 7, 8, 9, 10, 11 give 1, 4, 66, 1,262, 6,644 and 466,961 classes.
- mine − census = census − mine = 0 for every n.
- mine − round 1 = round 1 − mine = 0 for every n.

So nothing was lost by the census's α look-ahead, F7 pruning, K31 or core filters.

### R4. Saturated-cell pattern counts: my counter and a re-run of the census engine

**My counter (`patcount2.c`).**
- It uses K30+linear maps, my own F7 test (a centre of degree ≥ 3 plus two complementary transversals), and α ≤ f(n), tested as "no independent (f+1)-set".
- Results, labelled / reflection-symmetric / up to reflection (`patcount2.log`):

| n | labelled | symmetric | up to reflection |
|---|---|---|---|
| 6 | 2 | 0 | 1 |
| 7 | 10 | 0 | 5 |
| 8 | 260 | 0 | 130 |
| 9 | 8,570 | 22 | 4,296 |
| 10 | 79,488 | 42 | 39,765 |
| 11 | 9,871,248 | 454 | 4,935,851 |

- Every value equals the README and the census JSONs.

**Census engine re-run.** `e757/c/ordered_dfs n=N T=f m_min=N-2 m_exact=N-2 f7=1 mode=count` (`census_dfs_rerun.log`):
- solutions 2, 10, 260, 8,570, 79,488 and 9,871,248;
- node counts 25, 141, 1,474, 27,208, 440,201 and 22,336,935, identical to the census JSONs.

**Code read.**
- The DFS: the K30 staircase M[i] (new edge legal iff k > M[i]) is exactly K30. The α look-ahead is sound, because an independent set avoiding every still-feasible midpoint stays independent. `has_f7` is the same test as mine.
- `filter.c`: an extra-AP core counts as hit only if the forced triple is absent from the pattern.
- `fastreal.py` checks AP-set equality. `counts.py` and `postprocess.py` re-check (4,5) and compute h on every realized set.

### R5. Non-saturated existence and the infinite-family argument, done exactly (`nonsat.py`, `nonsat.log`, 3 s)

**Witnesses.** 34 in total:
- 2 census records (the first and one seeded random) from every non-saturated cell: (6,2), (6,3), (7,2), (7,3), (7,4), (8,5), (9,3..6), (10,7), and the n = 11 samples at m = 6, 7, 8;
- the record sets n = 8 (m = 5) and n = 11 (m = 8);
- my own gluings {0,1,2} ∪ ((7/3)·B + 50), with B = {0,1,2}, {0,1,2,5}, the 6-point saturated class, and the n = 8 record. These give n = 6, 7, 9, 11 with m = 2, 2, 5, 6, independently of the census.

**Per witness x0, all exact:**
1. **Definitions.** (4,5) holds, m < n − 2, and h = f(n), where h is computed by subset search on the definition of a Sidon set.
2. **Solution space.** rank = m and dim V = n − m ≥ 3. A vector v ∈ V is chosen with x0, v, 1 linearly independent.
3. **Family x(s) = x0 + s·v.**
   - The order holds on an explicit open interval I ∋ 0.
   - The distance coincidences of x0 are exactly the AP coincidences of P (checked), and each of them vanishes identically along v.
   - Every other coincidence form is nonzero at 0, so it has at most one root.
4. **Conclusion.** For every s ∈ I outside the finite root set, x(s) has exactly the coincidences of x0. So it is a (4,5)-set with AP set P and h = α(P) = f(n).
   - Since x0, v, 1 are independent, distinct s give distinct orientation-preserving classes, and reflection identifies at most pairs. So there are infinitely many classes.
5. **Spot check.** Twelve rational s per witness were re-checked from the definitions alone, and the 13 normal forms are pairwise distinct.

**Result:** `ALL_OK True`. For example, the n = 10 census witness at (10,7) has I = (−151721206122/25, 627485670258/31) with 2 roots in I.

### R6. n ≤ 5 (`small_n.py`, `small_n.log`)

- **n = 1, 2, 3:** a box search over [0,40] finds exactly 1 extremal class each: (0), (0,1) and (0,1,2). The proof for n = 3: h = 2 iff the set is a 3-AP.
- **{0,1,2,x}:** the only identically-equal distance pair is the AP (0,1,2), and all other coincidence roots are ≤ 4. So for **every real x > 4** this is a (4,5)-set with one AP and h = 3 = f(4).
- **{0,1,2,x,3x}:** the same holds with roots ≤ 4, giving h = 4 = f(5) for every real x > 4.
- **Inequivalence.** Distinct x give inequivalent sets: the gap ratio 1/(x−2) determines x, and reflections cannot match. An exact check of x = 5..64 gives 60 distinct classes in each family.
- **Box minimum:** the minimum h over (4,5)-subsets of [0,24] is 3 for n = 4 and 4 for n = 5.

### R7. n = 12

L002 (ACCEPTED) states that, up to affine equivalence, there are exactly 54,243 extremal 12-point sets, each with m = 10. Here m ≥ 9 follows from K8, and the census and the referees' enumerators found no pattern with m ≤ 9.

So every extremal 12-point set is saturated and rigid, and there are finitely many affine classes. Together with R5 and R6, "n = 12 is the smallest n ≥ 4 with finitely many affine classes" is true.

### R8. Frozen judge

`python3 judge/judge.py experiments/referee/L003-round2/spot/*.json` gives **26/26 `PASS NO-IMPROVEMENT`**, each with h = f(n) (`spot_judge.txt`). The 26 sets are:
- 3 random saturated classes per n from my enumeration (1 at n = 6);
- the 4 gluing witnesses and a perturbed member of each;
- perturbed members of the n = 8 and n = 11 record families.

### R9. Record sets

- **n = 10 record:** its normal form (0,47,62,74,78,87,94,101,124,174) is among my brute-force classes, with h = 6 (`record_check.log`).
- **n = 8 record (m = 5) and n = 11 record (m = 8):** both are non-saturated and pass R5.

### R10. The claim's own test

`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_small_counts.py` reports 4 passed in 115 s (`pytest_small_counts.log`). Afterwards `git status` showed only my scratch directory as changed.

### R11. Text audit against the evidence

- **Numbers that match the evidence:**
  - 4,935,851 − 1,671,894 = 3,263,957;
  - 1,067,660 + 72,327 + 64,946 = 1,204,933 unrealizable, plus 466,961 realizable, gives 1,671,894;
  - the n = 11 samples 251/257/216 (`n11_m*_sample.json`);
  - 2,195,189,896 equals the K30-only leaf count;
  - m_HY = 6 at n = 10 and 5 at n = 11.
- **Round-1 requests now fixed:**
  - the n-range in the Statement and in Step 4;
  - K31–K33 and K8 added to DEPENDS ON;
  - Step 3 now mentions the pre-filters;
  - "hyperplanes" changed to "proper subspaces".
- **Round-1 requests not fixed:**
  - "up to affine equivalence" (P1);
  - the "prefix-split driver with P=1" provenance (P2);
  - the K43 caveats (P5).

## Problems found (in order of severity)

### P1. The Statement's last clause is false as written (must fix; wording only)

The Statement says: "hence the set of all extremal n-point (4,5)-sets is infinite for 6 <= n <= 11 (…) and n = 12 is the smallest n >= 4 at which it is finite".
- The set of all extremal 12-point (4,5)-sets is infinite, since it is closed under x ↦ qx + t.
- What is finite is the number of affine classes (54,243).
- Read literally, "infinite for 6 ≤ n ≤ 11" is true for every n, which makes the clause vacuous.
- Round 1 (P1) flagged exactly this, noting "as raw sets, every n gives an infinite family, n = 12 included", and proposed the phrase "up to affine equivalence". The revision did not adopt it.

The mathematics is right (R5–R7). Suggested replacement for the Statement from "For every n in 6..11 …" onwards:

> For every n in 6..11 there also exist realizable non-saturated extremal patterns (m < n-2). The AP equations of such a pattern have rank <= m <= n-3, so its realizations form a family of positive dimension modulo x -> qx+t, and each such pattern gives infinitely many affine classes. Hence, up to affine equivalence, the extremal n-point (4,5)-sets are:
> - infinitely many for 4 <= n <= 11 (for n = 4, 5: {0,1,2,x} and {0,1,2,x,3x}, any real x > 4);
> - exactly one for n = 1, 2, 3;
> - finitely many (54,243) for n = 12, by L002: every extremal 12-point set has m = 10.
>
> So n = 12 is the smallest n >= 4 with only finitely many affine classes.

This also fixes a minor point. In the current text, "their solution spaces have positive dimension, so each gives infinitely many affine classes" does not follow, because every solution space has dimension ≥ 2. Step 4 correctly says "after normalization".

### P2. Step 2 attributes the wrong engine path (minor; round-1 P3 second bullet, not addressed)

The text says "the C DFS (e757/c/ordered_dfs, prefix-split driver with P=1)". Per `run_all.sh` and the README:
- the engine was called from `counts.py` (unsplit) for all n ≤ 10 and for the n = 11 samples;
- from `dfscount.py` for the n = 11 counts at m = 5..8;
- and through `ordered_dfs_split` (P = 1) plus `postprocess.py` only for (11, 9).

Suggested text: "(e757/c/ordered_dfs, via counts.py for n <= 10 and the n = 11 samples, via dfscount.py for the n = 11 counts at m <= 8, and via the prefix-split driver with P=1 for (11, 9))".

### P3. Step 3 describes the filters and the judge check inaccurately (minor)

1. **Filters.** "Saturated patterns surviving the K31 and <= 4-edge-core pre-filters are decided exactly" reads as if the filters were used for every n.
   - They were used only at n = 11.
   - At n ≤ 10, `counts.py` realized every saturated pattern exactly ("fallback": 0 in the JSONs).
2. **Judge check.** "judge spot check 20/20 for each n (50/50 at n=11, m=9)" sits in the saturated step, but the 20 sets per n are drawn from all realized sets of that n, pooled over m.
   - At n = 9, for example, only 1,262 of the 55,712 pooled sets are saturated.
   - At n = 11 all 20 come from the non-saturated samples.
   - Only the 50/50 is a saturated spot check.

Suggested text: "At n <= 10 every saturated pattern is decided exactly; at n = 11 the 1,671,894 patterns surviving the K31 and <= 4-edge-core pre-filters are decided exactly, the 3,263,957 discarded ones are unrealizable by K31-K33, and two unfiltered referee recounts (rounds 1 and 2) give the same 466,961 classes … Frozen judge: 50/50 random saturated sets at n = 11; additionally 20/20 per n drawn from all realized sets of that n (all m)."

### P4. Outside the claim (optional)

- **K43 in `kb/known_results.md`** repeats P1 ("the extremal set is infinite for 4≤n≤11 … n=12 is the smallest n≥4 at which it is finite"). It also repeats P3.2 ("judge spot checks 20/20 per n").
- **K43's "smallest m … one more than the Henning–Yeo minimum for 7≤n≤12"** still lacks the README's clamping caveat at n = 7 (round-1 P5).
- **Title.** The title "Exact counts of extremal (4,5)-sets for n = 6..11" would be more accurate as "… of saturated extremal (4,5)-sets …".
- **DEPENDS ON tags.** DEPENDS ON lost the tags on K24/K29 in the revision; they should read [derived-here] and [verified-here].

## Reproduction (from `experiments/referee/L003-round2/`)

```
gcc -O2 -o satcheck satcheck.c -lm; gcc -O2 -o patcount2 patcount2.c
for n in 6 7 8 9; do for k in 0 1; do for l in 0 1; do ./satcheck $n $k $l | tail -1; done; done; done   # R2
nice -n 10 ./satcheck 10 0 0 > sat_n10_k0_l0.txt          # R2, n=10 pure brute force, 533 s
bash run_n11.sh                                            # R2, n=11: K30+lin, lin only, K30 only in 9 chunks (~23 min total)
python3 -I compare.py 10 6 sat_n10_k0_l0.txt --r1 ../L003/sat_n10_k30.txt                         # R3
python3 -I compare.py 11 7 sat_n11_k1_l1.txt.gz --r1 ../L003/job_n11_k30/sat_n11_k30.txt.gz       # R3
for nt in "6 4" "7 5" "8 5" "9 6" "10 6" "11 7"; do ./patcount2 $nt; done                           # R4
python3 -I nonsat.py; python3 -I small_n.py; python3 -I spot.py                                     # R5, R6, R8
(repo root) python3 judge/judge.py experiments/referee/L003-round2/spot/*.json                      # R8
(repo root) PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_small_counts.py   # R10
```
