RESULT: NONE-FOUND

# Q8 falsification (omega inequality 7 tau(K) <= 3|R| + 2 e_2 + 4 e_1)

## Statement tested
For a (4,5)-set A (or any induced subset S of one, treated as its own (4,5)-set), D an independent set of H(S)
(no AP of S inside D), R = S \ D, K = clutter of inclusion-minimal (deduplicated) nonempty traces e \ D over APs e of S,
e_i = number of members of K of size i: `7*tau(K) <= 3*|R| + 2*e_2 + 4*e_1`.
Primary reading: |R| = |S \ D| (all non-avoided points, as in the note's counterexample 1). Stronger variant also tested:
|R| replaced by |union of K| ("active" vertices; <= |S\D|); violations of either are counted separately (violQ, violAct).
Sibling D4 (`21 tau <= 9|R| + 5 e_2 + 12 e_1`) is evaluated in the same pass as a sanity check.
Tags: [verified-here] for exact counts below; the NONE-FOUND verdict is [heuristic] evidence, not a proof.

## Implementation
`q8.c` (exact integer bitset code; tau by branch and bound with disjoint-packing bound and forbidden-vertex branching),
driver `q8lib.py`. All hypergraphs come from `e757.core.ap_edges` on exact integer sets. Validation:
`sanity.py` reproduces the D4 counterexample (12-pt set b, D={287}: tau=5, |R|=11, e_2=1, 105>104) and C reproduces
exactly the Python brute-force tau histograms for all D with |D|<=k on 12b and A_base (`validate.py`: identical
slack histograms for Q8 and D4). In the 3^12 enumeration of 12b, D4 is violated in exactly 1 state (D={287}).

## Scope and results (all numbers exact; "states" = (S,D) pairs evaluated)
| step | objects | states | Q8 violations | active-R variant violations | D4 violations | Q8 equalities |
|---|---|---|---|---|---|---|
| 1. ALL 3^n deletion/avoidance states (every induced subset S x every independent D) of A_base (n=14), 12pt#1 (omega 9804 #1; = the 12-pt set 0..575 here), 12b, 12c, and the n=8,10,11 records | 7 sets | 3,253,568 (A_base; matches omega's count) + 385,408 + 384,960 + 384,960 + 136,416 + 45,488 + 5,536 | 0 | 0 | 12-pt: 10, 1, 1 (n=8,10,11,14: 0) | A_base 94,544 |
| 2a. random saturated (4,5)-sets, exact (`anneal.random_linear_map` + exact solve + exact (4,5) check), n=12/14/16, 300 each: D over all indep. sets |D|<=3 (S=full) + 2000 random (S,D) per set; n=12 also full 3^12 | 900 sets | 116.5M (n=12), 0.74M (14), 0.80M (16) | 0 | 0 | 148 (n=12), 0 | 5.5M / 0.28M / 0.27M |
| 2b. adversarial pool: 6000/8000/12000 random saturated sets at n=12/14/16 ranked by D=empty slack then #low-slack states; top 300 per n; same battery; n=12 full 3^12; n=14 first 100 sets full 3^14 | 900 sets | 116.4M, 327.7M, 0.80M | 0 | 0 | 198 / 137 / 1 | 5.5M / 9.2M / 0.28M |
| 3a. generic gluings of {A_base, 12a, 12b, 12c}: all 16 disjoint unions (shift t=10^6+17, q=4099) and 736 one-vertex amalgams (all vertex pairs x two orientations/scales q in +-{4099,8209,12007}; kept iff exactly (4,5) with no cross APs, n<=25), D over indep. sets |D|<=3 plus 5000 random (S,D) each | 752 sets | 1.77M + 3.76M | 0 | 0 | 239+188 | 40 + 1.7M |
| 3b. random 3-piece amalgam trees (pieces from 8,10,11,12a,12b,12c records, <=31 points, exact (4,5) check), 20000 random (S,D) each | 300 sets | 6.0M | 0 | 0 | 11 | 2.7M |

Minimum slack (rhs - lhs of Q8) is 0 in every row: no negative value anywhere. No counterexample; `counterexamples.json` is `[]`.

## Tightness / distribution [verified-here]
- Q8 slack histograms (full) are in `step*_results.json` (key `hist_lowest`, and per-set in `step1_results.json['hist']`).
  A_base, all 3,253,568 states: slack 0: 94,544; 1: 131,346; 2: 84,128; 3: 305,817; 4: 311,463; 5: 175,228 ...
  (12-pt sets: slack 0 in 17,739 / 17,903 / 17,903 of ~385k states.)
- Equality configurations with S = whole set (`eqstates.py`, `eqstates_results.json`; exhaustive over all 2^n independent D):
  - A_base: 165 equality D's out of 4,855 independent D's: D=empty (tau=6, 7*6=42=3*14), 21 of size 7, 143 of size 8.
  - Each 12-point set: equality at a single avoided point D={p} (tau=5, e_1=0, e_2=1, |R|=11: 35=35):
    D={0} for 12-pt#1 (0..575 set), D={287} for 12b, D={-336} for 12c; also at |D|=6,7 (and D of size 3 for 12-pt#1). With D=empty slack is 1.
  - So the n=14 record is Q8-tight with no avoidance (D=empty Q8 is exactly tau <= 3n/7, the 4/7 conjecture), and the n=12 records become tight after avoiding one point.
- Note on D=empty: Q8 with D=empty reads h >= 4n/7, i.e. a Q8 counterexample with D=empty is exactly a (4,5)-set beating 4/7;
  the random pools at n=16 (12000 sets) had min D=empty slack 6 (tau=6, h=10), none with h=9. Q8 for general D is the stronger inductive form.
- The 3,253,568 valid-state count for A_base agrees with the omega note, but the note's 99,153 equality states vs our 94,544 differs;
  the note's convention for equality/|R| is not specified (possibly counts differently); not investigated, no violation either way.

## Honest limits
- NONE-FOUND is evidence, not proof. The exhaustive part covers only the 7 known extremal sets (all 3^n states each); the random parts
  cover saturated sets with n<=16, whose h is generally well above the record (random sets are far from tight; the adversarial
  ranking only partly addresses this), and gluings of at most 3 known pieces up to 31 points (uint32 bitsets; larger
  amalgams like the note's A_k with k>=3 of 12-pt pieces, 34 points, were not run).
- Abstract (non-realizable) linear F7-free hypergraphs (procedure item 5) were not enumerated, so nothing here says Q8 holds for them.
- Isolated points of S (in no AP) count in |R|(full) which only weakens the primary inequality; the active-R variant removes this and also has 0 violations.
- Non-saturated and fully random (4,5)-sets have few APs and were not sampled.
- Disjoint unions are additive for Q8 (tau, |R|, e_i all additive), so only amalgams are informative; they were tested in 3a/3b.

## Files
q8.c (core), q8lib.py, sanity.py, validate.py, gen_random.py, adv_pool.py, step1.py, step2.py, step3.py, step3b.py, eqstates.py;
data: step1_results.json, step2_results.json, step2_adv_results.json, step3_results.json, step3b_results.json, eqstates_results.json,
random_sets.json, adv_sets.json, counterexamples.json (empty).
Reproduce: `gcc -O2 -o q8 q8.c; python3 step1.py; python3 gen_random.py; python3 step2.py random_sets.json step2; python3 adv_pool.py; python3 step2.py adv_sets.json step2_adv; python3 step3.py; python3 step3b.py; python3 eqstates.py`
(note: violation text lines in step1-3 outputs were lost to a parser ordering bug, fixed in q8lib.py afterwards; all violation COUNTS were 0, taken from the C counters, so nothing was lost.)
