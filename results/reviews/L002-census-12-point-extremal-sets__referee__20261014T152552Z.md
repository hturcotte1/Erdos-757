VERDICT: ACCEPT

# Referee report, round 3: L002-census-12-point-extremal-sets (certificate: exhaustive enumeration with exact realization)

- **Referee:** referee subagent (Opus 5.5, max effort), 2026-10-14, round 3.
- **Scratch:** `experiments/referee/L002-round3/`. It holds scripts and logs. The large pattern dumps were written to the session scratchpad; each can be regenerated with the commands below.
- **Independence:**
  - Nothing was imported from `e757/`, `judge/` or the round 1–2 directories.
  - The census files and the earlier referee logs were read only as data to compare against.
  - The judge was run read-only, on claim files in my scratch directory.
- **Load:**
  - One heavy process at a time.
  - Longest single process: 14.5 min (cube chunk, C2).
- **Claim file reviewed:** `results/proofs/L002-census-12-point-extremal-sets.md` at commit 2fe58fc, after the round-2 revision.

## Summary

The certificate is correct, and its text now matches its evidence. Both round-2 fixes are applied correctly: the realizer is attributed to `fastreal.py` with 0 fallbacks, and the m ≤ 8 result is attributed to the referee runs.

I re-verified the result with a fourth pipeline. It shares no code and no search design with the census engine or with rounds 1–2. It consists of:
- a CNF encoding of the pattern class, decided and enumerated by CDCL (CaDiCaL 1.5.3 through pysat);
- my own F7 test;
- my own exact rational realizer and set verifier, written in C.

Results:
1. **Every pattern with α ≤ 7 is saturated.** No 12-vertex ordered pattern that is linear, midpoint-injective and K30, with F7 allowed, has α ≤ 7 and an interior non-midpoint. All 121 cubes are UNSAT. So m = 10 needs neither Henning–Yeo nor F7-freeness. α ≤ 6 is UNSAT outright.
2. **Enumeration matches the census exactly.** The CDCL enumeration of saturated α ≤ 7 patterns gives exactly 2,678,082 models: 2,226,490 F7-free and 451,592 containing F7. The F7-free set equals the census file exactly.
3. **Realization matches the census exactly.** Exact realization of all 2,678,082 gives 108,486 realizable patterns, all with h = 7. These form 54,243 affine classes, each arising from exactly {P, refl P}, and the class list is identical to the census list. On the claim's O′ subset my realizer reproduces 321,304 / 10,803 / 8,689 / 54,243.
4. **Every census set re-verified.** All 54,243 census sets pass my checks from the definitions.
5. **A new completeness test from independent data.** I drew 2,719,481 distinct 12-point (4,5)-sets from other generators in the repository (subsets of larger sets, random and adversarial falsifier sets). Exactly 26 have h = 7, and all 26 are census classes.

Only editorial notes remain. None of them affects the argument.

## Steps and status

| # | Step | Status |
|---|---|---|
| 1 | Reduction to ordered patterns (K3–K6, K30; class O adds K7); m ≤ 10 | **Verified.** Re-derivations are in C8. The m ≤ 9 exclusion holds without K7 or K8 (C2). |
| 2 | Census DFS: 2,226,490 at m = 10, 1,113,245 up to reflection; 0 at m = 9; m ≤ 8 by HY or the referee runs | **Verified.** Code read (T2); exact set equality with an independent CDCL enumeration (C3); m ≤ 9 independently UNSAT (C2); provenance of every cited log checked (T1). |
| 3 | Filters 754,235 / 395,039; realization 54,243 + 321,304 + 10,803 + 8,689; rigidity | **Verified** with my own realizer, both on O′ and on all patterns (C4). Rigidity argument checked (C8), and 0 singular systems. |
| 4 | 54,243 classes; known sets present; judge | **Verified.** Normal forms (C4, C5); known sets (C6); judge 20/20 (C7). |

## Checks performed

### T1. Text against evidence (every number in the claim)

- **m = 10 run.** 2,226,490 solutions, 187,004,404 nodes, 287.7 s. Source: census README, and round 2 R7 for the d2f70f5 reproduction.
- **m = 9 run.** `m9/dfs_done.txt` reads `DONE nodes=425209182 leaves=2226490 solutions=0 timed_out=0 time=607.48`.
- **Filter counts.**
  - `results/realize_summary.json` gives canon 1,113,245, k31 754,235, c4 395,039, call 313,774.
  - My own tally of the flags in `results/n12_m10_filtered.txt.gz` gives 359,010 (K31 fails) + 359,196 (a ≤4-edge core fails) + 81,265 + 313,774.
  - 718,206 = 359,010 + 359,196, as stated.
- **Realizer attribution.** `"n_fallback_to_realize_exact": 0`, so "decided by fastreal.py" is accurate.
- **m ≤ 8 provenance.** Both cited logs exist and say what the claim says:
  - `experiments/referee/L002/n12/mle8_runs.log` has `sols=0` in all 11 splits.
  - `experiments/referee/L002-round2/enum_n12_noneall.log` has `maxnone=10 ... COUNT m=10 alpha<=T: f7free=2226490 f7=451592`.
  - I read round 2's `enum.c`. It prints a COUNT line for every m with a nonzero count, and it filters nothing on F7. So that log really does cover all m with F7 allowed.
- **CP-SAT containment.** `results/crosscheck.json` reads `{"cpsat_raw_lines": 30559, "cpsat_canonical": 29228, "found_in_dfs": 29228, "missing": 0}`.
  - This is containment up to reflection.
  - Literal containment follows because the DFS output is closed under reflection (C3).
- **Tests.** `slowtest/run.log` shows `pytest -k "10-8-6 or 9-7-6"` with 2 passed. The test does compare the C DFS with CP-SAT native enumeration, as stated.
- **Judge.** `results/judge_spotcheck.txt` has 50 lines of PASS NO-IMPROVEMENT with h = 7.
- **Commit pins.** `e757/c/ordered_dfs.c` was changed only in ea6c3d9 (00:23) and d2f70f5 (11:17). The census output was committed in a887219 (11:00), between the two. This is consistent with "produced with ea6c3d9 source, reproduced at d2f70f5". The working tree equals HEAD.

### T2. My own reading of the census engine (`e757/c/ordered_dfs.c`, = d2f70f5)

- **Branching.** For midpoint j = 1..n−2 in order, a child is (i, j, k) with all three pairs uncovered (linearity) and k > max(M[i], j).
  - Here M[i] is the maximum right endpoint over placed edges whose left endpoint is ≥ i.
  - This is exactly K30 against every earlier midpoint: j′ < j together with i′ ≥ i and k′ ≥ k would force x_{j′} ≥ x_j.
- **NONE budget.** `forced` counts midpoints r ≥ j with no feasible triple. Feasibility only shrinks as edges are added, so the budget test is sound.
- **Look-ahead.** `ind_search2` maximizes |S| − #{r ∈ S ∩ R_f : some currently feasible triple (i, r, k) lies inside S} over sets S independent in the placed edges.
  - Every completion uses only triples that are feasible now.
  - So S minus its killed midpoints is independent in every completion, which makes the bound sound.
  - The branch-and-bound cut `val + |cand| <= best` is valid because the killed set only grows.
- **Leaves.** Exact α is computed by `ind_search`, and m = m_exact is required.
- **`has_f7`.** A centre, three disjoint arms, and the two complementary transversals: this is exactly F7.
- **Prefix options.** They are inert when `plen = 0`.

No defect found.

### C1. My own CNF model, validated

`sat_model.py` encodes the class as follows:
- one variable per triple (i < j < k), where j is the midpoint;
- at most one triple per midpoint;
- pairwise linearity;
- K30 as binary clauses;
- α ≤ T as "every (T+1)-set contains a triple";
- optionally, saturation, or "at least one empty midpoint" via auxiliary variables.

Validation:
- **Against my own brute force over all maps** (`brute_small.py`) at n = 7 and n = 8: every cell agrees.
  - Example (n = 8, α ≤ 6, any m): 252, 4,270, 8,301, 4,188 + 80 F7, and 286 + 110 F7.
  - `sat_enum.py 8 6 any` gives 17,487 models, which equals the brute-force total.
- **n = 9, saturated:** α ≤ 6 gives 8,570 F7-free + 1,656 F7; α ≤ 7 gives 8,608 + 1,656. Both equal round 2's brute force.
- **n = 10, saturated** (`sat_n10.log`): α ≤ 6 gives 79,488 F7-free (the test value); α ≤ 7 gives 302,316 (round 2, R3).

### C2. m ≤ 9 is impossible at n = 12 with α ≤ 7, without Henning–Yeo and without F7-freeness

- **Monolithic attempt.** `python3 sat_decide.py 12 7 nonsat cd15` did not finish in 1080 s (recorded in `sat_decide_n12_T7_nonsat.log`).
- **Cube and conquer.** Command: `python3 sat_cubes2.py 12 7 nonsat 1 10 cd15 <outer indices>`.
  - The cubes are (option at midpoint 1) × (option at midpoint 10), where an option is a triple or "empty". There are 11 × 11 = 121 cubes, and they partition the space.
  - Every cube is **UNSAT**. Logs: `sat_cubes2_nonsat_idx0-6.log` and `sat_cubes2_nonsat_idx7-10.log`.
  - Per-outer times: 57, 96, 171, 179, 167, 125, 73, 40, 22, 5 and 281 s.
  - An earlier single-solver run (`..._run1_timeout.log`) also reached the end of outer option 6 with no SAT cube before its timeout.
- **α ≤ 6 and α ≤ 5.** UNSAT for both the saturated and the non-saturated encodings (`sat_decide_T56.log`). This gives f(12) ≥ 7 with no appeal to HY.

### C3. Independent CDCL enumeration of all saturated α ≤ 7 patterns

- **Command.** `bash run_sat_enum_all2.sh`, which runs `sat_enum_cubes2.py 12 7 1 10 cd15 <k>`.
  - One process per split, where the split is midpoint 1 = (0, 1, k).
  - A fresh CaDiCaL solver per (midpoint 1, midpoint 10) cube.
  - Models are blocked by their positive literals. This is exact for saturated models, which have no proper super-pattern in the class.
- **Per-split totals** for k = 2..11 (`sat_enum2_k*.log`): 0, 393,809, 507,776, 492,197, 433,900, 338,573, 246,980, 153,313, 103,751, 7,783. The sum is **2,678,082**.
  - These equal round 1's per-split leaf counts in `mle8_runs.log`, and round 2's total.
  - The 10 × 10 per-cube matrix satisfies M[k][i] = M[11−i][11−k]. This is the reflection symmetry, and it serves as a built-in consistency check.
- **Comparison with the census** (`python3 final_compare.py <scratch>`, output in `final_compare.log`).
  - 2,678,082 distinct models: 451,592 contain F7 and **2,226,490 are F7-free**. The F7 test is my own (`f7split.py`).
  - **census − mine = 0 and mine − census = 0.**
  - The set is closed under reflection, with 0 self-symmetric patterns, and there are 1,113,245 F7-free patterns up to reflection.

### C4. Exact realization with my own solver (`vr.c`)

**Method.**
- Rational Gauss–Jordan elimination, with int64 numerators and denominators, __int128 intermediates, and an abort on overflow.
- An exact residual check against every AP equation.
- Integer scaling, followed by a check of strict order and a check that the 3-AP set equals the pattern.
- The (4,5) property checked over all 4-subsets.
- h computed by an exhaustive DFS over Sidon subsets, using the difference definition.
- α of the 3-AP hypergraph computed by a scan of all 2^12 subsets, and asserted equal to h.

**Results.**
- **All 2,678,082 CDCL models** (`vr_realize_sat_all.stderr`):
  - `singular=0 residfail=0 order=2441008 extra_ap=85218 not45=43370 realizable=108486 h_hist: 7:108486`.
  - The realizable patterns give 54,243 distinct normal forms, each from exactly 2 patterns.
  - Against the census class list: census − mine = 0 and mine − census = 0.
  - The maximum normalized coordinate is 1008.
- **All 2,226,490 census patterns** (`vr_realize_census.stderr`):
  - `order=2008558 extra_ap=66076 not45=43370 realizable=108486`.
  - So every realizable pattern is F7-free; none of the 451,592 F7 patterns is realizable.
- **The O′ subset** (census flags 1 1 1 *; `vr_oprime.log`):
  - `patterns=395039 order=321304 extra_ap=10803 not45=8689 realizable=54243`. This is exactly the claim's breakdown.
  - It also follows that the 718,206 filtered canonical patterns contain no realizable pattern.

### C5. All 54,243 census sets re-verified (`results/realized_n12.json.gz`)

Pipeline: `census_to_vr.py | ./vr set`, then `check_b.py`.

For every set:
- the elements are distinct;
- it is a (4,5)-set;
- h = 7 by the Sidon DFS, and α = 7;
- m = 10;
- its rank-order AP pattern equals the stored edges.

The 54,243 affine normal forms are pairwise distinct (`check_b.log`: `problems={}`).

### C6. Completeness test against independent data

`python3 collect_indep.py | ./vr set` gathers 2,719,481 distinct 12-point sets, deduplicated by affine normal form, from:
- every 12-subset of A_base;
- the 14-point CP-SAT census sets (both files);
- the annealer best (the only set stored in `best.json`, n = 18);
- the 1,743 A_base two-point extensions;
- the falsifier's random and adversarial sets (n = 12–14);
- lp-fit random sets, with all of their 12-subsets, restricted to keep the run under 20 minutes: n = 12 with α = 7, n = 13 with α ≤ 8, n = 14 with α ≤ 9, n = 15 with α ≤ 9, n = 16 with α ≤ 10, and n = 18 with α ≤ 11.

Results:
- All 2,719,481 are (4,5)-sets. Their h distribution is 7: 26, 8: 172,471, 9: 1,756,858, 10: 781,017, 11: 9,109.
- The 26 sets with h = 7 come from these sources:
  - 3 known records;
  - 19 from the falsifier's random and adversarial generators;
  - 2 random lp-fit 12-sets;
  - 2 subsets of random lp-fit 14-sets.
- All 26 have m = 10, and **all 26 classes are in the census.**

### C7. Frozen judge

`python3 judge/judge.py experiments/referee/L002-round3/spot/*.json` was run on 15 random census classes and 5 random C6 sets. Result: **20/20** `PASS NO-IMPROVEMENT ... h=7 ratio=7/12`, exit 0 (`spot_judge.txt`). As a ratio check, 7/12 > 4/7 because 49 > 48, so no class is a record.

### C8. Mathematics re-derived

- **K3 (weak Sidon).** Suppose x + y = z + w with x < z < w < y. Then z − x = y − w and w − x = y − z, so the four points have at most 4 distinct distances.
- **K4 (h = α).** For weak Sidon sets, Sidon is equivalent to 3-AP-free. In the difference form: b − a = d − c on distinct pairs gives a + d = b + c with {a, d} ≠ {b, c}.
- **K5 (midpoints).** Midpoints are injective by weak Sidon and are never extreme points.
- **K6 (linearity) needs (4,5), not just weak Sidon.** The set {−2, 0, 1, 2} is weak Sidon but has only 4 distinct distances, and its APs (−2, 0, 2) and (0, 1, 2) share the pair {0, 2}.
  - Round 2's remark "each needs only weak Sidon" is therefore wrong for K6.
  - The claim itself correctly cites K6 as a property of (4,5)-sets [published].
- **K30.** x_j = (x_i + x_k)/2.
- **Rigidity.** I − B is weakly chained diagonally dominant: following left endpoints reaches a row with l(j) = 0, which is deficient. So I − B is nonsingular.
- **Class bijection.** Positive affine maps preserve the ordered pattern, and negative ones reflect it. The pattern then fixes the set up to positive affine maps. A self-symmetric pattern would not break the bijection, and none exists anyway.

## Problems found (all editorial; none is a gap in the certificate)

1. **The dependency remark mixes two classes.** DEPENDS ON and Step 1 justify dropping K8 by saying "every class-O pattern ... with α ≤ 7 has exactly 10 edges". But class O is defined to be F7-free.
   - Dropping K7 and K8 *together* needs that statement without F7-freeness.
   - It does hold in that form. The round-2 log cited in Step 2 has no F7 filter, and C2 above confirms it independently.
   - Suggested wording: "every linear, midpoint-injective, K30 pattern (F7 allowed) on 12 vertices with α ≤ 7 has exactly 10 edges".
2. **The STATUS line is stale.** It still mentions only the round-1 revision.
3. **Unbalanced parentheses in DEPENDS ON.** The text reads "((4,5) implies weak Sidon; (h = alpha …".
4. **"Each core … re-derived by an independent referee".** The recomputation is in `experiments/referee/catalogue-n8/README.md`, and there is no review file for it. Cite that path. This is immaterial, because the count does not use the cores (C4).
5. **Outside the claim file (optional).**
   - K41 in `kb/known_results.md` and the "Exhaustiveness and the statement" paragraph of the census README still give the older, weaker dependency chain ("modulo Henning–Yeo and K30/K31/core").
   - K41 also says "the 5 known 12-point sets"; these are three distinct sets.
   - The certificate now supports "K3–K6 [published] and K30 only". The CDCL result of C2 can be cited as a third independent m ≤ 9 confirmation.

## Reproduction (from `experiments/referee/L002-round3/`)

```
gcc -O2 -o vr vr.c
python3 brute_small.py 8; python3 sat_enum.py 8 6 any OUT.gz g4; python3 f7split.py OUT.gz FREE.gz   # C1
python3 sat_cubes2.py 12 7 nonsat 1 10 cd15 0,1,2,3,4,5,6; python3 sat_cubes2.py 12 7 nonsat 1 10 cd15 7,8,9,10  # C2
bash run_sat_enum_all2.sh; python3 final_compare.py <scratch>                                          # C3
zcat <scratch>/sat_all_lines.txt.gz | ./vr pat 12                                                      # C4
python3 census_to_vr.py EDGES.txt | ./vr set > OUT; python3 check_b.py OUT EDGES.txt CLASSES.txt       # C5
python3 collect_indep.py | ./vr set                                                                    # C6
```
