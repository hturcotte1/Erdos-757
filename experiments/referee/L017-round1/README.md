# Referee L017, round 1: scratch folder (independent checks)

Question: is certificate results/proofs/L017-i11-minimal-counterexample-structure.md correct?
All code here is the referee's own (no import of e757 or of the prover's hyp.py); nauty geng/genbg (unmodified,
experiments/referee/L013-round2/out/nauty_build/) are used only as generators.  cells/ holds the refereed tarballs
of L012/L013/L014/L016 extracted afresh (git-ignored).

| file | what | result |
|---|---|---|
| list_cells.py -> cell_inventory.json | own parser of all stored cell lists | 159 (n,m,t) keys |
| cells_slack01.py | tight / slack-1 connected cells n<=30 and stored Delta<=3 counts | matches 13.1 and the proof of 13.3 (483 = 13 + 470) |
| src/cotrans.c, validate_cotrans.py | tau and co-transversality of vertices/pairs via Fact 0.4 (decision B&B) | 0 mismatches vs brute force on 400 random linear 3-graphs |
| roles.py -> roles_output.json | role_b/c/e/f1/f2 of Theorem 4(iv) on the 483 Delta<=3 classes | identical to C5 |
| remark132.py | Remark 13.2 on the Delta<=4 lists | 24,151 / 199,524 predictions, 0 failures; types as stated; (P) fails for E1 |
| patterns.py | Hall-deficient distributions of the six co-vertices | exactly 7 orbits (r=1:1, r=2:5, r=3:1, r>=4:0) |
| src/nu_subcubic.c | 11 nu >= 3M on all subcubic graphs 2<=N<=14 (geng -D3) | 0 violations; min positive 11nu-3M = 1 (K4 with subdivided edge); min nu/M = 2/7 |
| src/thm7.c -> thm7_output.txt | Theorem 7 on all connected linear Delta<=2 3-graphs, n<=21 (genbg) | 12,101 graphs, tau = m - nu(G) always, slack >= 1 for m >= 2 |
| src/vcrit.c, src/vcrit2.c -> vcrit_*.txt | all linear vertex-critical violators: n<=11 (all degrees), n=12,13,14 (Delta<=3) | n<=11: F7 + two (9,8,4); n=13: five 3-regular (13,13,6); none at 12, 14 |
| check_theorems.py | conclusions of Theorems 1(a)-(f), 3, 4, 5 on those 8 violators | 4,223 checks, 0 failures |
| f7_check.py | F7-containment and (P3) of the 8 violators | F7 satisfies (P3); the others are F7-free and violate (P3) only at S=V |
| test_iv.py -> test_iv_output.txt | random test of Theorem 4(iv) equivalences (direct tau(H) vs pattern condition) | 4,097 deficient + 1,154 non-deficient configurations, 0 mismatches |
| decomps.py | engine decompositions of the 17 top cells, (28,24) slack 0 | identical to C4 (64 / 19 / 11 / 208; 864, 16, 8, 952, 334) |
| abase_check.py | Sanity checks on A_base | (14,12,6), s=0, every vertex co-transversal; A_base - 0 = E1 + (10,7), s=0 |
| rerun/ | prover's C1, C2, C4, C5, C6, C8, C9 re-run read-only (PYTHONDONTWRITEBYTECODE=1) | identical outputs (C2 differs only in timings) |
