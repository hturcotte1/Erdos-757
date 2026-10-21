# L015 prover work folder: the anonymous reader's 5/9 family, independent proof and verification

Certificate: `results/proofs/L015-reader-family-c-le-5-9.md` (TYPE: proof, `CLAIM: c* <= 5/9`; ACCEPTED by three referee rounds on 2026-10-20, K60; round 1 'ACCEPT WITH FIXES', rounds 2 and 3 ACCEPT. The computations in this folder predate the referee rounds, and its README was edited afterwards only for the round-1 editorial fixes. The construction itself remains the anonymous reader's, see Origin below).


**Origin.** The family $S_K=O\cup\varphi(O)\cup\dots\cup\varphi^K(O)$ with $O=\{0,49,75,83,98,101,117,119,121,159,269\}$ and
$\varphi(x)=101+18x/269$, the counts $|S_K|=11+9K$ and $h(S_K)=7+5K$, and the claim $c_*\le5/9$ are an anonymous reader's
(Erdős Problem a Day, reader submission 7bkzb8 of 17 Oct 2026, written up by the site on 19 Oct 2026, marked there
"Unreviewed by humans"): **[community]**, not ours. This folder holds an independent verification of every finite fact that the
certificate's proof uses, plus consistency checks: **[verified-here]** (exact integers and Fractions, Python standard library only).

## Question
Does the every-depth argument of the certificate (Steps 1-6) reduce the claim to finitely many facts, and do those facts hold?
Do independent computations (not using the proof's structure) agree with $|S_K|=11+9K$, $9(K+1)$ APs, the (4,5)-property and
$h(S_K)=7+5K$, and with the earlier rebuild in experiments/20261020-1730-reader-5-9/?

## Method and commands
All scripts were written for L015; none imports code from experiments/20261020-1730-reader-5-9/, e757/ or judge/. They read
data/reader_5_9_family.json, results/claims/C003-reader-5-9-K6.json and the agent's check_results.json / census_deep_results.json
only to compare numbers. `bash reproduce.sh` reruns everything (about 3 minutes wall on the shared machine, nice 10, one process).

| id | command (from this folder) | output | what it checks |
|---|---|---|---|
| C1 | `python3 -I v1_facts_O.py` | v1_facts_O_output.txt | facts F0-F6 (O, $\varphi$, $L$, $y(x)=251x-27169$, primality of 269, the nine APs of O and the absence of other relations, the residues mod 269 of the deepest-level cases $m=1,2,3$, the hits $\varphi^d(x')\in O$) - load-bearing |
| C2 | `python3 -I v2_transfer.py` | v2_transfer_output.txt | the 16-entry table best[s][s'] by two methods (AP-free bitmasks; Sidon by definition), M, $R_0$, $R_0\otimes M=R_0+5$, $U^*$ - load-bearing for the equalities (the upper bounds are also proved by hand in the certificate, Step 5.6) |
| C3 | `python3 -I v3_family.py 8 0 1 2 3 4 5 6 7 8 9 10 11 12 15 20 30 40 60` | v3_family_output.txt, v3_family_results.json | integer form = $269^K S_K$ (K<=8), equal to the agent's data and to C003; full relation census for 18 values of K up to 60; literal $\lvert B-B\rvert\ge11$ on all 4-subsets for K<=8 (1,837,620 subsets at K=8) - consistency |
| C4 | `python3 -I v4_h.py 20` | v4_h_output.txt | h by literal brute force from the Sidon definition (K=0,1) and by a generic exact solver for the AP hypergraph recomputed from sums (K<=20; alpha(H_AP) = h by Step 5.1 / Theorem 1(b)) - consistency |
| C5 | `python3 -I v5_witness.py 0 1 2 3 4 5 6 7 8 9 10 12 15 20 30 50` | v5_witness_output.txt | the explicit Sidon subsets $T_K=\bigcup_j\varphi^j(U^*)$, $U^*=\{0,98,101,117,119,159,269\}$: size $7+5K$, Sidon by definition, AP-free, self-similar |
| C6 | `python3 -I v6_compare.py` | v6_compare_output.txt | agreement with the agent's numbers (table, M, $R_0$; n, m, h for K<=8; census K<=30) |
| C7 | `python3 -I v7_controls.py` | v7_controls_output.txt | non-vacuity: a planted cross-copy point is detected by the census and fails the 4-subset test; the solver gives h(A_base)=8, h=7 for a 12-point record, and alpha_AP({1..9}) = 5 (the independence number of the 3-AP hypergraph, = r_3(9); not h: that set is not weak Sidon, its largest Sidon subset has 4 points) |

## Results (all exact)
- C1: `ALL FACTS OK` (53 checks). The nine APs of O are exactly {0,49,98}, {49,75,101}, {49,83,117}, {49,159,269}, {75,98,121},
  {75,117,159}, {83,101,119}, {83,121,159}, {117,119,121}; middles = the nine interior points; pairwise intersections <= 1; none
  contains both 0 and 269. Mod 269 over O° = O \ {0,269}: no x = 0, no x1+x2 = 0, and x_a+x_b = x_c only for (49,49,98), (159,159,49).
- C2: best = [[5,6,6,6],[5,6,6,6],[5,6,6,6],[6,7,7,7]] (rows: anchor state (0,0),(1,0),(0,1),(1,1); columns: inner state), identical by
  both methods; M = [[5,6,6,6],[4,5,5,5],[4,5,5,5],[4,5,5,5]], R_0 = [6,7,7,7], R_0 (x) M = [11,12,12,12] = R_0 + 5; 831 Sidon subsets of O.
- C3: for K = 0..12, 15, 20, 30, 40, 60: n = 11+9K, exactly 9(K+1) relations, all of them 3-AP relations, the AP set equals
  {phi^J(e)} exactly, no point pair in two APs, consecutive copies share exactly the two anchor points, other copies are disjoint,
  levels as in Step 1 of the certificate, level span of every AP <= 1; min |B-B| = 11 over all 4-subsets for every K <= 8.
  The K = 6 integer set equals the set of results/claims/C003-reader-5-9-K6.json; its stored 37-point witness is Sidon.
- C4: no 8-subset of S_0 and no 13-subset of S_1 is Sidon (165 and 77,520 subsets checked); the generic solver gives
  alpha(H_AP(S_K)) = 7+5K for every K = 0..20 (= h(S_K) by Step 5.1 / Theorem 1(b)).
- C5: T_K is a Sidon subset of S_K of size 7+5K for each K tested (up to K = 50, 461 points).
- C6: `ALL COMPARISONS AGREE`. C7: `ALL CONTROLS OK`.

## Conclusion
Every finite fact used by the certificate holds [verified-here], and all independent computations agree with the reader's
counts for the tested depths. The all-K statement itself rests on the proof in the certificate [derived-here, unrefereed], not on
these finite checks; C3-C7 are consistency checks.
