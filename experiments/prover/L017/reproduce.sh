#!/bin/bash
# L017 (structure of a minimal counterexample to I11): every command of the illustrative computations C1-C6.
# Run from experiments/prover/L017/.  One process each, niced, with timeouts (the machine is shared).
set -e
cd "$(dirname "$0")"
mkdir -p out/L012 out/L013 out/L014 out/L016
# the refereed cell lists (read-only sources; extracted into the git-ignored out/)
(cd out/L012 && tar xzf ../../../L012/cells.tar.gz)
(cd out/L013 && tar xzf ../../../L013/cells.tar.gz)
(cd out/L014 && tar xzf ../../../L014/cells.tar.gz)
(cd out/L016 && tar xzf ../../../L016/cells_new.tar.gz)
# C1: Theorem 7 (needs nauty geng: experiments/referee/L013-round2/out/nauty_build/geng)
timeout 1800 nice -n 10 python3 check_lemma_m.py 12 3000 20261027 > check_lemma_m_output.txt
# C2: Theorem 2 (U) on the stored tight and slack-1 cells
timeout 1800 nice -n 10 python3 check_cells_u2.py out/L012/cells/cell_3_1_1_D4.txt out/L012/cells/cell_10_7_4_D4.txt \
  out/L012/cells/cell_14_12_6_D4.txt out/L012/cells/cell_17_13_7_D3.txt out/L012/cells/cell_12_10_5_D4.txt \
  out/L012/cells/cell_19_16_8_D4.txt out/L012/cells/cell_22_17_9_D4.txt out/L016/cells_new/runF/cell_26_22_11_D3.txt \
  > check_cells_u2_output.txt
# C3: all vertex-critical linear violators with at most 10 vertices, every claim of Theorems 1, 3, 4, 5 checked exactly
timeout 3000 nice -n 10 python3 minimal_violators.py 10 > minimal_violators_10_output.txt
# C3 (extension: about 35 min on the loaded machine): 11 vertices
timeout 9000 nice -n 10 python3 minimal_violators.py 11 11 > minimal_violators_11_output.txt
# C4: the engine's decompositions at the 17 top-level violator cells of L013/L016, tight cells n <= 30, cells n = 28..30
timeout 600 nice -n 10 python3 engine_decomps.py > engine_decomps_output.txt
# C5: local configurations of Theorem 4 (iv) in the 13 tight and the 470 slack-1 Delta<=3 classes with n <= 26 (Corollary 13.3)
timeout 600 nice -n 10 python3 tight_configs.py > tight_configs_output.txt
timeout 1500 nice -n 10 python3 tight_configs.py out/L012/cells/cell_8_5_3_D3.txt out/L012/cells/cell_12_10_5_D3.txt \
  out/L012/cells/cell_15_11_6_D3.txt out/L012/cells/cell_19_16_8_D3.txt out/L012/cells/cell_22_17_9_D3.txt \
  out/L016/cells_new/runF/cell_26_22_11_D3.txt > tight_configs_slack1_output.txt
# C6: Theorem 2 (R), (R+), (U) on random linear 3-graphs
timeout 900 nice -n 10 python3 check_lemmas_random.py 1500 7 > check_lemmas_random_output.txt
# C7: cross-check of the minimum-transversal enumeration against direct transversal numbers
timeout 1500 nice -n 10 python3 crosscheck_pairs.py 1000 out/L012/cells/cell_3_1_1_D3.txt out/L012/cells/cell_10_7_4_D4.txt \
  out/L012/cells/cell_14_12_6_D4.txt out/L012/cells/cell_17_13_7_D3.txt out/L012/cells/cell_8_5_3_D3.txt \
  out/L012/cells/cell_15_11_6_D3.txt out/L012/cells/cell_22_17_9_D3.txt > crosscheck_pairs_output.txt
timeout 2400 nice -n 10 python3 crosscheck_pairs.py 1000 out/L016/cells_new/runF/cell_26_22_11_D3.txt \
  out/L012/cells/cell_12_10_5_D3.txt out/L012/cells/cell_19_16_8_D3.txt >> crosscheck_pairs_output.txt
# C8: the engine's hits at the top-level cell (24,13,9,3) (r = 6 inputs) are all disconnected, as Theorem 4(iii) requires
timeout 900 nice -n 10 python3 ext_hits_check.py > ext_hits_check_output.txt
# C9: end-to-end brute force of Theorem 4 (iii)-(iv) + C5 on small unions of known graphs
timeout 1800 nice -n 10 python3 brute_patterns.py > brute_patterns_output.txt
