# 2-point extensions of all 2,910 saturated extremal 14-point (4,5)-sets  [verified-here]

Question: for each class A in data/census_n14_m12_classes.jsonl.gz (n=14, m=12, h=8), is there a
(4,5)-set B = A u {x,y} (x,y real, not in A) with h(B) <= 9? Such a B would be a 16-point record (9/16 < 4/7).

Method: exactly the case analysis T0/T1a/T1b/T2 of results/proofs/L001-abase-two-point-extensions.md,
generalised from experiments/20261014-0640-abase-extensions/extend.py. Per class:
- A is scaled by 4, so every T1 candidate (midpoints/endpoints of pairs of A u {x}, x in P_x) is an integer (asserted); T2 intersection
  points use Fractions scaled to a common denominator. All checks are integer/Fraction arithmetic.
- h(A)=8 recomputed (all 2,910 classes), all maximum 3-AP-free 8-subsets enumerated: their number and the points lying in all of them (T2 pre-check).
- T1a: h(A u x)+1 for every admissible single extension x (A u x a (4,5)-set). T1b: all candidate pairs {x,y}; (4,5) tested exactly
  on every 4-set containing x or y; for each (4,5) pair a 3-AP-free (checked Sidon) 10-subset is searched (h<=10 is trivial); if none, exact alpha.
- T2: 42 lines (14 points x 3 roles), hypergraph H(A)+{a,x,y} on 16 vertices, 10-subset searched (else exact alpha);
  the pairwise line-intersection points are tested exactly for (4,5) and, if (4,5) and not already in T1, h computed.
- Any h<=9 would be written to RECORD_CANDIDATES.txt (none was).

Command: `bash scripts/start_job.sh experiments/20261015-2340-ext14-all 4 python3 experiments/20261015-2340-ext14-all/extend_all.py data/census_n14_m12_classes.jsonl.gz experiments/20261015-2340-ext14-all 2`
(nice 15; no randomness). A_base test: `python3 extend_all.py x x 1 --abase-test` (1.2 s).
Runtime: 1844 s wall clock with 2 processes (about 1.0 CPU-hour).

## Acceptance (A_base)
Output on {0,136,...,1056}: |P_x|=223, 50 single (4,5) extensions, 11,774 T1 pairs, 1,743 (4,5) T1b pairs all with h=10,
42 T2 lines all alpha=10, 498 T2 intersection points, 0 of them (4,5), 143 maximum Sidon subsets: matches L001 exactly.
The same numbers appear in the census class with index 2440 (found by its numbers) of results.json.

## Results (results.json; per-class rows also in results.jsonl)
- Classes processed: 2,910 (all fully through T1a, T1b, T2); h(A)=8 for all.
- Single (4,5) extensions: 141,153 in total (32 to 61 per class). (4,5) 2-point extensions in T1b/T2-intersections: 4,970,208 total (854 to 2,496 per class).
- min h over all extensions (T1a/T1b/T2): 10 for every class. Histogram {10: 2910}. Classes with h<=9: 0. No record candidates.
- All 2,910*42 T2 line hypergraphs have alpha = 10; no T2 line-intersection point is a (4,5)-set in any class.
- T2 pre-check (a point of A lying in all maximum Sidon subsets): false for every class (0/2910); number of maximum Sidon subsets ranges 137 to 150.

## Conclusion
For every one of the 2,910 saturated extremal 14-point classes, every (4,5) two-point extension has h = 10 (ratio 5/8).
No 16-point (4,5)-set contains a saturated extremal 14-point set with h <= 9. [verified-here] (subject to the L001 case analysis;
this does not cover extensions by 4+ points, nor non-saturated 14-point sets with h=8, Q11.)
