#!/bin/bash
# (L014) checks after the main run: (e1) the final step re-run without pruning on all inputs, (e2) brute force on a sample, (f) the
# Delta<=4 control cell(23,21,10,4) and A_base, (b) comparison of every cell list with the earlier runs.
cd /home/user/Erdos-757/experiments/prover/L014
M=$PWD/out/cells; F=$PWD/out/final; mkdir -p $F
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
until done_cell 23_21_10_D3; do sleep 15; done
echo "post start $(date -u +%FT%TZ)"
# (f) control: cell(23,21,10,4) with the same machinery (the Delta<=4 sub-cells were computed by sched_aux.sh, phase E), in parallel
( until grep -q "^E rc=" out/logs/sched_aux.log; do sleep 15; done
  CELLDIR=$M ENGINELOG=$PWD/out/engine_R4.log WORKDIR=$PWD/out/workR4 PROGRESS=$PWD/out/progress.jsonl NPROC=2 MD=10 nice -n 5 timeout 5400 python3 run_cells.py 23,21,10,4 > out/logs/R4.log 2>&1
  echo "f done rc=$? $(date -u +%FT%TZ)"
  python3 control_checks.py > control_checks_output.txt 2>&1 ) &
# (e1) regenerate the 133,804 inputs exactly as the engine builds them; pruned re-run (counters must equal the main run's), unpruned run + filt
CELLDIR=$M ENGINELOG=/dev/null python3 gen_inputs.py 23 21 10 3 $F/in.txt $F/tags.txt > final_inputs_output.txt
split -n l/2 -d $F/in.txt $F/in_part
P=""; for p in 00 01; do (nice -n 5 timeout 3600 ./bin/ext_d 22 9 10 3 2 < $F/in_part$p > $F/pruned_$p.txt) & P="$P $!"; done; wait $P
P=""; for p in 00 01; do (nice -n 5 timeout 5400 ./bin/ext_d 22 9 10 3 2 noprune < $F/in_part$p > $F/noprune_$p.txt) & P="$P $!"; done; wait $P
{ echo "pruned:"; tail -qn1 $F/pruned_00.txt $F/pruned_01.txt; echo "noprune:"; tail -qn1 $F/noprune_00.txt $F/noprune_01.txt;
  echo "filt HIT 23 notau on all unpruned hits:"; cat $F/noprune_00.txt $F/noprune_01.txt | ./bin/filt HIT 23 notau | tail -n1;
  echo "HIT lines in the pruned run:"; cat $F/pruned_00.txt $F/pruned_01.txt | grep -c '^HIT' ; } > final_noprune_output.txt 2>&1
echo "e1 done $(date -u +%FT%TZ)"
# (e2) brute force on a stratified random sample (seed 14), plus inputs with unpruned hits
cat $F/noprune_00.txt $F/noprune_01.txt > $F/noprune_all.txt
python3 sample_final.py $F/in.txt $F/tags.txt $F/noprune_all.txt $F/sample.txt 14 100,0,40,6,60 40 > bf_final_output.txt
nice -n 5 timeout 5400 python3 bf_final.py 22 9 10 3 2 $F/sample.txt ./bin/ext_d 5 >> bf_final_output.txt 2>&1
echo "e2 done $(date -u +%FT%TZ)"
nice -n 5 python3 final_classify.py 23 $F/noprune_00.txt $F/noprune_01.txt > final_classify_output.txt 2>&1
echo "classify done $(date -u +%FT%TZ)"
wait
# (b) comparisons with the earlier runs
SP=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
python3 compare_cells.py $M W1735=/home/user/Erdos-757/experiments/20261017-1735-q14-cell-sizes/out/cells W1925=/home/user/Erdos-757/experiments/20261017-1925-q14-decide/out/cells W1720=/home/user/Erdos-757/experiments/20261017-1720-i11-n26/out/cells L012=$SP/L012cells/cells L013=$SP/L013cells/cells > compare_cells_output.txt 2>&1
echo "post end $(date -u +%FT%TZ)"
