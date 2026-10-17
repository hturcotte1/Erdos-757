# Hunt: realizable extremal 15-point sets and their one-point extensions (n = 16 record search via Lemma Delta)

Question. A 16-point record C (h = 9) is a one-point extension of an extremal 15-point set B = C - p with 9 <= m(B) <= 12
(kb/notes/extension_lemmas.md, Lemma Delta) [derived-here]. Collect many realizable such B (class-O DFS patterns at (15, alpha <= 9, m)
that realize exactly) and test all one-point extensions of each.

## Method (hunt.py; stats.py summarises)
1. Producer (`hunt.py dfs`): random descent in the prefix tree of e757/c/ordered_dfs (depth-3 prefix from `list_prefixes`, then
   `mode=prefixes depth=d pre=...` children to depth 5-7, keeping only children whose partial AP system passes a float LP order-feasibility
   test), then `mode=enum pre=<prefix> refl=1` with per-run time limit (m=12: 10 s, m=11: 20 s, m=9/10: 60 s). Round robin m = 12,11,12,11,...,9,10.
   At most 100 (m=12) / 300 (m=11) random patterns kept per prefix. 70% of the descents restart from depth-5 prefixes that earlier produced
   realizable patterns (productive-prefix pool). [heuristic selection; every kept set is exact]
   (The first design, plain depth-3 prefixes with 30 s windows, gave ~0 realizable patterns: realizable patterns are concentrated in few prefixes.)
2. Consumer (`hunt.py work`): dedupe by canonical pattern (min of pattern and its reflection); float-LP prefilter (patterns it calls infeasible
   are skipped: heuristic, counted separately); exact `e757.realizability.realize_exact`; then exact checks on the integer set (translated to 0,
   divided by the gcd): `is_45_set`, AP set equals the pattern, alpha = 9 by enumerating all 3-AP-free subsets.
3. Extension test per B, all exact integer arithmetic (set doubled so midpoints are integers):
   (a) the task's test: candidates x = every point forming a 3-AP with two points of B, x not in B; keep x iff B+x is a (4,5)-set
       (only 4-sets through x need checking); h(B+x) = 9 iff every maximum Sidon 9-subset of B contains a pair {a,b} with {x,a,b} an AP, else 10.
   (b) abstract (realization-independent) test, stronger: a record extension needs a set G of deg(x) <= 14 - m pairs of B covering all maximum
       Sidon 9-subsets (each contains a pair of G). We enumerate all minimal covers of size <= 14 - m (branching on the first uncovered subset),
       and for each cover G and each of the 16 rank positions of x build the 16-point labelled pattern (B's edges + one edge per pair; the role of x
       is determined by its position), prefilter (midpoint-injective, linear), then `realize_exact` at n = 16. Any realized C with h <= 9 is a record
       (would be saved to RECORD_CANDIDATE.json and passed to scripts/new_claim.py automatically; none occurred).
   Caveat on (a): a generic realization of B creates only deg-1 extensions; extensions with deg(x) >= 2 need special B. That is what test (b) covers
   (it quantifies over all realizations of the pattern of B, not only the one found).
4. Judge: `python3 scripts/new_claim.py --slug ext15-m11-example|ext15-m12-example --set <first m=11 / m=12 set in data>` (judge_lines.txt).

## Commands (repo root)
`bash scripts/start_job.sh experiments/20261017-0210-ext15-hunt/jobs_dfs 3 nice -n 5 env PYTHONPATH=. python3 experiments/20261017-0210-ext15-hunt/hunt.py dfs 2.2 33 6`
(earlier DFS runs: seeds 1 (depth-3 version), 7 (D=8), 21 (D=8 + pool); the final one above, seed 33, D=6) and
`... jobs_work ... hunt.py work 2.5`; `PYTHONPATH=. python3 experiments/20261017-0210-ext15-hunt/stats.py` -> results.json.
Wall time 02:10-04:56 UTC on a machine at load ~9-11 (nice 5, 2 processes); the worker used ~10 CPU-min, the producer's Python ~2 CPU-min plus short C runs.
The producer script was changed 4 times during the run (see above); all logs in jobs_dfs/run.log, jobs_work/run.log; raw pattern files in data/pats_raw.tar.gz;
per-file attempt counts in data/attempts.jsonl.

## Results [verified-here: every listed set is exactly realized and checked; counts of patterns are heuristic samples]
Sets: data/ext15_sets.jsonl.gz, one JSON per line: set (primitive integers, up to 53 bits), edges (rank triples), m, deg_seq, n_max_sidon, universal,
n_ext_admissible, ext_degx_dist, min_h_ext, cover_min, n_min_covers, covers, cover_ext. 2337 distinct patterns (distinct up to reflection; each is a
positive-dimensional family, we keep one random point), all with h = alpha = 9 = f(15), all (4,5)-sets.

| m | realizable sets | patterns tested (DFS output sample) | realizable fraction | max degree 3 / 4 / 5 | #max Sidon 9-sets (min/med/max) | universal vertex |
|---|---|---|---|---|---|---|
| 12 | 1589 | 33,401 | 4.8% | 780 / 799 / 10 | 82 / 115 / 156 | none |
| 11 | 748 | 5,736 | 13.0% | 520 / 228 / 0 | 136 / 157 / 189 | none |
| 10 | 0 | 0 patterns found (3 descents only) | | | | |
| 9 | 0 | 0 patterns found (3 descents only) | | | | |

Failure reasons (tested patterns): m=12: order-infeasible 31,073 (4,939 exact + 26,134 by the float prefilter), forced repeated difference 394,
forced extra AP 345; m=11: order-infeasible 4,783, forced extra AP 110, forced repeated difference 95. m=9,10: the 3 + 3 descents ended in subtrees with no
pattern; this is NOT evidence about the cells (probe README: the cells are far from exhausted).
Degree sequences: most common m=12: (3^7,2^7,1) 494 sets, (4,3^5,2^8,1) 484; m=11: (3^4,2^10,1) 281, (4,3^2,2^11,1) 162. Distinct degree sequences: 19 (m=12), 11 (m=11).

One-point extensions:
- (a) every B has 63-109 admissible single-point extensions (min/med/max: m=12 63/81/92; m=11 84/102/109); in all of them deg(x) = 1 and h(B+x) = 10.
  Minimum h over extensions: 10 for all 2337 sets. **No record.**
- (b) m = 12: for none of the 1589 patterns is there a pair set G with |G| <= 2 covering all maximum Sidon 9-subsets, so no 16-point (4,5)-set
  C = B + x with m(C) <= 14 and h(C) = 9 exists for ANY realization of these patterns (given Lemma Delta's m(C) <= n - 2 = 14).
  m = 11: all 748 patterns have covers of size exactly 3 (minimal covers per pattern 1 to 17, the 50-cap never reached), 88,816 labelled 16-point
  patterns (cover x position) were built; **every one fails midpoint-injectivity or linearity**, so 0 reach realize_exact. (Reason: m(C) = 14 needs
  3 new midpoints, available only among x and the two interior non-midpoints of B, plus the old extreme if x is the new extreme.)
  Hence none of the 2337 collected B is the 15-point subset of a record, for any realization. [verified-here for these patterns; the premise m(C) <= 14 is the
  published midpoint-injectivity fact; the cover argument is elementary but not referee-reviewed]
- Universal vertices (in every max Sidon 9-subset): none in 2337 sets, consistent with Lemma U.
- Judge examples (judge_lines.txt; results/claims/C001, C002): the first m=11 set and first m=12 set in the data:
  `JUDGE: PASS NO-IMPROVEMENT C001-ext15-m11-example n=15 h=9 ratio=3/5 (0.600000) vs 4/7=0.571429`
  `JUDGE: PASS NO-IMPROVEMENT C002-ext15-m12-example n=15 h=9 ratio=3/5 (0.600000) vs 4/7=0.571429`
  This is the exact verification of K50: non-saturated extremal 15-point (4,5)-sets exist (m = 11 and m = 12).

## Conclusion / caveats
Extremal 15-point sets with m = 11, 12 are plentiful (>= 2337 patterns found in ~2.7 h of niced wall time; the supply was not exhausted: ~100-250 new
sets per 10 minutes at the end), but none extends to a 16-point record, and for m=12 and m=11 this is explained combinatorially (no small cover / midpoint
injectivity). The sample is non-uniform (DFS output near productive prefixes), so it says nothing about the full cell counts. m = 9, 10 were not explored in
any meaningful way here. The float-LP prefilter may have discarded a few feasible patterns (heuristic loss only).
Data not committed (instruction). Next step: apply test (b) as a DFS prune/necessary condition: a 15-point B can be part of a record only if some
<= (14 - m)-pair set covers all its maximum Sidon 9-subsets and survives the midpoint count; for m=12 even the cover step already fails on 1589/1589.
