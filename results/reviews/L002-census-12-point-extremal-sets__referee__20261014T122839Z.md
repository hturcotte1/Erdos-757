VERDICT: NEEDS-WORK

# Referee report: L002-census-12-point-extremal-sets (certificate: exhaustive enumeration with exact realization)

Referee: referee subagent (Opus 5.5, max effort), 2026-10-14. All scratch code and logs: `experiments/referee/L002/`.
Nothing from `e757/` or `judge/` was imported. The judge was run read-only on temporary claim files in the scratch directory.

## Summary

**The Statement is correct, and I confirmed it independently.** Up to affine equivalence there are exactly 54,243 twelve-point (4,5)-sets with h = 7. Each has m = 10 and is affinely rigid.

- **Independent enumerator.** I wrote my own enumerator (CSP over the interior vertices, MRV ordering, forward checking, and a transversal-bitset bound on α).
  - It reproduces the census DFS output exactly as a set: 2,226,490 labelled patterns at m = 10.
  - It finds 0 patterns at m = 9 and 0 at m ≤ 8.
  - A run with no α-pruning at all gives the same counts. That run covers all 686,700,420 saturated linear K30 patterns and computes α exactly at every leaf.
- **Census engine against brute force.** The census engine (source at commit ea6c3d9, rebuilt) agrees with a pure brute force on all 108 (n, m, T) cells for n = 5..10.
- **Exact realization of every pattern.** My own exact integer solver realized all 2,226,490 patterns, not just the 395,039 that the submission realized.
  - Exactly 108,486 are realizable, i.e. 54,243 reflection pairs.
  - This is the submitted list exactly.
- **Every submitted set re-verified.** (4,5) checked from the definition; h = 7 by brute force over all 4096 subsets and by a CP-SAT ILP; judge 43/43 on a sample.

**Why NEEDS-WORK.** The write-up misstates its own dependency structure.

- **K31 and the small cores carry weight.** In the submitted pipeline, 718,206 of the 1,113,245 canonical patterns were discarded by K31 or by the ≤4-edge forbidden cores and were never realized. So, as submitted, the count depends on K31 and on every ≤4-edge core of K32–K33. The DEPENDS ON line says the opposite ("used only as a filter, not for completeness"; "rejections are re-confirmed by exact realization").
- **Rigidity.** The justification "all rigid since m = n−2" is incomplete.
- **CP-SAT cross-check.** It is presented as playing the falsifier's role, but it is only a containment check against an unfinished enumeration.

All of this is fixable in the text. The evidence below already fills every gap. It also shows that the result does not need K7, K8, K31, K32 or K33: only K4–K6 [published] and K30 (a one-line proof, re-checked).

## Steps of the certificate and their status

| # | Step (as written) | Status |
|---|---|---|
| S1 | h = 7 gives τ = 5; HY gives 85 ≤ 60 + 3m, so m ≥ 9; K5 gives m ≤ 10. The pattern lies in class O (linear K6, F7-free K7, injective midpoints K5, K30). | **Verified.** The arithmetic is correct. The K30 proof was re-checked: x_j = (x_i + x_k)/2 < (x_i' + x_k')/2 = x_j'. HY's hypotheses (3-uniform, linear, F7-free) hold by K6 and K7. **Stronger result (C3):** inside {linear, injective midpoints, K30} every 12-vertex pattern with α ≤ 7 has exactly 10 triples. This needs neither HY nor F7. |
| S2 | The C DFS enumerates class O for n = 12 and α ≤ 7: 2,226,490 patterns at m = 10 and 0 at m = 9. | **Verified** by reading the code (C1), by brute force for n ≤ 10 (C2), by an independent enumerator with identical output (C3), and by brute force at n = 12 (C3). |
| S3 | Filters: 754,235 K31-free; 395,039 also core-free. Realization of those 395,039: 54,243 realizable; failures 321,304 order / 10,803 extra AP / 8,689 repeated difference. | The **conclusion is verified directly** by realizing all patterns (C5). The K31 count and the reason breakdown match exactly. The justification as written depends on K32–K33 (problem 1). "All rigid since m = n−2" is incomplete (problem 2). |
| S4 | Rigid realizable patterns, up to reflection, correspond one-to-one to affine classes. The known sets are present. Judge sample. | **Verified.** There are 54,243 distinct normalized sets, each arising from exactly two labelled patterns (P and its reflection). There are no symmetric patterns. All 3 distinct known sets are present. |

## Checks performed

**C1. Code reading of the census engine** (`git show ea6c3d9:e757/c/ordered_dfs.c`; the working-tree file has since gained prefix-split options in d2f70f5, all gated by `plen`/`mode_pref`, so behaviour is the same for the census command).

- **Branching.** Midpoints j = 1..n−2 are processed in order. A child is any (i, j, k) whose three pairs are uncovered (this is linearity), with k > max(M[i], j). Here M[i] is the largest right endpoint among placed edges whose left endpoint is ≥ i; this is exactly K30 against all earlier midpoints. NONE is allowed while the budget lasts.
- **Forced-NONE count.** Feasibility only shrinks as edges are added, so the count is sound.
- **α look-ahead (`ind_search2`).** It searches for S with value(S) = |S| − #killed. The maximum of value(S) equals α(H′), where H′ is the placed edges together with all currently feasible triples. Every completion is contained in H′, so the look-ahead is sound.
- **F7 test.** It looks for a centre with three disjoint arms plus two transversals that partition the arms. That is exactly F7 as a subhypergraph.
- **Leaves.** α is computed by an exact branch and bound, and the edge count must equal m.

I found no soundness defect.

**C2. Census binary against brute force, n = 5..10.**
- Commands: `python3 compare_small.py 9` and `python3 compare_small.py 10 10` (outputs `compare_small_n5_9.txt`, `compare_small_n10.txt`).
- Result: `cells=79 mismatches=0` and `cells=29 mismatches=0`.
- What was compared on each cell:
  - (a) `mydfs allm=1`: only pairwise linearity/K30, exact α by DP over 2^n subsets, F7 by testing every 5-subset of edges;
  - (b) my pruned search;
  - (c) `census_src/ordered_dfs_census … f7=1 mode=count`.
- Examples: (7,5,5) = 10, (8,6,5) = 260, (9,7,6) = 8570, (10,7,6) = 36,210, (10,8,6) = 79,488.
- At n = 11 the census binary and my pruned search also agree: (11,9,6) = 0 and (11,9,7) = 9,871,248.

**C3. Independent enumeration at n = 12** (`mydfs.c`; split = r fixes midpoint 1's triple to (0,1,r); r = 0 means midpoint 1 is NONE). Totals are in `n12/summary.txt`.
- **m = 10, pruned** (`./mydfs n=12 m=10 T=7 prune=1 print=1 split=r`, r = 2..11):
  - Per-split counts: 0, 317206, 419069, 412333, 367417, 287604, 208253, 126807, 82605, 5196. These equal the census per-split counts (`census_split_counts.txt`). Total 2,226,490.
  - The two sorted pattern lists are identical: `LC_ALL=C comm -3` gives 0 lines.
- **m = 9, pruned:** 0 in all 11 splits.
- **m ≤ 8 (`mle=1`):** 0.
  - In these runs, the complete patterns passing α ≤ 7 number 2,678,082 = 2,226,490 F7-free + 451,592 containing F7, and all have exactly 10 edges.
- **No α-pruning** (`prune=0 fastleaf=1`):
  - m = 10: 686,700,420 saturated linear K30 patterns. The F7-free ones with α ≤ 7 number 2,226,490, and the per-split counts are identical.
  - m = 9: 3,389,574,440 leaves, 0 solutions.

**C4. Integrity of the DFS output** (`check_codes.py`). There are 2,226,490 distinct patterns. The set is closed under reflection, and no pattern is self-symmetric.

**C5. Exact realization of ALL patterns** (`zcat …/n12_m10_all.jsonl.gz | ./realize12 … ; log realize_full.log`).

How the solver works:
- It solves 2x_j − x_{l(j)} − x_{r(j)} = 0 with x_0 = 0 and x_11 = 1 by fraction-free elimination in int64/__int128.
- It back-substitutes exactly in integers and asserts divisibility.
- It checks the residual against the original equations.
- It then checks strict order, that the set of 3-APs equals the pattern, the (4,5) property from the definition, and h by brute force over 4096 subsets.

Output:
```
lines=2226490 badstruct=0 nonlinear=0 k30fail=0 f7=0 alpha>7=0   alpha_hist: 7:2226490
singular=0 divfail=0 residfail=0 order_infeasible=2008558 extra_ap=66076 not45=43370 realizable=108486   h_hist: 7:108486
distinct canonical sets: 54243 (each from exactly 2 labelled patterns); theirs - mine: 0, mine - theirs: 0; max coordinate 1008
```

Further checks:
- **O′ subset** (selected by the submission's flags): `order_infeasible=321304 extra_ap=10803 not45=8689 realizable=54243`. This matches S3 exactly.
- **K31 recomputed** with my own medial-triangle definition (`k31_check.py`): 754,235 K31-free, agreeing with the census flag on all 1,113,245 patterns.
- **Without the F7 filter** (`realize12_nof7` on all 2,678,082 α ≤ 7 patterns): `f7=451592 … realizable=108486`. So F7-freeness is not needed for the count either.

**C6. Python re-verification of every submitted set** (`verify_sets.py …realized_n12.json.gz 54243 1`): 0 failures. The checks were:
- the elements are distinct;
- (4,5) holds, from the definition;
- the 3-AP set equals the stored edges, with m = 10;
- h = 7 by a CP-SAT ILP (status OPTIMAL; the witness was re-checked as Sidon from the definition).

The known sets reduce to three distinct sets under five names: record_12 = START_HERE §6 third set; 12b = omega ex. 1; 12c = omega ex. 2. Each is (4,5) with m = 10 and h = 7, each class is in the census, and the three are pairwise inequivalent.

**C7. Frozen judge** on 40 random census sets plus the 3 known sets (`python3 make_spot_claims.py 40; python3 run_spot.py`): 43/43 `PASS NO-IMPROVEMENT … h=7`, exit 0 (`spot_check_output.txt`).

**C8. CP-SAT containment.** All 30,559 CP-SAT labelled solutions appear in my enumeration (0 missing). `crosscheck.json` agrees.

**C9. Rigidity (proof).** For any saturated pattern the system matrix is 2(I − B), where B is substochastic. Row j is deficient when l(j) = 0 or r(j) = 11, and following left endpoints from any vertex reaches 0. So ρ(B) < 1 and the system is nonsingular. Computationally there are 0 singular systems among the 2,226,490 patterns.

**C10. Ratio.** 7/12 > 4/7, so no set in the census is a record (as claimed).

**Not re-verified, and immaterial after C5:**
- the 395,039 / 313,774 / 81,265 core-filter counts;
- the core library K32–K33 itself;
- the DFS node counts and timings.

## Problems, by severity

1. **The DEPENDS ON line misstates which facts the count depends on.**
   - `realize_all.py` realizes only patterns with flags k30 = k31 = c4 = 1 (`if fl[0] and fl[1]: … if fl[2]: pats.append`).
   - So 359,010 canonical patterns rejected by K31 and 359,196 rejected by ≤4-edge cores were never realized.
   - The submitted certificate therefore relies on K31, and on the soundness of every ≤4-edge core in `data/forbidden_ordered_n7.json` and `n8.json` (K32–K33 [verified-here]).
   - This contradicts "K31 … used only as a filter, not for completeness" and "rejections are re-confirmed by exact realization". That second sentence is also truncated ("…").
   - The conclusion is true (C5), but the stated evidence chain is not what the files contain.
2. **The rigidity argument is incomplete.** Step 3's "all rigid since m = n−2" does not follow from counting equations. Replace it with the M-matrix argument of C9, or cite the rank computation.
3. **The falsifier substitute is overstated.** The CP-SAT enumeration was time-limited, unfinished, and ran in the smaller class O′. It only shows that 30,559 patterns are contained in the DFS output; it does not show completeness. Completeness is now established by C2 and C3.
4. **Cosmetic: the known sets in S4.** "Five previously known sets (… '12', the two omega sets, the third set of START_HERE §6 …)" is garbled. '12' *is* the START_HERE §6 set, and '12b'/'12c' *are* the omega sets. Say "three distinct sets (five names)".
5. **Reproducibility.** `e757/c/ordered_dfs.c` changed after the census run (d2f70f5). Pin commit ea6c3d9 in the certificate. I checked that the change is behaviour-neutral for the census command and validated the ea6c3d9 build.

## What is needed for ACCEPT (text only; no new computation)

- Rewrite DEPENDS ON and Step 3 so they cite the full exact realization of all 2,226,490 labelled patterns: 108,486 realizable, none outside O′. The evidence is `experiments/referee/L002/realize_full.log` and `oprime_realize.log`, or the authors' own re-run.
- With that change, the certificate needs only:
  - K4–K6 [published];
  - K30;
  - the referee's checks that no pattern with m ≤ 9 has α ≤ 7 (C3, which also removes K8) and that the count does not depend on F7 (C5, which also removes K7).
- Fix the rigidity sentence (C9), the falsifier line, and the known-sets wording, and pin the engine commit.
- Optionally strengthen K41 in kb/known_results.md in the same way ("modulo HY and K30/K31/core conditions" can be reduced to "K4–K6 and K30").
