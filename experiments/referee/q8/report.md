VERIFICATION: CONFIRMED

# Independent recheck of Q8 falsification (referee, 2026-10-14)
Own code only (check.py: plain Python ints, exact (4,5)-test, AP bitmasks, brute-force tau by increasing size; sweep.c: my own C
sweep, tau by brute force over k-subsets of R in increasing k, minimal-trace clutter dedup). No e757, no falsifier code or binary.
Earlier partial file indep_check.py (called the falsifier binary) was deleted. Outputs: sweep_base.out, step3.out, step4.out.
Tags: [verified-here] for counts; NONE-FOUND itself remains [heuristic] evidence.

## 1. D4 sanity (check.py step1)
12b = {0,178,...,436}, D={287}: tau=5, |R|=11, e_2=1, e_1=0; D4: 105 > 104 (violated); Q8: 35 <= 35 (holds, equality). 10 APs.

## 2. A_base, all 3^14 states (S, D indep in H(S), D subset S)
| quantity | mine | falsifier |
|---|---|---|
| valid states | 3,253,568 | 3,253,568 |
| Q8 violations | 0 | 0 |
| Q8 equality states (|R| = full S\D) | 94,544 | 94,544 |
| D4 violations | 0 | 0 |
| slack hist 0..5 | 94544,131346,84128,305817,311463,175228 | identical |
Runtime 2 s. 326 sampled states (stride 9973) cross-checked against pure-Python brute force: 0 mismatches.
Omega note's 99,153 "equality states" is not reproduced by either of us (convention unknown); irrelevant to violations.

## 3. Extra full 3^n sweeps (all agree with falsifier's step1 where it reports)
n=8: 5,536 valid; n=10: 45,488; n=11: 136,416; 12-pt #1 (=0..575 set): 385,408 (D4 viol 10); 12b: 384,960 (D4 viol 1); 12c: 384,960 (D4 viol 1).
Q8 violations 0 everywhere; equality 600 / 3,449 / 7,022 / 17,739 / 17,903 / 17,903.
Beyond their report: 20 sets from their random_sets.json / adv_sets.json (4 each of n=12,14 and 2 of n=16, random and adversarial pools):
all 20 are exact (4,5)-sets, distinct points, saturated (m = n-2). Full 3^n sweep on the 16 with n<=14 (3^12/3^14) and on two n=16 sets
(3^16 = 43M states; ~27.6M valid, 38 s each): 0 Q8 violations in all. (D4 does get violated on some of these, 2/4/48, consistent with D4 being refuted.)

## 4. Verdict on scope statement
The report's claims (exhaustive on 7 known sets, random/adversarial saturated n<=16, gluings <=31 points, nothing about abstract
hypergraphs or A_k with k>=3, NONE-FOUND = heuristic) are honest as far as I could check; I did not re-run its gluing steps 3a/3b
or the non-exhaustive step 2 parts. Caveat: its note that "random sets are far from tight" is right: evidence is strongest at the tight sets.

## 5. D empty reading
D = empty, S = A: R = A, traces are the APs (size 3; distinct APs of a linear hypergraph are never nested, so K = H, e_1=e_2=0),
so Q8 reads 7 tau(H) <= 3n, tau = n - h, i.e. h >= 4n/7. Hence Q8 restricted to D empty (for all induced subsets S too, which are
(4,5)-sets themselves) is exactly the conjecture c* = 4/7 in the strong form f(n) >= 4n/7 for every n; a Q8 counterexample with D empty is
a (4,5)-set beating 4/7. Q8 for general D is an inductive strengthening of it (A_base is tight: 7*6 = 42 = 3*14).
Note this means proving Q8 would prove c* = 4/7 (closing the problem), so Q8 is at least as hard as the full conjecture.
