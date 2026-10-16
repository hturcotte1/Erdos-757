VERDICT: ACCEPT

# Referee report: L004-census-14-point-extremal-sets (certificate: exhaustive enumeration with exact realization)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-15, round 1.
- **Claim file reviewed:** `results/proofs/L004-census-14-point-extremal-sets.md` as committed in ef46fe6, unchanged in the working tree.
- **Scratch:** `experiments/referee/L004/` holds scripts, logs and small data. The SAT outputs went to the session scratchpad and can be regenerated with the commands at the end.
- **Independence:**
  - My verifiers import nothing from `e757/` or `judge/`, and nothing from earlier referee directories: `pchk.c`, `sat14.py`, `realize14.py`, `realize_all14.py`, `verify_sets.py`, `collect14.py`, `leaves_check.py`, `sample14.py`.
  - The census engine was rebuilt from the HEAD source (`census_bin`), and only for the reproducibility checks T3 and C5.
  - The authors' split driver was run only to validate its `--refl` path at n = 12 (C6).
  - The judge was run read-only on claim files in my scratch directory.
- **Load:** at most one heavy process at a time, niced. The long runs went through `scripts/start_job.sh`.

## Summary

The statement is correct as far as I can verify it, and every number in it matches its evidence.

**What I re-verified from scratch:**
- The bookkeeping of all 2,537 prefixes.
- Every one of the 205,529 output patterns: saturated, linear, K30, F7-free, α = 8 exactly, canonical, and distinct.
- Exact realization of all 205,529 patterns with my own integer Bareiss realizer, using no pre-filters. It gives exactly the claimed 2,910 realizable patterns, all rigid, with h = 8, the same 2,910 affine classes, and A_base among them.
- The breakdown on the O′ subset, which reproduces summary.json exactly.

**Why the method is sound:**
- The prefix split is a pure subtree restriction.
- All 7,920 depth-3 cubes are accounted for.
- The reflection reduction is a leaf filter, not a prefix pruning. I validated it at n = 12 against the certified L002 set.

**Completeness, checked independently with my own CNF and CDCL enumeration:**
- I enumerated 719 census prefixes exhaustively: 28.3% of the prefixes and 8.8% of the census nodes. These are all 563 cheap prefixes, prefix 0, and 155 prefixes drawn at random from the rest.
- In each one my patterns equal the census output and my model count equals the census leaf count.
- The mirror images of all 25,156 non-canonical models found are present in the census.
- 21.8% of all orbits are covered exhaustively in this way.

**Whole-census checks:**
- A per-prefix reflection identity holds for all 2,537 prefixes.
- 2,160 random SAT models, spread over 1,348 prefixes, are all in the census.
- 20 prefixes rerun with a fresh build give identical results.
- All 147 extremal saturated sets found in 1.8M candidate sets from other generators are census classes.

**What remains:**
- Editorial inaccuracies in the proof text. None changes a sentence of the Statement.
- One stated limitation: completeness on the 78% of orbits not covered by the exhaustive comparison rests on my reading of the engine and on the whole-census checks, not on a second full enumeration. That would cost about 34 CPU-hours with my encoding.

## Steps and status

| # | Step of the proof | Status |
|---|---|---|
| 1 | Reduction to saturated class-O patterns with α ≤ 8 | **Verified** (M1): re-derived K3–K6 and K30, the F7 definition and the HY scope. |
| 2 | Prefix-split enumeration: 2,537 prefixes, 205,529 orbits, 1.13e11 nodes | **Verified**. Code read (T2); bookkeeping (T1); prefix list complete (T3); exhaustive independent comparison on 719 prefixes (C2); whole-census consistency (C3–C5); `--refl` path validated (C6). Wording issue E1. |
| 3 | Filters and exact realization: 119,844 / 46,419 / 34,995; 2,910 realizable; failure reasons | **Verified with my own realizer on ALL 205,529 patterns** (R1), so the pre-filters are not load-bearing. The K31 count was reproduced independently. Arithmetic wording issue E2. |
| 4 | Classes: 2,910; A_base present; judge | **Verified** (R1, R2, J). |

## Checks performed

### T1. Bookkeeping of the stored census (`check_book.py`, `pchk.c`; log `check_book.log`)

`python3 check_book.py .../n14/results census_keys.txt.gz` reported `PROBLEMS {}`. In detail:

- **Prefix list.** `n14_m12_prefixes.txt` holds 2,537 distinct prefixes.
- **Per-prefix files.** Every index has a `.done` and a `.jsonl.gz` file, and there are no `.part` files. In every `.done`:
  - the prefix field equals the list entry;
  - `timed_out` is 0;
  - `solutions` equals the number of lines of the fully read gzip file.
- **Totals.**
  - Σ solutions = 205,529 and Σ nodes = 113,454,008,923. Both equal the TOTAL file.
  - Σ time = 277,501.1 s.
- **Every output pattern** was checked by my C checker:
  - the triples at midpoints 1–3 equal its prefix;
  - it is saturated (each of the vertices 1..12 is the middle of exactly one triple);
  - it is linear and satisfies K30;
  - it is F7-free;
  - α is exactly 8 (a scan of all 2^14 vertex subsets; histogram `{8: 205529}`);
  - it is canonical, i.e. sorted P ≤ sorted refl P.
- **Distinctness.** The 205,529 canonical keys are pairwise distinct.
- **Symmetry.** 415 patterns are reflection-symmetric.
- **Leaf counts.** Σ leaves over the `.done` files is 410,643 = 2·205,529 − 415. This is the labelled count.

### T2. Reading the engine and driver

**Provenance.**
- `e757/c/ordered_dfs.c` at HEAD is identical to the working tree.
- Its last change is d2f70f5, which already contains `pre=` and `mode=prefixes` (see E4).
- The binary `e757/c/ordered_dfs` is dated 2026-10-14 11:15:19. That is before the launch at 11:21, and it was not rebuilt afterwards.

**`pre=` option.**
- At levels j ≤ plen, only the given triple is tried, and only if it passes the same legality tests as in the unsplit search:
  - all three pairs uncovered;
  - k > max(M[i], j) (K30);
  - the F7 test;
  - `entry_ok`.
- The NONE branch is disabled for edge tokens.
- So the run below a prefix visits exactly the subtree of that node in the unsplit search.

**`mode=prefixes`.**
- It prints every node at level depth+1 that survives `entry_ok`, and does not search below it.
- Hence the union of the prefix subtrees is the unsplit tree.

**Reflection handling.**
- `refl=1` acts only in `report_leaf`, after all pruning: a leaf is output iff sorted P ≤ sorted refl P.
- `list_prefixes` runs with `refl=0`, and `refl` has no effect on prefixes anyway.
- So every prefix is searched completely, and exactly one of {P, refl P} is output.
- The prefixes are not reflection-orbit representatives, and could not be: reflection maps midpoints 1–3 to midpoints 12–10.

**Look-ahead.** I re-derived its soundness.
- Future edges at a midpoint r are among the triples feasible now, and feasibility only shrinks.
- For S independent in the placed edges, S minus {r ∈ S : some feasible triple at r lies in S} stays independent in every completion.
- The branch-and-bound cut `val + |cand| <= best` is valid.
- With m_exact = 12 the budget is 0, so every future midpoint must remain feasible.
- At the leaf (j = 13), α is computed exactly and checked twice.

**Array bounds at n = 14.** pmn ≤ 42 < 512, evn ≤ 12, the edge stack is ≤ 12, and u32 masks suffice.

**Driver.**
- The output goes to a `.part` file, which is renamed only if rc = 0, `timed_out` = 0 and the stream count equals `solutions`. The `.done` file is written after the rename.
- On resume, prefixes with a `.done` file are skipped; all others restart from scratch.
- The authors' `test_prefix_split_small` passes (`pytest -k prefix_split_small`).

### T3. The prefix list is complete

- **Regeneration.** Running `mode=prefixes depth=3` with the installed binary and with my fresh build of `HEAD:e757/c/ordered_dfs.c` gives identical output: `DONE nodes=2743`, 2,537 PRE lines, identical to the frozen list.
- **All depth-3 cubes.** There are 12 × 22 × 30 = 7,920 cubes: a triple with middle 1, one with middle 2, one with middle 3.
  - 2,537 of them are census prefixes.
  - Of the other 5,383, 5,355 already violate linearity or K30 among their own three triples.
  - The remaining 28 were refuted by my SAT model: no F7-free model exists.

### C1. My CNF model (`sat14.py`)

**Encoding.**
- One variable per triple (i, j, k) with i < j < k, meaning that j is the midpoint.
- Exactly one triple per interior vertex 1..n−2.
- Pairwise linearity.
- K30 as binary clauses: forbid (i,j,k) and (a,b,c) together when j < b, i ≥ a and k ≥ c.
- α ≤ T: every (T+1)-subset contains a triple.
- F7 is not encoded. With `LAZYF7=1`, a model that contains F7 gets one 5-literal clause per F7 copy instead of being output. This removes exactly the patterns that contain that copy.

**Supporting code.**
- My F7 finder agrees with `pchk`'s independent F7 test on all 8,083 models of prefix 0 when F7 is allowed: 5,015 contain F7, 0 mismatches.
- Blocking by the 12 true literals is exact, because every model has exactly 12 true triples.

**Validation against known values** (`cnf_validation.log`):
- (n, T) = (9, 6): 10,226 models = 8,570 F7-free + 1,656 with F7. This equals L002 round 3's brute force.
- (10, 6): 79,488 F7-free, the value in `tests/test_census_counts.py`.

### C2. Exhaustive independent comparison on 719 census prefixes (`compare_sat.py`; `compare_final.log`, `coverage_final.log`)

**Which prefixes were enumerated:**
- all 563 prefixes with census time ≤ 10 s;
- prefix 0;
- 155 prefixes from a seeded random sample (`make_cubes.py`, seed 20261015) of 200 prefixes with census time > 10 s. The remaining 45 were not reached within the 3-hour job limit. The sample was run in shuffled order, so the completed part is itself a random subset.

The 719 prefixes include 61 with census time > 100 s and 24 with > 300 s, among them prefix 0 (2,130 s, 3,003 solutions). All 11 possible first edges occur.

**Per-cube requirements:**
- the F7-free canonical models equal the census prefix file exactly;
- the number of F7-free models equals the census `leaves` count;
- every F7-free non-canonical model has its mirror somewhere in the census;
- non-census cubes have no F7-free model.

**Result:**
- **6,102 cubes:** the 719 census prefixes plus all 5,383 non-census cubes.
- 47,393 F7-free models, all with α = 8: 22,237 canonical and 25,156 non-canonical.
- `PROBLEMS {}`.
- 44,706 of the 205,529 orbits (21.8%) have a member in a fully enumerated cube. For these orbits, presence in the census is verified, and absence would have been detected.
- Total SAT time: 10,855 s.
- Earlier runs with F7 allowed (prefix 0 and prefixes 2534–2536) also matched.

### C3. Random-model containment across all prefixes (`sample14.py`, `check_members.py`; `sampler_members.log`)

**Method.**
- 4,044 random tries.
- Each try takes a uniformly random census prefix and random preferred phases.
- With probability 1/2 it adds one random extra assumption at a midpoint between 4 and 12.
- The conflict budget is 20,000 and F7 is handled lazily.

**Result.**
- 2,160 distinct F7-free models (including 23 from a smoke test), all of them in the census.
- They lie in 1,348 distinct census prefixes, and in 1,742 when mirrors are counted.

### C4. Per-prefix reflection consistency of the whole census (`leaves_check.py`; `leaves_check.log`)

**The identity.** For every prefix c:

  leaves(c) = sol(c) + #{P in census : P ≠ refl P, and the prefix of refl P is c}.

The non-canonical leaves are not stored. But if the search is complete, they are exactly the mirrors of census patterns.

**Result.**
- The identity holds for all 2,537 prefixes.
- No mirror falls into a non-census cube.

**What it does and does not show.**
- No orbit is half-missed anywhere in the census.
- A missing orbit would have to be lost both by the search below its own prefix and by the search below its mirror's prefix. These are different subtrees.

### C5. Engine reruns (`rerun_engine.py`; `rerun_engine.log`)

- I reran 20 random prefixes outside the C2 sample, with census time between 10 and 60 s.
- I used my fresh build of the HEAD source, with the driver's exact arguments.
- Solution sets, `nodes`, `leaves` and `solutions` are identical in all 20.

### C6. The `--refl` path at n = 12 (`refl_n12_compare.py`; `split12refl.log`)

**Why this was needed.** The census README validated the split driver at n = 12 only without `--refl`, while the n = 14 run used `--refl`.

**Run.** `python3 -m e757.ordered_dfs_split 12 7 10 2 1 <dir> --refl` produced:
- 107 prefixes;
- 1,113,245 solutions;
- 187,004,606 nodes.

**Comparison.**
- Every output pattern is canonical, and the patterns are distinct.
- The set is exactly the orbit set of the certified L002 output: 2,226,490 labelled patterns, 1,113,245 orbits.

### R1. Exact realization of all 205,529 patterns, without pre-filters (`realize14.py`, `realize_all14.py`; `realize_all14.log`)

**Method.**
- Solve 2x_j − x_l − x_r = 0 for j = 1..12, with x_0 = 0 and x_13 = 1.
- Use integer Bareiss forward elimination and Fraction back-substitution.
- Check the residual exactly against every original equation.
- Then test, in this order: strict order, the 3-AP set equal to the pattern, and the (4,5) property, each from the definition.

**Results over all 205,529 patterns.**
- No singular system: the determinant is nonzero for every pattern, so every pattern is rigid.
- Outcomes: order 197,763; extra AP 2,877; not (4,5) 1,979; **realizable 2,910**.

**On the census's O′ subset** (flags read from `post/filtered.txt.gz`):
- order 41,751, extra AP 912, not (4,5) 846, realizable 2,910. This equals summary.json.
- The subset also excluded by a long core: 11,378 / 33 / 13. This also equals summary.json.

**The realizable patterns.**
- All are (4,5)-sets with h = 8 (Sidon DFS) and α = 8.
- They give 2,910 distinct normal forms.
- Patterns: mine − census = 0 and census − mine = 0. Normal forms likewise 0 and 0, with 0 disagreements.
- A_base is present.

**Pre-filters are not load-bearing.**
- No realizable pattern lies outside O′.
- No realizable pattern fails a long core.
- My own K31 count (no x < y < z with endpoint pairs {x,y}, {x,z}, {y,z}) reproduces 119,844 (`k31_count.log`), and no realizable pattern contains a medial triangle.

### R2. The 2,910 stored sets, from the definitions (`verify_sets.py`; `verify_sets.log`)

Every set:
- consists of distinct sorted integers;
- is a (4,5)-set;
- has a rank-order 3-AP pattern equal to the stored edges;
- has m = 12;
- has h = 8 by exhaustive Sidon search and α = 8;
- does not beat the record: 8/14 = 4/7 exactly.

The normal forms are pairwise distinct, the maximum normalized coordinate is 3,960, and A_base is present. `PROBLEMS {}`.

### R3. F7 patterns are unrealizable (`f7_realize.log`)

All 5,048 distinct F7-containing models from the four cubes enumerated with F7 allowed are unrealizable: 4,696 order-infeasible and 352 with an extra AP. This is consistent with K7 [published].

### D1. Completeness against data not produced by the census (`collect14.py`; `collect14.log`)

**Sources.** I collected 1,808,461 distinct 14-point candidate sets, up to affine normal form, from:
- A_base and `data/small_records.json`;
- the 146 CP-SAT census sets, a different engine;
- all 14-subsets of the annealer's 18-set;
- the falsifier's random and adversarial sets, with all 14-subsets of their 16-sets;
- lp-fit random sets with n = 14..18 and small α, with all their 14-subsets;
- all 14-subsets of the 1,743 two-point extensions of A_base.

**(4,5)-sets with m ≥ 11:**

| m | h = 8 | h = 9 | h = 10 | h = 11 |
|---|---|---|---|---|
| 12 | 147 | 1,521 | 294 | – |
| 11 | 0 | 8,558 | 8,134 | 14 |

**Results.**
- All 147 sets with m = 12 and h = 8 are census classes: A_base plus the 146 CP-SAT sets.
- No set with m = 11 and h = 8 occurs.
- All 1,474 raw CP-SAT patterns at (14, 12, α ≤ 8) are in the census. They form 1,409 orbits.

### J. Frozen judge (`run_judge.py`; `spot_judge.txt`)

I ran the judge on 25 random census classes plus A_base. Result: **26/26** `PASS NO-IMPROVEMENT ... h=8 ratio=4/7`, exit 0.

### M1. Mathematics re-derived

- **Reduction.** For a 14-point (4,5)-set with m = 12 and h = 8, the rank-ordered pattern lies in the census class:
  - weak Sidon gives injective midpoints, never at an extreme, so m = 12 means every interior vertex is the midpoint of exactly one AP;
  - the pattern is linear (two APs sharing a pair produce a 4-AP or {0,1,2,4}, which has only 4 distances);
  - it is F7-free (K7 [published]);
  - it satisfies K30 (x_j = (x_i + x_k)/2 ≥ (x_a + x_c)/2 = x_b whenever i ≥ a and k ≥ c);
  - α = h (K4).
- **Rigidity.** The determinant is nonzero for every pattern (R1), so each realization is unique up to positive affine maps.
- **Classes.** Reflection maps P to refl P, and realizability is invariant under reflection. So the realizable canonical patterns are in bijection with the affine classes (reflection included). This gives 2,910.
- **Scope.** With n = 14 and τ = 6, Henning–Yeo gives 102 ≤ 70 + 3m, so m ≥ 11. The m = 11 case is outside the claim, as the claim says.

## Problems found (in order of severity)

None blocks acceptance. Item 1 is a stated limitation of the verification. E1–E6 are editorial. None of them changes a sentence of the Statement, and none of them needs a computation.

1. **Limitation: completeness at n = 14 is independently re-enumerated only in part.**
   - What the independent check covers:
     - 719 of the 2,537 prefixes, 8.8% of the nodes and 21.8% of the orbits, exhaustively (C2);
     - every one of the 7,920 depth-3 cubes outside the census prefix list (T3);
     - the whole census through the per-prefix reflection identities (C4), random containment (C3), reruns (C5) and independent data (D1).
   - What it rests on for the rest:
     - completeness on the remaining orbits rests on my reading of the engine (T2);
     - that engine is the one fully re-enumerated by independent referees at n ≤ 12 (L002, L003), and its code path at n = 14 is the same.
   - Cost of a full independent run: my CNF processes about 0.92M census-nodes per second, so a full run would take about 34 CPU-hours.
   - **Recommendation:** record in LEDGER/K45 that the n = 14 completeness was re-checked independently by sampling plus whole-census consistency checks, not by a second full enumeration.
2. **E1. Step 2 misdescribes the symmetry reduction.**
   - The text says "(depth-3 prefixes, 2,537 of them, one representative per reflection orbit)".
   - The 2,537 prefixes are *all* surviving depth-3 nodes, and they cannot be orbit representatives (T2).
   - The reduction is a leaf filter applied after the full search below each prefix.
   - Suggested wording: "all 2,537 surviving depth-3 prefixes were searched; a solution P is output only if sorted(P) ≤ sorted(refl P), so each reflection orbit appears exactly once: 205,529 orbits = 410,643 labelled patterns, 415 of them reflection-symmetric".
3. **E2. Step 3's failure-reason arithmetic is wrong as written.**
   - The text says "order-infeasible 41,751 + 11,378 excluded by a longer core; forced repeated difference 846 + 13; forced extra AP 912 + ...".
   - The second numbers are *subsets* of the first: summary.json counts "(excluded by long core) X" in addition to X.
   - The correct breakdown is 2,910 + 41,751 + 912 + 846 = 46,419.
   - Suggested wording: "order-infeasible 41,751, forced extra AP 912, forced repeated difference 846 (of which 11,378, 33 and 13 are also excluded by a 5–6-edge core)".
4. **E3. DEPENDS ON can be weakened.** K31–K33 are not needed for the count: R1 realized all 205,529 patterns without any pre-filter and obtained the same 2,910. This is as in L002/L003. K7 is imposed by the enumeration. That is legitimate, since it is [published], and R3 corroborates it.
5. **E4. Provenance.** "commit d2f70f5 plus the prefix-split option" is inaccurate: the prefix-split code is part of d2f70f5. Suggested wording: "e757/c/ordered_dfs.c at d2f70f5 (unchanged since; binary built 2026-10-14 11:15 UTC, before the launch)".
6. **E5. "277,501 CPU-seconds".** The engine's `time` is CLOCK_MONOTONIC wall time per process, and the processes were niced and shared cores. So this figure is summed process wall time, not CPU time.
7. **E6. The n = 12 validation omits `--refl`.** "The same split driver reproduces the certified n=12 count 2,226,490 exactly" is true only without `--refl`, but the n = 14 run used `--refl`. C6 now covers the `--refl` path; I suggest citing it.

## Reproduction (from `experiments/referee/L004/`; S = a scratch directory)

```
gcc -O2 -o pchk pchk.c
git show HEAD:e757/c/ordered_dfs.c > census_src_HEAD.c && gcc -O2 -march=native -o census_bin census_src_HEAD.c -lm
python3 check_book.py ../../20261014-1005-census-dfs/n14/results census_keys.txt.gz                      # T1
./census_bin n=14 T=8 m_min=12 m_exact=12 f7=1 progress=0 refl=0 mode=prefixes depth=3                    # T3
python3 make_cubes.py; LAZYF7=1 python3 sat14.py 14 8 $S/x.gz list:cubes_noncensus.txt                     # T3
python3 sat14.py 9 6 $S/v9.gz all; python3 sat14.py 10 6 $S/v10.gz all                                     # C1
bash run_sat_batches.sh cubes_cheap.txt 100 $S/sat_cheap; bash run_sat_batches.sh cubes_sample_rest_shuffled.txt 5 $S/sat_sample_rest
python3 compare_sat.py census_keys.txt.gz <prefixes.txt> <results> <sat outputs...>; python3 coverage.py <sat outputs...>   # C2
python3 sample14.py $S/sample_seed7.gz 1800 7; python3 check_members.py census_keys.txt.gz $S/sample_seed7.gz       # C3
python3 leaves_check.py                                                                                    # C4
python3 rerun_engine.py 20 60 31415                                                                        # C5
python3 -m e757.ordered_dfs_split 12 7 10 2 1 $S/split12refl --refl; python3 refl_n12_compare.py $S/split12refl  # C6
python3 realize_all14.py census_keys.txt.gz <results>/post my_realizable.txt.gz                            # R1
python3 verify_sets.py <results>/post spot; python3 run_judge.py                                           # R2, J
python3 collect14.py <results>/post                                                                        # D1
```
