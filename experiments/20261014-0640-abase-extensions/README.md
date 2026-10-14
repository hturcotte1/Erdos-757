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
