#!/bin/bash
# Reproduction of every computation cited in results/proofs/L014-f23-equals-14.md (run from this directory; about 3 CPU-hours of
# compute on 2-3 cores; large files go to out/, git-ignored).  Read-only inputs from earlier certificates: the C sources of
# experiments/prover/L012/indep, L012's engine.py/decomp22.py (copied, byte-identical), nauty 2.8.8 (unmodified sources, the copy used
# by L012), ../L012/route4_classes.txt.gz and ../L012/abase_pattern.txt (controls); the worker's / probe's / L012's / L013's cell lists
# (comparisons only, C6).
set -e
cd /home/user/Erdos-757/experiments/prover/L014
SP=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
mkdir -p $SP/L012cells $SP/L013cells; tar xzf ../L012/cells.tar.gz -C $SP/L012cells; tar xzf ../L013/cells.tar.gz -C $SP/L013cells   # comparisons only (C6)
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
# --- C2: binaries rebuilt with L012's commands, compared with L012's binaries; engine.py and decomp22.py copied from L012
mkdir -p bin out/cells out/logs; S=../L012/indep
gcc -O2 -Wall -o bin/enum_conn $S/enum_conn.c; gcc -O2 -Wall -o bin/filt $S/filt.c; gcc -O2 -Wall -o bin/ext_d $S/ext_d.c
gcc -O2 -Wall -o bin/realize $S/realize.c; gcc -O2 -Wall -o bin/realize_extra $S/realize_extra.c
gcc -O2 -DWORDSIZE=64 -DMAXN=64 -I$NB -I$ND -o bin/canon $S/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
[ -e engine.py ] || cp ../L012/engine.py .; [ -e decomp22.py ] || cp ../L012/decomp22.py .
bash build_check.sh > build_check_output.txt
# --- C1: arithmetic; dry-run trees; decompositions by two generators
python3 arith14.py > arith14_output.txt
CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 tree.py 23 21 10 3 > tree_23_21_10_3.txt
CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 tree.py 23 21 10 4 > tree_23_21_10_4.txt
CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 decomp_check.py tree_23_21_10_3.txt > decomp_check_D3_output.txt
CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 decomp_check.py tree_23_21_10_4.txt > decomp_check_D4_output.txt
python3 remark4.py > remark4_output.txt
python3 c23_construction.py > c23_construction_output.txt
# --- C3: the main run from an empty cell directory (stream.py driver; NPROC as shown; nice 5).  Phase 1: A = (14,10,5,3) (direct);
# B = the other 97 cells of the dry-run tree that do not need (14,10,5,3), in the tree's post-order (out/listB.txt).
export MD=10 CELLDIR=$PWD/out/cells PROGRESS=$PWD/out/progress.jsonl
(ENGINELOG=$PWD/out/engine_A.log WORKDIR=$PWD/out/workA NPROC=1 nice -n 5 timeout 7200 python3 run_cells.py 14,10,5,3 > out/logs/A.log 2>&1) &
(ENGINELOG=$PWD/out/engine_B.log WORKDIR=$PWD/out/workB NPROC=1 nice -n 5 timeout 7200 python3 run_cells.py $(cat listB.txt) > out/logs/B.log 2>&1) &
# phases 2-4 (C: (15,13,6,3), (18,14,7,3); D: (21,15,8,3); F: (22,18,9,3) with G: (19,17,8,3); T: (23,21,10,3)) start when their
# prerequisites are complete files.  The actual run used sched_main.sh (phase 2: C and D) until 22:31 UTC, then sched_main2.sh (D
# re-run from scratch in its own session) and from 23:02 UTC sched_main3.sh (G as soon as C is complete, F after D, then T; each job in
# its own session); see README 'Process notes'.  To reproduce:
( until grep -q '^INFO ' out/cells/cell_14_10_5_D3.txt 2>/dev/null && grep -q '^INFO ' out/cells/cell_21_18_9_D3.txt 2>/dev/null; do sleep 15; done
  (ENGINELOG=$PWD/out/engine_C.log WORKDIR=$PWD/out/workC NPROC=1 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 15,13,6,3 18,14,7,3 > out/logs/C.log 2>&1) &
  (ENGINELOG=$PWD/out/engine_D2.log WORKDIR=$PWD/out/workD2 NPROC=1 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 21,15,8,3 > out/logs/D2.log 2>&1) &
  setsid -w ./sched_main3.sh > out/logs/sched_main3.log 2>&1; wait ) &
# --- C5 (f) Delta<=4 cells for the control, C7 equivalence of the driver, C8 direct enumerations and MD=9 recursions
cp listE.txt out/listE.txt; ./sched_aux.sh > out/logs/sched_aux.log 2>&1 &
# (its last step, crosscheck_direct.py on 14,12,6,3 ..., was stopped by the prover after 24 min on (14,12,6,3); the own direct runs used
#  in C8 (c) were then, after phase E:)
( until grep -q '^E rc=' out/logs/sched_aux.log 2>/dev/null; do sleep 15; done
  echo "cell (14, 12, 6, 3): direct route STOPPED by the prover after 24 min wall (lowest-priority session; enum_conn had printed almost nothing): no result" > crosscheck_direct_output.txt
  nice -n 10 python3 crosscheck_direct.py $PWD/out/cells $PWD/out/direct 1500 17,11,6,2 15,11,6,2 16,11,6,2 18,12,7,2 19,11,7,2 20,11,7,2 19,12,7,2 20,12,7,2 20,11,7,3 >> crosscheck_direct_output.txt 2>&1 ) &
# --- C4 (e) final step without pruning, brute force; C9 controls (f); C6 (b) comparisons
./post_checks2.sh > out/logs/post_checks2.log 2>&1 &   # (post_checks.sh: the earlier, sequential version, stopped while waiting)
wait
# --- further checks on the finished lists
CELLDIR=$PWD/out/cells ENGINELOG=/dev/null python3 ext_validate.py 21 18 9 3 out/extval 6000 > ext_validate_21_18_9_output.txt
python3 census_control.py > census_control_output.txt
bash l008_direct_compare.sh > l008_direct_compare_output.txt
mkdir -p out/L013direct; for d in ../L013/out/direct/cell_*; do b=$(basename $d); [ -f $d/$b.txt ] && ln -sf $(realpath $d/$b.txt) out/L013direct/$b.txt; done
python3 compare_cells.py out/cells L013direct=$PWD/out/L013direct | grep L013direct > l013_direct_compare_output.txt
python3 input_counts.py out/cells 23 21 10 3 > input_counts_output.txt
for c in "14 10 5 3" "13 10 5 3" "12 10 5 3"; do set -- $c; CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 tree.py $1 $2 $3 $4 9; done > tree_md9.txt
CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 decomp_check.py tree_md9.txt > decomp_check_md9_output.txt
SP=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad   # the run extracted L012/L013 cells.tar.gz here:
mkdir -p $SP/L012cells $SP/L013cells; tar xzf ../L012/cells.tar.gz -C $SP/L012cells; tar xzf ../L013/cells.tar.gz -C $SP/L013cells
python3 compare_branches.py out/cells W1735=/home/user/Erdos-757/experiments/20261017-1735-q14-cell-sizes/out/cells W1925=/home/user/Erdos-757/experiments/20261017-1925-q14-decide/out/cells W1720=/home/user/Erdos-757/experiments/20261017-1720-i11-n26/out/cells L012=$SP/L012cells/cells L013=$SP/L013cells/cells > compare_branches_output.txt
python3 top_info.py out/cells 23,21,10,3 22,18,9,3 19,17,8,3 21,15,8,3 18,14,7,3 15,13,6,3 14,10,5,3 21,18,9,3 23,21,10,4 > top_info_output.txt
# --- soundness audit, in batches as the lists were completed (the run copied the completed files into out/audit1 ... out/audit6b):
# audit1 (115 lists, K=2000, seed 14), audit2 (23 lists, K=2000, seed 15), audit3 ((15,13,6,3), (18,14,7,3), K=1000, seed 16),
# audit4 ((21,15,8,3), K=1000, seed 17), audit5 ((19,17,8,3), K=1000, seed 18), audit_late.sh ((22,18,9,3) K=500, (23,21,10,4) and
# (23,21,10,3) K=200, seed 19); e.g.  python3 audit_sample.py out/audit3 1000 16 > out/audit3_output.txt
python3 pyverify.py > pyverify_unit_tests_output.txt
# --- summaries and tracked copies
bash finalize.sh
