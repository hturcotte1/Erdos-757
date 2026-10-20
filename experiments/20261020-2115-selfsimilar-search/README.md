# Self-similar (4,5)-families beyond the reader's 5/9 family

**Question.** Is there a seed O (a (4,5)-set, n0 points) and an affine map phi with phi(a)=a', phi(b)=b' (a,b,a',b' in O) such that S_K = O u phi(O) u ... u phi^K(O) is a (4,5)-set, |S_K| = n0+(n0-2)K, and h(S_K) = h0 + gK with g/(n0-2) < 5/9 (the reader's family K59/K60 has n0=11, g=5)?

## Method [verified-here unless tagged]
* Seeds (dump_seeds.py; normalised, deduped up to affine maps and reflection): n0=12: all 54,243 extremal classes; n14: all 2,910 extremal classes; n15: the 2,337 sampled non-saturated extremal sets of K50 (one realisation each); n13: 40,163 deletions of one point from the 14-point classes (all have h=8=f(13)); n11: reader's O + small_records + 640,905 deletions of a point from 12-point classes (h=7=f(11)). C22/C23 and near-extremal seeds were NOT used.
* Maps: every a<b, every ordered a',b' (either orientation, so r may be negative) with |r|=|b'-a'|/(b-a)<1. Type T0: {a',b'} disjoint from {a,b} (the clean two-shared-point chain); T1: hub (a'=a or b'=b, one point common to all copies); T2: other overlaps (counted, never useful; the transfer matrix was checked against CP-SAT only for K<=2 there).
* Structure filter (filt.c, mod P=2^61-1, conservative: equal over Q => equal mod P; survivors re-verified exactly): for K=1,2,3, |S_K| = n0+(n0-2)K, all pair sums x_i+x_j (i<j) distinct, number of 3-APs = (K+1)m0 (no cross-copy AP), no two APs share two points. That is exactly "(4,5) + APs are the copies' APs" (weak Sidon + linear <=> (4,5)). Validated against exact Fraction code (ss_lib.structure_check) on 10,890 maps of 4 seeds: 0 mismatches, 504 survivors, same slopes (validate_filter.py, validate_T1T2.py).
* Growth: 4x4 max-plus transfer matrix (best(s,s') over 3-AP-free U in O by anchor/exit state, M=best-|s|), slope = (max R_240 - max R_120)/120 exact; reproduces the L015 table, R_K = 7,12,17,... for the reader's (ss_lib.transfer, `verified_examples.json`).
* filt2 = filt with the (combinatorial, geometry-independent) slope computed first and maps pruned if g/(n0-2) > 2/3 (n13, n15) or > 5/9 (n11 sample).
* filt1: one shared point, generic r (random residues mod P; two draws), 2x2 transfer, ratio g/(n0-1). filt3: period-2 words (m1,m2) on one seed: copy j has anchors of m_j and exits of m_{j+1}; growth = cycle mean of M1 (x) M2 over 2; relaxed (each map only K=1-valid; any hit would need exact geometry check).

## Commands
`python3 dump_seeds.py`; `gcc -O2 -o filt filt.c` (same for filt1/2/3); `./run_all.sh` (n12 two parts, n14; n13/n15 full runs were stopped and replaced by) `PRUNE_NUM=6 ./filt2 seeds_n13.txt 3 P 2`, `PRUNE_NUM=6 ./filt2 seeds_n15.txt 3 P 2`; `./filt1 seeds_nXX.txt 3 0 1 11`; `./filt3 seeds_n14.txt 0 1 5`; `python3 aggregate.py`; exact checks `verify_hits.py`. All with nice -n 10, timeouts, <=2 processes. No randomness except filt1's xorshift seed 11.

## Results (results.json has the full slope histograms)
| scan | seeds | survivors (K<=3) | min g | min limit | below 5/9 |
|---|---|---|---|---|---|
| 2-pt chain n0=12, T0/T1/T2 | 54,243 | 6.48M / 0.69M / 1.05M | 6 | 3/5 | 0 |
| 2-pt chain n0=14 | 2,910 | 538k / 48k / 72k | 7 (T0) | 7/12 | 0 |
| 2-pt chain n0=13 (slope-pruned) | 40,163 | 47.5M x2 parts pass slope<=2/3 | 20/3 | 0.606 | 0 |
| 2-pt chain n0=15 (slope-pruned, sampled seeds) | 2,337 | 5.8M x2 | 23/3 | 0.590 | 0 |
| 2-pt chain n0=11 (every 20th derived seed, PRUNE g<=5) | 32,046 | 72 quadruples pass slope<=5/9 (11 K<=3-valid) | 5 | 5/9 | 0 (11 ties) |
| reader's O (n0=11) | 1 | 128 T0 (2 with g=5) | 5 | 5/9 | 0 (tie) |
| 1-pt generic chain n0=12/13/14/15 | all | -- | 6.5 / 7.5 / 8 / 8.5 | .591/.625/.615/.607 | 0 |
| period-2 words n0=12 (3000 seeds) / n0=14 (all) | | 26.5M / 51.9M pairs | 6 / 7 | 3/5, 7/12 | 0 |

* Only the reader's pair (0,max,101,119) and its **mirror** (r=-18/269: 0->119, 269->101, same g=5, structure verified exactly K<=4, a second valid 5/9 family, not an improvement) attain 5/9; every other survivor is worse, with the pattern **min g = h0-1** for the extremal even-n0 seeds (the reader's O is special: g=h0-2).
* **New ties at n0=11:** the 11-point sample (every 20th of 640,905 derived seeds) contains 8 further seeds / 11 maps with g=5, i.e. limit exactly 5/9, all verified exactly for K<=4 (n11_ties.json; incl. maps with interior anchors and extreme exit, e.g. seed [0,40,54,64,74,77,80,96,108,152,224], r=18/49). So the reader's family is not isolated (about 8 such seeds per 32k, extrapolating ~160 over all 640,905 derived seeds [heuristic]); by the bound below none of them can improve.
* No self-similar chain with limit < 5/9 exists among the seeds scanned. **No sets were submitted to the judge** (nothing to submit; no families beat 5/9).
* Tag [derived-here]: any such family has g >= (9/17)(n0-2) (otherwise c* < 9/17), and g is a cycle mean of a 4-node max-plus matrix (denominator <= 4), so for n0=11 g=5 is the minimum possible: **the reader's 5/9 is optimal among two-shared-point chains with n0=11**; n0=12 needs g<=5.5 (5.5=11/2 allowed), n0=13 g=6, n0=14 g=6.5, n0=15 g=7 (7/13=.538) are the only improving cases. Also g >= h(O-{a,b,a',b'}) (the cycle that avoids all four shared points), and in a 1-point chain a or a' must be an extreme point of O (else a formal cross-relation: both are AP-midpoints) [derived-here].

## Ideas documented, not run
* Two maps S = O u phi1(S) u phi2(S) (tree; per node the children attach at two pairs, leaves are unconstrained, so the leaf layer dominates: expected worse than chains).
* Sharing k>=3 points per copy; near-extremal seeds (h0=f+1); realisations of the non-saturated 15-point patterns other than the stored one (positive-dimensional families could change which maps are valid); 13-point seeds from 12-class + AP-forming extensions (1.4M, not enumerated); period-3 words; full n11 scan (only ties 5/9 possible).

## Honest conclusion
No improvement of 5/9. Structure validity was tested for K<=3 only (mod P), and for the reported examples exactly for K<=4 (the reader's: K<=8 elsewhere); the all-K statement for a new family would need an L015-type argument and none was needed. The seed coverage is the stated one; unscanned seed families (e.g. 13-point extremal sets not extending to 14 points, other 15/17-point extremal sets, n0>=16) remain open. Data: data/selfsim_families.json. Large seed files (n11) are git-ignored; regenerate with dump_seeds.py.
