#!/bin/bash
# Referee L013 round 2: every command used (run from this folder; large outputs in out/, git-ignored).
set -e
cd /home/user/Erdos-757/experiments/referee/L013-round2
# 0. nauty 2.8.8, unmodified, from the PyPI pynauty-2.8.8.1 sdist (sha256 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2)
mkdir -p out/dl out/src_extract bin
pip download --no-deps --no-binary :all: pynauty==2.8.8.1 -d out/dl
tar xzf out/dl/pynauty-2.8.8.1.tar.gz -C out/src_extract
rm -rf out/nauty_build && cp -r out/src_extract/pynauty-2.8.8.1/src/nauty2_8_8 out/nauty_build
(cd out/nauty_build && ./configure --disable-popcnt --disable-clz && make genbg genbgL geng labelg shortg)
cp out/nauty_build/{genbg,genbgL,geng,labelg,shortg} bin/
gcc -O2 -Wall -Wno-misleading-indentation -o bin/refx src/refx.c
# 1. arithmetic
python3 arith_ref.py > out/arith_ref_output.txt
# 2. prover lists (data only)
mkdir -p out/prover_cells && tar xzf ../../prover/L013/cells.tar.gz -C out/prover_cells
diff -rq out/prover_cells/cells ../../prover/L013/out/cells
python3 unit_tests.py
python3 audit_cells.py out/prover_cells/cells > out/audit_cells_output.txt
python3 top_branches.py out/prover_cells/cells > out/top_branches.txt
python3 verify_reps.py > out/verify_reps_output.txt
# 3. final extension steps from the prover's lists (own decompositions, random relabelling, own extension search)
./run_ext_all.sh "23 13 9 2 8" "24 13 9 2 8" "24 18 10 3 9" "25 16 10 2 9" "25 22 11 3 10" "26 14 10 2 9" "26 15 10 2 9" "26 15 10 3 9" "23 20 10 3 9" "25 17 10 3 9" "26 21 11 3 10" > out/ext_top.log
for spec in "23 14 9 2 8 2 1" "23 14 9 3 8 3 2" "24 13 9 3 8 3 2" "24 12 9 2 8 2 1"; do set -- $spec
  python3 build_inputs.py out/prover_cells/cells $1 $2 $3 $4 $5 --perm 7 > out/inp/in_$1_$2_$3_d$4.txt
  for mode in ext brute; do ./bin/refx $mode $(($1-1)) $5 $3 $6 $7 < out/inp/in_$1_$2_$3_d$4.txt | grep SUMMARY; done; done
./run_ext_all.sh "21 18 9 3 8" "23 15 9 2 8" "23 15 9 3 8" "24 14 9 2 8" "24 14 9 3 8" "24 19 10 3 9" "25 18 10 3 9" > out/ext_c9.log
./sample_brute.sh > out/sample_brute_output.txt
# 4. independent enumerations
python3 dual_d2.py out/prover_cells/cells > out/dual_d2_output.txt
for c in "24 12 9 2" "23 13 9 2" "26 14 10 2" "25 16 10 2" "22 11 7 2" "23 13 8 2" "22 12 8 2" "24 14 9 2" "22 13 8 2"; do python3 genbg_cell.py $c; done > out/genbg_d2_output.txt
./genbg_all_base.sh > out/genbg_all_base_output.txt
./bin/genbgL -q -c -Z1 -d1:3 -D3:3 11 6 18:18 | ./bin/refx filter 11 6 4 3 | tail -1
./bin/genbgL -q -c -Z1 -d1:3 -D2:3 21 13 39:39 | ./bin/refx filter 21 13 8 2 | tail -1
# 5. own bottom-up engine on the twelve top-level cells, in induction order, then comparison of all cells
NPROC=2 python3 myengine.py 23 13 9 2 23 14 9 3 23 20 10 3 24 12 9 2 24 13 9 3 24 18 10 3 25 16 10 2 25 17 10 3 25 22 11 3 26 14 10 2 26 15 10 3 26 21 11 3 > out/myengine_run.log
python3 compare_mine.py > out/compare_mine_output.txt
# 6. reproducibility comparisons
python3 compare_worker.py ../../20261017-1720-i11-n26/out/cells ../../20261017-1645-i11-n23-n24/out/cells > out/compare_worker_output.txt
mkdir -p out/l012_cells && tar xzf ../../prover/L012/cells.tar.gz -C out/l012_cells && python3 compare_worker.py out/l012_cells/cells > out/compare_l012_output.txt
