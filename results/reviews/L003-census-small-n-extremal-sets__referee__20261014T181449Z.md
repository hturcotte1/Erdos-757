VERDICT: NEEDS-WORK

# Referee report, round 1: L003-census-small-n-extremal-sets (certificate: exhaustive enumeration with exact realization)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-14, round 1.
- **Claim file reviewed:** `results/proofs/L003-census-small-n-extremal-sets.md` as committed in c7135f0. It is unchanged up to HEAD 59f5c53. Evidence: `experiments/20261014-1430-small-counts/` (README, `results/`, and the gitignored `n11/results/`).
- **Scratch:** `experiments/referee/L003/`. Large outputs are gzipped (`*.gz`, gitignored). The directory totals 44 MB, and no single file exceeds 14 MB.
- **Independence:**
  - My enumerators (`satenum.c`, `patenum.c`, `patcount.c`) and my exact decider (`realdec.py`) import nothing from `e757/`, `judge/` or earlier referee directories. My comparison scripts do not either.
  - Census outputs were read only as data.
  - The census binary was run only to regenerate the n = 11 "first 300" samples (C6), for a reproducibility recount (C11) and through the claim's own test (C11).
  - The judge was run read-only, on claim files in my scratch directory.
- **Load:**
  - One niced heavy process at a time. The longest was the n = 11 K30-only enumeration: a background job via `scripts/start_job.sh`, 17:29–17:54 UTC.
  - Two brief overlaps occurred. A 42 s n = 11 run happened during that job. Separately, a chained follow-up job started early because its wait condition misfired; I killed it after about 30 s and relaunched it with a PID-based wait.

## Summary

The certificate's numbers are all correct. I reproduced every one of them with an independent pipeline.

- **Saturated counts.** The six counts 1, 4, 66, 1,262, 6,644 and 466,961 hold. For every n = 6..11 my list of affine classes is set-equal to the census list.
  - My enumerator uses no α-pruning, no F7 test, no K31 or core filter, and no linearity pruning. Its only pruning is the one-line order fact K30.
  - For n ≤ 9 it is a plain brute force over all ∏ j(n−1−j) midpoint maps.
  - At n = 11 it decides all 2,195,189,896 K30 maps: a provably sound float pre-filter (it can only reject) followed by exact integer arithmetic. A pure-exact run with linearity pruning gives identical output (C3).
- **Pattern-level counts.** Every count in the README table matches my independent count in every cell, including n = 11, m = 5..9.
- **Non-saturated counts.** Every realizable count claimed exact for n ≤ 10 matches my independent exact decider, down to the breakdown of failure reasons. So do the n = 11 sample counts.
- **Non-saturated families.** The infinite non-saturated families for n = 6..11 are correct.

Two problems keep this from ACCEPT.

- **P1: a false sentence in the Statement.** The Statement says "the set of all extremal n-point (4,5)-sets is infinite for n ≤ 11, and n = 12 is the first size at which it is finite".
  - It is false for n = 1, 2, 3, which have exactly one affine class each: {0}, {0,1} and {0,1,2}.
  - For n = 4 and 5 the claim offers no evidence, although the sentence is true there.
  - Proof Step 4 ("for each n ≤ 11") and K43 repeat the error.
- **P2: inaccurate step text with an undeclared dependency.**
  - Step 3 says every saturated pattern was decided exactly. At n = 11, however, 3,263,957 of the 4,935,851 canonical patterns were discarded by the K31 and ≤4-edge-core filters without being realized.
  - The justification for those filters (K31–K33) is missing from DEPENDS ON.
  - The count survives only because an unfiltered recount, mine, gives the same 466,961 classes.

Both problems are fixed by rewording, and no number changes.

## Steps and status

| # | Step | Status |
|---|---|---|
| S1 | Saturated classes 1, 4, 66, 1,262, 6,644, 466,961 for n = 6..11 | **Verified** (C1–C4) |
| S2 | Realizable non-saturated extremal patterns exist for every n = 6..11, each giving infinitely many classes | **Verified** (C6, C7) |
| S3 | "infinite for n ≤ 11, and n = 12 is the first size at which it is finite" | **False for n ≤ 3; unsupported for n = 4, 5** (C8, P1) |
| 1 | Reduction to class-O patterns with α ≤ f(n), 1 ≤ m ≤ n−2 | **Verified** (C12) |
| 2 | DFS enumeration of class O by (n, m) | **Verified** in every reported cell (C5, C11). Wording issues: P3 |
| 3 | Exact realization; rigidity; patterns ↔ affine classes; judge | **Numbers verified** (C1–C4, C10). Text inaccurate at n = 11: P2 |
| 4 | Non-saturated: existence, exact counts for n ≤ 10, n = 11 samples, genericity argument | **Verified** (C6, C7). "For each n ≤ 11" is false for n ≤ 3 (P1). Wording: P4 |

## Checks performed

All commands are run from `experiments/referee/L003/` unless stated otherwise. Logs are in that directory.

### C1. Saturated sets by brute force over ALL midpoint maps (n = 6..9)

**What `satenum.c` does.**
- A saturated (4,5)-set gives every interior rank j exactly one AP (l(j), j, r(j)). This uses weak Sidon and the fact that midpoints are never extreme (C12).
- The set is therefore the unique solution of 2x_j = x_{l(j)} + x_{r(j)}, with x_0 = 0 and x_{n−1} = 1.
- The search assigns j = n−2 down to 1, the reverse of the census order.
- At each leaf it does the following:
  - an exact `__int128` Bareiss solve, with an exact residual check;
  - a strict-order test;
  - a (4,5) test on all 4-subsets, from the definition;
  - a recount of the 3-APs from the set itself, compared with the map;
  - h computed as the largest Sidon subset, by DFS on differences;
  - an affine normal form: min 0, gcd 1, and the smaller of the set and its reflection.
- `brute=1` disables all pruning.

**Command:** `./satenum n 99 0 1 0` (log: `satenum_stats.log`).

| n | maps | singular | saturated (4,5)-sets | h histogram | classes |
|---|---|---|---|---|---|
| 6 | 576 = (4!)² | 0 | 2 | 4:2 | **1** |
| 7 | 14,400 | 0 | 8 | 5:8 | **4** |
| 8 | 518,400 | 0 | 132 | 5:132 | **66** |
| 9 | 25,401,600 = (7!)² (44.9 s) | 0 | 2,524 | 6:2,524 | **1,262** |

Every saturated (4,5)-set with n ≤ 9 has h = f(n). In every run, apmismatch = 0.

### C2. Saturated sets with K30-only pruning (n = 6..11)

**Float pre-filter.** `float=2` adds a pre-filter that can only reject.
- **Soundness.** The system matrix 2I − B is a weakly chained diagonally dominant Z-matrix, hence a nonsingular M-matrix. So 0 < det ≤ 2^{n−2}.
  - Every exact gap and every difference of distances is an integer multiple of 1/det.
  - A double-precision value below 1e−6 therefore certifies an exact value ≤ 0.
  - The bound is asserted at run time and was never violated.
- **Evidence for the det range.** On all maps for n ≤ 7, and on 200,000 maps at n = 8, det lies in [n−1, 2^{n−2}] (`rigidity_check.log`).
- **Validation.** At n = 10, the pure-exact run and both float modes give identical STATS and identical SET lines.

**n = 6..10.** Leaves: 180, 2,684, 55,438, 1,506,374 and 51,841,968. The ok45 counts are identical to C1 for n ≤ 9.
- n = 10: 51,412 saturated (4,5)-sets, with h histogram 6: 13,288, 7: 38,106, 8: 18. That gives **6,644 classes**.

**n = 11.** Background job (`job_n11_k30/run.log`, output `job_n11_k30/sat_n11_k30.txt.gz`):

`STATS n=11 T=7 lin=0 brute=0 leaves=2195189896 singular=0 orderfail=1713955435 not45=480027565 ok45=1206896 apmismatch=0 out=933922 maxdet=510 hhist 7:933922 8:272960 9:14`

That gives **466,961 classes** (`compare_n11_k30only.log`).

### C3. n = 11 with linearity pruning, pure exact path (no float)

`./satenum 11 7 1 0 0` (`job2/run.log`):
- 13,860,888 leaves, ok45 = 1,206,896, out = 933,922, with the same h histogram as C2.
- The SET lines are identical, in the same order, to the float run `sat_n11_k30lin.txt.gz`.
- They are also identical, as a multiset, to the K30-only output.

So linearity pruning loses nothing, and the n = 11 count depends on neither the float pre-filter nor linearity.

### C4. Set-level comparison with the census

`compare_census.py` reads the census sets as data:
- n ≤ 10: `results/n{n}_m{n−2}_real.json.gz`;
- n = 11: all 418 `n11/results/post/real_*.json.gz` batches, which hold 466,961 records.

Results (`compare_n6_10.log`, `compare_n11_k30only.log`):
- For n = 6, 7, 8, 9, 10 and 11, **mine − census = census − mine = 0**. My class counts are 1, 4, 66, 1,262, 6,644 and 466,961.
- The number of labelled sets is exactly twice the number of classes in every case. So no saturated extremal set with n ≤ 11 is reflection-symmetric, which is consistent with "realizable = classes".

### C5. Pattern counts per (n, m) against the README table

**Method (`patcount.c`).**
- The search covers partial maps, assigned for j descending, with K30 and linearity only.
- At each leaf: exact α by enumerating all subsets, my own F7 test, and a reflection-symmetry count.

**Results.** Cells are F7-free labelled / symmetric / up to reflection, with F7-containing counts in brackets. Logs: `patcount_small.log`, `patcount_more.log`, `job2/run.log`.

| n | m = 1..4 cells | higher cells |
|---|---|---|
| 6 | m2 9/3/6 · m3 46/0/23 · m4 2/0/1 | — |
| 7 | m1 0 · m2 63/3/33 · m3 631/9/320 · m4 348/2/175 | m5 10/0/5 [+10 F7] |
| 8 | m3 0 · m4 0 | m5 1,832/0/916 [+80] · m6 260/0/130 [+110] |
| 9 | m1 0 · m2 0 · m3 208/12/110 · m4 5,256/0/2,628 | m5 74,212/90/37,151 [+360] · m6 69,535/7/34,771 [+2,090] · m7 8,570/22/4,296 [+1,656] |
| 10 | — | m5 0 · m6 0 [+840 F7] · m7 36,210/0/18,105 [+2,370] · m8 79,488/42/39,765 [+11,946] |
| 11 | — | m5 0 · m6 208,880/0/104,440 [+9,240] · m7 8,891,530/238/4,445,884 [+102,812] · m8 26,228,370/146/13,114,258 [+726,024] · m9 9,871,248/454/4,935,851 [+819,030] |

**Every F7-free entry equals the census value** (README table, `results/n*_m*.json`, `results/dfs_n*_m*.json`).
- This includes the zero cells at m_HY, which back the README's "smallest m = m_HY + 1".
- The census DFS (α look-ahead, F7 pruning, prefix split at (11,9)) is therefore complete in every reported cell.

### C6. Non-saturated realizability: my own exact decision procedure (`realdec.py`)

**The criterion.** P is realizable iff all three of the following hold:
- C = V ∩ {strictly increasing} is nonempty, where V is the solution space of the AP equations;
- no extra-AP form vanishes identically on V;
- every 4-subset keeps at least 5 distinct distance forms modulo the annihilator of V.

All failure sets are finite unions of proper subspaces of V (C12).

**Certificates.**
- C ≠ ∅: an exact rational point, found by float LP and then checked exactly.
- C = ∅: an exact Gordan vector y ≥ 0, y ≠ 0, with Σ y_i (x_{i+1} − x_i) ≡ 0 on V.
- Forced coincidences are checked exactly.
- Every "realizable" verdict is also backed by an explicit integer witness set. Each witness is checked from the definitions ((4,5), AP set equal to P), and its h is computed by brute-force Sidon search.

F7 patterns are included and decided too.

**Results.** Cells are F7-free patterns up to reflection → realizable (failure reasons). Logs: `realdec_n6_8_and_10_6.log`, `realdec_n9_small.log`, `job2/run.log`.

| (n,m) | result |
|---|---|
| (6,2) | 6 → 6 |
| (6,3) | 23 → 22 (1 repeated difference) |
| (6,4) | 1 → 1 |
| (7,2) | 33 → 33 |
| (7,3) | 320 → 313 (7 repeated difference) |
| (7,4) | 175 → 158 (8 extra AP, 5 repeated difference, 4 order) |
| (7,5) | 5 → 4 (1 extra AP) |
| (8,5) | 916 → 698 (34 extra AP, 158 order, 26 repeated difference) |
| (8,6) | 130 → 66 (15 extra AP, 46 order, 3 repeated difference) |
| (9,3) | 110 → 110 |
| (9,4) | 2,628 → 2,536 (65 repeated difference, 27 order) |
| (9,5) | 37,151 → 30,866 (718 extra AP, 1,512 repeated difference, 4,055 order) |
| (9,6) | 34,771 → 20,938 (2,341 extra AP, 1,990 repeated difference, 9,502 order) |
| (10,7) | 18,105 → 7,105 (768 extra AP, 1,141 repeated difference, 9,091 order) |

- **Every realizable count and every reason breakdown equals the census JSON.**
- Every witness has h = f(n). There are 0 undecided patterns and 0 missing witnesses.
- No F7-containing pattern is realizable in any cell. That covers 6, 40, 55, 184, 1,045, 1,185 patterns, plus all 420 patterns at (10,6). So K7 is not needed for these counts.

**n = 11 "first 300" samples (`sample11.log`).** The patterns were regenerated with the census binary (`limit=300`), used only as a data source.
- m = 6: 251/300 (17 extra AP, 32 order).
- m = 7: 257/300 (29 repeated difference, 14 order).
- m = 8: 216/300 (42 repeated difference, 11 extra AP, 31 order).

All three equal `results/n11_m*_sample.json`.

### C7. Non-saturated existence and explicit infinite families (`nonsat_family.log`)

For each n = 6..11, I took 3 random non-saturated census sets and re-verified each from the definitions:
- the (4,5) property on all 4-subsets;
- AP set equal to the stored edges;
- m < n − 2;
- h = f(n), by subset brute force.

For each set:
- dim V = n − m ≥ 3, which exceeds the dimension 2 of an affine orbit.
- Five perturbations x + εv, with v ∈ V \ span(x, **1**), are each (4,5)-sets with the same AP set and h = f(n).
- The five perturbations lie in five pairwise distinct affine classes.

Also, f(n) = ⌈(9n+6)/17⌉ = 4, 5, 5, 6, 6, 7, which is the Ma–Tang lower bound [published], and every value is attained.

### C8. n ≤ 5 (`small_n_classes.log`, `small_n_families.log`)

- **n = 1, 2, 3: exactly one affine class each.**
  - Proof for n = 3: a 3-set {a < b < c} has h = 2 iff b − a = c − b, so every extremal set is affinely {0,1,2}.
  - A box search over [0,30] agrees.
- **n = 4 (f = 3):** the sets {0,1,2,x} for x = 5..40 are 36 pairwise inequivalent extremal sets.
- **n = 5 (f = 4):** the sets {0,1,2,x,3x} for x = 5..40 are 36 pairwise inequivalent extremal sets.

So the S3 sentence holds exactly for 4 ≤ n ≤ 11.

### C9. Record sets

- **n = 8 record:** m = 5, a (4,5)-set with h = 5, not saturated. Its pattern is among my 698 realizable (8,5) patterns.
- **n = 10 record:** m = 8, h = 6. It is among my 6,644 classes.
- **n = 11 record:** m = 8, h = 7, not saturated. This matches the census summary, where `pattern_in_realizable` is false for the saturated census.

### C10. Judge

- `python3 judge/judge.py experiments/referee/L003/spot/*.json` was run on 6 random n = 11 saturated sets from my enumeration and 6 non-saturated witnesses (n = 6, 7, 8) from my decider. Result: **12/12 `PASS NO-IMPROVEMENT`** with h = f(n) (`spot_judge.txt`).
- Census judge files:
  - `results/judge_spot_n{6..11}.txt` are 20/20 PASS each. The pool sizes 29, 508, 764, 55,712, 13,749 and 724 equal the sums of the realizable counts.
  - `n11_m9_judge_spotcheck50.txt` is 50/50.

### C11. Census code re-run

- `python3 -m pytest -q tests/test_small_counts.py` reports 4 tests passed in 117 s. The repo's `addopts = -q` makes this `-qq`, so only the dots are printed. Log: `pytest_small_counts.log`.
- `e757/c/ordered_dfs n=11 T=7 m_min=9 m_exact=9 f7=1 mode=count` gives `DONE nodes=22336935 leaves=9871248 solutions=9871248`. This is identical to `dfs_n11_m9.json` and `n11_m9_TOTAL.json` (`census_rerun_n11_m9.log`).

### C12. Code reading and mathematics

**Code read:**
- `e757/c/ordered_dfs.c`: branching; the K30 staircase M[i]; linearity through `nb`; the NONE budget with m_exact; the refined α look-ahead, which is sound because feasibility only shrinks; exact α at the leaves; `has_f7`.
- `counts.py`: `enum` asserts timed_out = 0 and the solution count; `canon` and `normalize`; `realize_all` uses `fastreal` for m = n−2 and `realize_exact` otherwise.
- `dfscount.py`: the symmetry arithmetic.
- `ordered_dfs_split.py` and `postprocess.py`: the n = 11 filter and realization stages.
- `fastreal.py`: exact Gauss–Jordan, strict order, AP-set equality, (4,5).

I found no defect affecting a reported number.

**Mathematics re-derived:**
- **K3.** Suppose x + y = z + w with x < z < w < y. Then z − x = y − w and w − x = y − z, so these four points determine at most 4 distances.
- **Injective midpoints.** Two APs with midpoint j give x_i + x_k = x_i' + x_k' = 2x_j on disjoint pairs, which contradicts weak Sidon. Midpoints are never extreme. Hence m = n − 2 exactly when every interior rank is the midpoint of exactly one AP.
- **K6.** Two APs that share a pair are two distinct distance coincidences inside 4 points.
- **K30:** a one-line argument.
- **Rigidity:** the WCDD M-matrix argument above.
- **Class bijection:** as in L002.
- **Infinite families.** C is open in V. The failure sets are finite unions of proper subspaces; for (4,5), each is an intersection of two coincidence hyperplanes. A coincidence that holds generically holds at the realized point, so the generic points of C near the realization are extremal sets with the same pattern. Moreover rank = m ≤ n − 3, so dim V ≥ 3 > 2, and there are infinitely many affine orbits. **Correct.**

## Problems found (in order of severity)

### P1. False sentence in the Statement (must fix)

"Hence the set of all extremal n-point (4,5)-sets is infinite for n ≤ 11, and n = 12 is the first size at which it is finite" is wrong under either reading.
- **Up to affine equivalence** (the intended reading), n = 1, 2, 3 have exactly one extremal class each (C8).
- **As raw sets**, every n gives an infinite family, n = 12 included.

The evidence also covers only n = 6..11, so n = 4, 5 are unsupported in the claim (they are true, see C8). Proof Step 4, "For each n <= 11 at least one non-saturated pattern is realizable", is false for n ≤ 3: for n = 3 the only extremal set {0,1,2} is saturated. The same sentence is in K43 (`kb/known_results.md`).

Suggested text: "…is infinite up to affine equivalence for 4 ≤ n ≤ 11 (n = 6..11 by the census; n = 4, 5 by the families {0,1,2,x} and {0,1,2,x,3x}, x ≥ 5); for n ≤ 3 there is exactly one class; n = 12 is the smallest n ≥ 4 at which it is finite."

### P2. Step 3 is inaccurate at n = 11 and has an undeclared dependency (must fix the text; the number is unaffected)

Step 3 says "Every saturated pattern is decided exactly (fastreal.py / realize_exact)". At n = 11, only the 1,671,894 survivors of the filters were realized.
- 1,666,080 canonical patterns were removed by K31.
- A further 1,597,877 were removed by the forbidden cores with at most 4 edges.
- That is 3,263,957 in total (`n11_m9_postprocess_summary.json`).

These filters rest on K31–K33 [verified-here], which are not in DEPENDS ON. The claim's own evidence for 466,961 therefore depends on them.

In L002 this dependency was harmless because a referee realized all patterns. Here the same role is now played by C2–C4: an unfiltered recount with identical classes.

Fix: add K31–K33 to DEPENDS ON and reword Step 3, or cite this review's filter-free recount as the completeness evidence for n = 11.

### P3. Minor wording in Step 2 and DEPENDS ON

- **"For each n and each m".** The m below the Henning–Yeo minimum were not enumerated at n = 10 (m ≤ 5) or at n = 11 (m ≤ 4). Those cells rest on K8 [published], which DEPENDS ON lists only implicitly through K24. They matter for the f(n) values and the "smallest m" remarks, not for the Statement.
- **"prefix-split driver with P=1".** This applies only to (11, 9). For n ≤ 10 the claim used the unsplit engine via `counts.py`.

### P4. Minor wording in the genericity argument of Step 4

- "The failing points lie on finitely many hyperplanes" should read "on finitely many proper linear subspaces of the solution space". A (4,5) failure is an intersection of two coincidence hyperplanes.
- State the reason the quotient is positive-dimensional: rank = m ≤ n − 3, so dim V ≥ 3 > 2.

The argument itself is correct (C12).

### P5. Outside the claim (optional)

- K43 copies P1.
- K43's "smallest m … is one more than the Henning–Yeo minimum for 7 ≤ n ≤ 12" holds at n = 7 only with the README's clamped m_HY = 1.
  - Unclamped, Henning–Yeo gives m ≥ 0.
  - The trivial bound m ≥ τ = 2 is what is attained.
  - The README states this caveat; K43 does not.

## Reproduction (from `experiments/referee/L003/`)

```
gcc -O2 -o satenum satenum.c; gcc -O2 -o patenum patenum.c; gcc -O2 -o patcount patcount.c
for n in 6 7 8 9; do ./satenum $n 99 0 1 0 | tail -1; done              # C1 brute force over all maps
for n in 6 7 8 9; do ./satenum $n 99 0 0 2 > sat_n${n}_k30.txt; done; ./satenum 10 6 0 0 2 > sat_n10_k30_float2.txt   # C2
nice -n 10 ./satenum 11 7 0 0 2 | gzip > job_n11_k30/sat_n11_k30.txt.gz  # C2, n=11 K30-only (~25 min)
nice -n 10 ./satenum 11 7 1 0 0 | gzip > job2/sat_n11_k30lin_exact.txt.gz # C3 pure exact
python3 compare_census.py N <my output> <census real files>               # C4
./patcount N T M                                                          # C5
./patenum N T M | python3 realdec.py N T h                                # C6
bash sample11.sh                                                          # C6, n=11 samples
python3 nonsat_family.py; python3 small_n_classes.py; python3 rigidity_check.py   # C7, C8, C12
(repo root) python3 judge/judge.py experiments/referee/L003/spot/*.json   # C10
(repo root) python3 -m pytest -q tests/test_small_counts.py               # C11
```
