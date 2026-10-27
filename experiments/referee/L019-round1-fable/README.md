# Referee #2 (round 1) scratch folder for L019

Review: results/reviews/L019-triple-coverage-C1__referee__20261027T060439Z.md (VERDICT: ACCEPT WITH FIXES).

Files (all written from scratch; nothing imported from e757/, judge/, hg.py, pyverify.py):
- ref.py: linearity, F7 copies (two disjoint edges + centre with a perfect matching), P3 (brute force and Hall/SDR matching),
  tau (branch and bound), all minimum transversals, CP-SAT cross-check, fold construction.
- selftest.py: cross-checks of ref.py against brute force / CP-SAT and the stored lists.
- test_fold.py: Theorem 5 (a)-(d) on stored graphs and random linear 3-graphs (0 failures on 7,286 + 13,754 folds).
- test_slack.py: Theorem 1 bookkeeping, (Pair), Theorem 2(iv), (Red) on stored graphs (0 failures).
- test_gadget.py: Theorem 2(i) with k = 2 (slack <= 3) and k = 3 (slack <= 1, i.e. C1 on data; also Theorem 3) (0 violations).
- test_misc.py: Lemma 11, Proposition 10's F7 configuration, Step 0.8 inequality, small violators.
- nbhd26.cpp / nbhd26: independent C++ re-implementation of C8 (confirms the (26,22,11) claim: 144 triples, all (6,4)).
- repro/: copy of the prover's scripts; `bash reproduce.sh` reproduced all eight output files byte-identically, except that the
  fourth nbhd_cover.py iteration (cell 26_22_11) exceeds its 1800 s timeout (stopped manually after the C++ confirmation).

Commands and outputs are quoted in the review.  Run everything with `timeout` and `nice -n 10`.
