VERDICT: NEEDS-WORK

# Referee report, round 2: L002-census-12-point-extremal-sets (certificate: exhaustive enumeration with exact realization)

- Referee: referee subagent (Opus 5.5, max effort), 2026-10-14, round 2.
- Scratch: `experiments/referee/L002-round2/`.
- Independence:
  - Nothing from `e757/`, `judge/` or `experiments/referee/L002/` was imported or reused.
  - The census engine was only rebuilt, from `git show <commit>:e757/c/ordered_dfs.c`, in order to re-run it.
  - The judge was run read-only, on claim files in my scratch directory.
- Load: one process at a time, on a machine with load about 12 on 4 cores. Every computation took under 10 minutes.

## Summary

The Statement is correct. I verified it with a third, fully independent pipeline.

**My enumerator.** I wrote it from scratch. It differs from the census engine as follows:
- midpoints are processed right to left;
- K30 is tested explicitly, pair by pair;
- α ≤ 7 is tested exactly, as "every 8-subset contains a triple", with a sound static look-ahead;
- there is no F7 filter in the search.

At n = 12 and α ≤ 7 it produces:
- exactly 2,226,490 F7-free saturated patterns. After sorting, this list is byte-identical to the census file.
- 451,592 F7-containing patterns.
- no pattern at all with m ≤ 9, for any number of non-midpoints, without assuming F7-freeness.

**My exact realizer.** It solves in long double and then checks an exact int64 certificate that the integer vector solves the AP system. Order, the AP set, (4,5) and the Sidon number are then checked exactly. On all 2,678,082 patterns it finds:
- 108,486 realizable patterns, i.e. 54,243 reflection pairs;
- h = 7 for every one of them, computed from the Sidon definition;
- a set of normalized sets equal to the census list.

**Census engine re-run.** I rebuilt it from the pinned commit d2f70f5 and re-ran both runs; both reproduce exactly. The Step 3 pipeline numbers are also reproduced exactly.

So the mathematics and every number in the certificate are right. The revised DEPENDS ON line is also true in substance: only K3–K6 [published] and K30 are needed. K7, K8 and K31–K33 are not.

**Why NEEDS-WORK.** The text still misstates provenance in two places:
- Step 3 says the 395,039 patterns were "decided by `e757.realizability.realize_exact`". They were in fact decided by `experiments/20261014-1005-census-dfs/fastreal.py`; `realize_exact` was a fallback that was used 0 times.
- Step 2 attributes "0 for m ≤ 8" to the census C DFS, which was never run for m ≤ 8.

Both are one-sentence fixes, and no new computation is needed.

## Steps and status

| # | Step (as written) | Status |
|---|---|---|
| 1 | Reduction to class O (linear K6, injective interior midpoints K5, F7-free K7, K30); m ≤ 10; h = α = 7 | **Verified.** I re-derived K5, K6 and K30 from the definitions; each needs only weak Sidon (K3). h ≤ α is trivial (Sidon ⇒ 3-AP-free). α ≤ h holds because a 3-AP-free subset of a weak Sidon set is Sidon. F7-freeness is not needed (R4–R6). |
| 2 | C DFS: 2,226,490 at m = 10; 0 at m = 9; "0 for m ≤ 8" | **Numbers verified** (R1–R7). The m ≤ 8 result is attributed to a run that does not exist (Problem 2). |
| 3 | Filters 754,235 / 395,039; realization 54,243 + 321,304 + 10,803 + 8,689; rigidity | **Numbers verified** (R8, R9); the rigidity argument is correct (R12). The oracle is misnamed (Problem 1). |
| 4 | Bijection with affine classes; known sets; judge | **Verified** (R8, R10, R11). |

## Checks performed

**R1. Code reading of the census engine.**
- The working tree equals d2f70f5 (`cmp` against `git show d2f70f5:e757/c/ordered_dfs.c`: identical).
- The diff ea6c3d9..d2f70f5 only adds `pre=`/`mode=prefixes`. Every new branch is gated by `j <= plen` (with plen = 0) or `mode_pref`, so the census commands are unaffected.
- I re-checked each component:
  - branching over (i, j, k) with linearity via `nb`;
  - K30 via the staircase M[i] (the maximum right endpoint over placed edges with left endpoint ≥ i);
  - the forced-NONE budget;
  - the `ind_search2` look-ahead. It is sound: any completion uses only currently feasible triples, so S minus its killed midpoints stays independent;
  - `has_f7`: a centre, three disjoint arms, and two complementary transversals;
  - the exact α at the leaves.

  All are sound.

**R2. My enumerator against a plain brute force, n = 5..9.**
- `brute.py` is Python with no pruning. It tests F7 by explicit isomorphism over all 7! bijections and computes α by a full subset scan.
- Commands: `python3 brute.py n` for n = 5..9, then `python3 cmp_small.py`.
- What was compared: every (m, T), with pruning on and off, and the F7-free and F7 counts separately.
- Result: **cells 158, mismatches 0**.
- Brute-force values include (7,5,5) = 10, (8,6,5) = 260, (8,6,6) = 286 and (9,7,6) = 8570, all as in `tests/test_census_counts.py`.

**R3. My enumerator against the census engine (d2f70f5 build).**
- n = 10, m = 8:

  | T | census | mine |
  |---|---|---|
  | 5 | 0 | 0 |
  | 6 | 79,488 | 79,488 |
  | 7 | 302,316 | 302,316 |

  At T = 7 the two sorted pattern lists are identical (`cmp`).
- n = 11, m = 9: T = 7 gives 9,871,248 (round 1's value); T = 6 gives 0.

**R4. Main run at n = 12.**
- Command: `./enum 12 7 0 1 1` (`enum_n12_m10.log`). It took 217,509,329 nodes and 26 s.
- Output: `COUNT m=10 alpha<=T: f7free=2226490 f7=451592`.
- My sorted F7-free list and the sorted census file `results/n12_m10_all.jsonl.gz` are byte-identical:
  - sha256 prefix 1be572b9de4580e4 for both;
  - 2,226,490 distinct lines.

**R5. The α look-ahead is not needed.**
- `./enum 12 7 0 0 0` (no look-ahead; `enum_n12_m10_noprune.log`) gives 686,700,420 saturated linear K30 leaves. This matches round 1, and the α ≤ 7 counts are the same.
- `./enum 12 7 1 0 0` (`enum_n12_none1_noprune.log`) allows at most one non-midpoint. It gives 3,389,574,440 leaves and the same counts, with nothing at m = 9.

**R6. m ≤ 9, and f(12) ≥ 7, without Henning–Yeo or F7.**
- Command: `./enum 12 7 b 1 0` for b = 1, 2, 10 (`enum_n12_none1.log`, `enum_n12_none2.log`, `enum_n12_noneall.log`). Here b is the number of interior non-midpoints allowed; b = 10 covers every m.
- Result: in every run, every α ≤ 7 leaf has m = 10.
- Also, `./enum 12 6 10 1 0` gives 0 leaves (`enum_n12_T6_all.log`): no pattern at n = 12 has α ≤ 6.

**R7. Census engine re-run at the pinned commit.**
- m = 10: `./census_d2f70f5 n=12 T=7 m_min=10 m_exact=10 f7=1 mode=enum progress=0`.
  - Output: `DONE nodes=187004404 leaves=2226490 solutions=2226490 timed_out=0 time=329.06`.
  - The sorted output is identical to the stored file.
- m = 9: output `DONE nodes=425209182 leaves=2226490 solutions=0 timed_out=0 time=556.53` (`census_rerun_m9.txt`).
- Both node counts equal the README's.

**R8. Exact realization of all 2,678,082 saturated patterns with α ≤ 7, F7 included.**
- Command: `zcat my_n12_m10_all.txt.gz | ./realize` (`realize_all.log`).
- Output:
  ```
  lines=2678082 singular=0 certfail=0 order_infeasible=2441008 extra_ap=85218 not45=43370 realizable=108486 f7lines=451592 f7realizable=0 maxD=1008
  h_hist: 7:108486
  ```
- `compare_sets.py` then gives:
  - 54,243 distinct normalized sets, each arising from exactly {P, refl(P)};
  - 0 self-symmetric patterns;
  - theirs − mine = 0 and mine − theirs = 0, against `results/realized_n12.json.gz`, which I re-normalized myself;
  - all 54,243 of their labelled patterns are in my realizable list.
- Known sets. The patterns of `record_12`, omega 1 and omega 2 were computed from the sets by `known_patterns.py`. They realize back to the same normalized sets, and all three are present in both lists.

**R9. The Step 3 pipeline numbers.**
- `oprime_check.py`: my own medial-triangle (K31) test finds 754,235 K31-free patterns among the 1,113,245 canonical ones. It agrees with the census flag on all 1,113,245.
- The O′ subset (census flags k30 = k31 = c4 = 1) has 395,039 lines.
- `./realize` on O′ gives order-infeasible 321,304, extra AP 10,803, not (4,5) 8,689, realizable 54,243, exactly as in the text.
- The 54,243 O′-realizable patterns already cover all 54,243 classes. So on this data the K31 and core filters discarded no realizable pattern.

**R10. Reflection.** `refl_check.py` on the 2,226,490 patterns:
- the set is closed under i → 11 − i;
- 0 patterns are self-symmetric;
- 1,113,245 satisfy es ≤ refl(es). This matches "1,113,245 up to reflection".

**R11. Frozen judge.**
- `python3 judge/judge.py experiments/referee/L002-round2/spot/*.json`, on 25 random census sets plus the 3 known sets: **28/28** `PASS NO-IMPROVEMENT ... h=7 ratio=7/12`, exit 0.
- The census's own `results/judge_spotcheck.txt` shows 50/50 PASS.

**R12. Rigidity.**
- The proof's M-matrix argument is correct:
  - each row of B has at most two entries equal to 1/2;
  - iterating l(j) < j reaches 0, so every interior vertex has a path to a deficient row;
  - hence ρ(B) < 1 and 2(I − B) is nonsingular.
- Computationally:
  - 0 singular systems among the 2,678,082 patterns;
  - |det| ≤ 6^5 by Hadamard, so the floating-point determinant cannot round to the wrong integer;
  - every solution carries an exact integer certificate (0 certificate failures);
  - max |det| is 1008.

**R13. Housekeeping.**
- The pinned commits d2f70f5 and ea6c3d9 are ancestors of HEAD (`git merge-base --is-ancestor`).
- The proof file has the same md5 as in the round-1 revision commit; it was unchanged during this review.

## Problems (by severity)

**1. Step 3 misnames the realization oracle.**
- The text says: "Every one of the 395,039 remaining patterns is decided by `e757.realizability.realize_exact`".
- What the code does: `realize_all.py` calls `fastreal.realize_fast` first and falls back to `realize_exact` only when that returns None. `results/realize_summary.json` records `"n_fallback_to_realize_exact": 0`.
- So `realize_exact` decided none of these patterns. The census README states this correctly.
- The same error appears twice more: in "Computer-verified steps", which lists `e757/realizability.py` but not `fastreal.py`, and in the delegation note ("oracle e757/realizability.py").
- This is a provenance error, not a correctness error. `realize_fast` is an exact Fraction Gauss–Jordan solver, and its reason breakdown is reproduced exactly by two independent integer realizers (round 1, and R9 here).
- **Fix:** "decided by the exact Fraction solver `realize_fast` (experiments/20261014-1005-census-dfs/fastreal.py; same check order and failure labels as `e757.realizability.realize_exact`, which was never needed as a fallback)". Also list `fastreal.py` under Computer-verified steps.

**2. Step 2 attributes "0 for m≤8" to the census C DFS.**
- The census engine was run only with `m_exact=10` and `m_exact=9` (README; `m9/run_m9.sh`). The m = 9 run allows at most one non-midpoint, so it covers only m ≥ 9.
- The census README itself uses Henning–Yeo for m ≤ 8.
- The fact is true:
  - round 1 found 0 (`experiments/referee/L002/n12/mle8_runs.log`, 0 in all splits);
  - this round found 0 too (R6, `experiments/referee/L002-round2/enum_n12_noneall.log`, with F7 not assumed).

  But the sentence claims a run that does not exist, and Step 1 and DEPENDS ON lean on it ("so Henning–Yeo is not needed").
- **Fix:** "...for m = 9 it finds 0 patterns (425M nodes, 607 s). No pattern with m ≤ 8 has α ≤ 7 either: the independent enumerations of referee rounds 1 and 2 (experiments/referee/L002/n12/mle8_runs.log; experiments/referee/L002-round2/enum_n12_noneall.log, all m, F7 not assumed) find α ≤ 7 only at m = 10. Alternatively, Henning–Yeo gives m ≥ 9."

**3. Engine pin wording (cosmetic).**
- The stored census output predates d2f70f5: in the history, d2f70f5 comes after a887219 and 8c0b191. It was therefore produced from the ea6c3d9 source.
- d2f70f5 only adds inert options, and its build reproduces both runs exactly (R7). Pinning d2f70f5 is therefore acceptable.
- **Suggested wording:** "run with the ea6c3d9 source; reproduced identically with d2f70f5 (referee round 2)".

**4. DEPENDS ON omits K3 (cosmetic).**
- K3 is "(4,5) ⇒ weak Sidon" [published, Ma–Tang Props 2.1–2.2].
- K4 (stated "for weak Sidon A") and K5 both need it.

No mathematical problem was found. Every number in the certificate was reproduced.

## What is needed for ACCEPT

Text only: fixes 1 and 2 are required; fixes 3 and 4 are recommended. No new computation is needed. Checks R2–R12 of this review can be cited as the round-2 independent confirmation of completeness, realization and class count.
