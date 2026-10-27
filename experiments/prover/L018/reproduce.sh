#!/bin/bash
# reproduce.sh -- all computations of certificate L018 (results/proofs/L018-red-universality.md).
# Exact integer arithmetic throughout. Run from this folder. Inputs read (not modified):
#   ../../20261027-0230-red-config/out/cls_*.txt and redk5_free_graphs.txt.gz, red_*.tsv (census, n <= 14)
#   ../L013/cells.tar.gz (tight cell lists; extracted into cells13/)
set -e
cd "$(dirname "$0")"
mkdir -p cells13
tar xzf ../L013/cells.tar.gz -C cells13 cells/cell_17_13_7_D3.txt cells/cell_10_7_4_D3.txt cells/cell_14_12_6_D3.txt \
    cells/cell_12_10_5_D3.txt cells/cell_8_5_3_D3.txt cells/cell_15_11_6_D3.txt cells/cell_19_16_8_D3.txt cells/cell_22_17_9_D3.txt cells/cell_13_8_5_D3.txt
N="nice -n 10 timeout 3600"
# C1: Theorem 3 (pendant catalogue)
$N python3 localconf.py 1 1 > out_root1_R1.txt
$N python3 localconf.py 1 2 > out_root1_R2.txt
$N python3 localconf.py 1 3 > out_root1_R3.txt
$N python3 show.py 1 2 > out_root1_R2_leaves.txt
$N python3 show.py 1 3 > out_root1_R3_leaves.txt
# C2: validation on the census
$N python3 validate_catalog.py 13 > validate_catalog_output.txt
$N python3 pendant_census.py 13 2 > pendant_census_n13_R2.txt
$N python3 pendant_census.py 13 3 > pendant_census_n13_R3.txt
$N python3 pendant_census.py 14 3 14 > pendant_census_n14_R3.txt
$N python3 dist_check.py > dist_check_output.txt
# C3: Theorem 2 checks
$N python3 lemma_m_check.py > lemma_m_check_output.txt
# C4: lemmas U1, U2, TP, Theorem 1
$N python3 lemma_tests.py 11 > lemma_tests_output.txt
$N python3 lemma_tests.py 12 > lemma_tests_output_n12.txt
# C5: dense core (Section 8)
$N python3 dense_core.py > dense_core_output.txt
$N python3 dense_core2.py > dense_core2_output.txt
# C6: tight cells (Remark 5.4)
$N python3 tightdeg.py > tightdeg_output.txt
# C7: local catalogues at degree-2 and degree-3 roots
$N python3 localconf.py 2 1 > out_root2_R1.txt
$N python3 localconf.py 3 1 > out_root3_R1.txt
# C8: Theorem 8 data
$N python3 tight_glue.py > tight_glue_output.txt
echo done
