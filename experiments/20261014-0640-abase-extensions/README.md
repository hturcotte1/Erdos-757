# Exact re-verification of K13: 2-point extensions of A_base  [verified-here]

Question: for distinct reals x, y with B = A_base u {x,y} a (4,5)-set, is h(B) = 10 always?
(A_base = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}, h = 8.)
A counterexample (h(B) <= 9) would be a 16-point (4,5)-set with ratio 9/16 < 4/7.

Command: `python3 extend.py` (about 30 s, no randomness) -> `results.json`;
`python3 bruteforce_check.py` (independent completeness check, ~1 h, log in `brute.log`).

## Method (all arithmetic in `fractions.Fraction`)
Upper bound h(B) <= 10 is trivial (deleting x,y from a Sidon set of B leaves a Sidon set of A, so h(B) <= h(A)+2).
Since B is (4,5) it is weak Sidon, so h(B) = alpha(AP hypergraph) (Ma-Tang Lemma 2.3); `e757.core.alpha` is used.
Every pair {x,y} (x,y not in A, x != y) falls in exactly one of these classes, by which APs of B involve x or y:

* **T0/T3.** Neither x nor y lies in any AP of B. Then H(B) = H(A) plus two isolated vertices, h = 8+2 = 10.
* **T1.** At least one new point lies in P_x = {(a+b)/2, 2a-b : a,b in A} \ A (223 values; 50 give a (4,5)-set A u {x}). Say x in P_x
  (all unordered pairs are enumerated, deduplicated by frozenset).
  * T1a: y in no AP of A u {x}: h(B) = h(A u {x}) + 1, computed exactly for all 50 admissible x (all = 10; h(A u {x}) = 9 each).
  * T1b: y in P_y(x) = all midpoints/endpoint-extensions of pairs of A u {x} (finite). 11,774 unordered candidate pairs;
    A u {y} and the 91 quadruples containing both x,y are tested exactly; 1,743 are (4,5)-sets; h via `alpha` is 10 in every case.
    Each of the 1,743 also has an explicit Sidon (checked by `is_sidon`) 10-subset (`witness_certified` = 1743).
* **T2.** Neither x nor y is in P_x, but some AP {a,x,y} exists (a in A in one of three roles: y=2x-a, y=(x+a)/2, y=2a-x; 42 lines).
  Any further AP in B must again contain both x and y (else x or y is in P_x), hence gives a second line.
  * generic point of a line: H(B) = H(A) + one edge {a,x,y}. alpha of this 16-vertex hypergraph (`saturated.alpha_of_edges`)
    is 10 for all 42 lines (14 values of a x 3 roles). Hence any (4,5) point on a generic line has h = 10.
  * exceptional points: points lying on two distinct non-parallel lines (498 intersection points, pairs with x,y not in A, x != y);
    parallel lines never meet, and distinct (role,a) give distinct lines. Each is tested exactly: none is a (4,5)-set
    (`type2_isect_45` = 0). (Points where a coordinate lies in P_x are T1.)

## Results (results.json) 
* Exact finite extensions checked: 11,774 (T1b candidates) + 498 (T2 intersections) + 50 (T1a families) + 42 line-families.
* (4,5)-sets among finite pairs: 1,743 (plus 50 T1a one-parameter families with y generic, plus the line families).
* Distribution of h: {10: 1,793} (1,743 + 50); all 42 line hypergraphs alpha = 10. No extension has h <= 9, so no record candidate.
* Comparison with omega #9804 (124 compatible triples, 6,484 pairs, 6,609 extensions): their counting convention is not stated
  in our digest, so the numbers cannot be matched; ours are unordered pairs {x,y} up to the generic families above.
  The conclusion (h = 10 always) agrees. Not reconciled: [heuristic] omega probably counts ordered pairs / includes generic families.

## Conclusion
K13 re-derived with exact computation: every (4,5)-set A_base u {x,y} has h = 10 [verified-here], subject to the case
analysis above (referee should check completeness of the classification; `bruteforce_check.py` is an independent
sanity test over half-integers in [-60,1120]).
Test: `tests/test_abase_extensions.py` (50 sampled stored extensions: exact (4,5), alpha = 10).

## Independent brute-force completeness check (brute.log, ~50 min) [verified-here]
All unordered pairs of half-integers in [-60,1120] with A u {v} (4,5): 1,781 values. Among exact (4,5) pairs, 589 have both points
in some AP and are not generic points of a T2 line: all 589 are in the stored set (0 missing). A further 6,287 (4,5) pairs
are generic line points (exactly one new AP {a,x,y}); a 1/500 sample all had Sidon 10-subsets (no failure printed).
(Note: 6,287 line-generic pairs is the same order as omega's 6,484 "pairs"; their count likely includes such pairs.)

## Referee round 1 fixes (supersedes the brute-force paragraph above) [verified-here]
* `witnesses.json`: explicit 3-AP-free (hence Sidon) 10-subset for each of the 1,743 (4,5) extension pairs, and a 3-AP-free 9-subset of A u {x} for each of the 50 generic-y cases (add y). `tests/test_abase_extensions.py` checks 50 stored 10-sets directly (10 points, subset of A u {x,y}, no a+b=2q) and all 50 S9.
* `bruteforce_check.py` rewritten: no e757/extend.py imports, plain integers (coordinates doubled), window = half-integers in [-300,1699.5]
  (3,305 valid singles, 5,185,660 (4,5) pairs). It finds a checked 3-AP-free + Sidon 10-subset for EVERY (4,5) pair (0 failures; also asserts h(A)=8 exhaustively),
  all 15,800 line-generic pairs included. 16,566 window pairs have both points in 3-APs with points of A; of these 15,800 are
  line-generic (exactly one new AP {a,x,y}) and 766 are NON-line-generic. Lookup in results.json uses exact Fraction keys
  (round 2 fix; an earlier version used int(2*F(a)), which truncated quarter-integer values and gave a wrong stored count of 1,734).
  Result: stored pairs 1,743 (all keys distinct), of which 766 lie in the window; all 766 were found by the brute force and
  all 766 non-line-generic pairs are stored (0 missing, 0 stored-in-window unmatched). The other 977 stored pairs have a
  coordinate outside the window or a non-half-integer coordinate. Runtime 5.7 min (`brute.log`).
