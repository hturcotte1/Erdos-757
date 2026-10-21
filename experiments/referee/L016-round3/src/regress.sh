#!/bin/bash
# regression: L012's ext_d (MAXP 256), the worker's MAXP-640 rebuild, the prover's ext_d_fast and my own build of ext_d_fast.c, byte for byte
cd /home/user/Erdos-757/experiments/referee/L016-round3; mkdir -p out/reg
E256=/home/user/Erdos-757/experiments/prover/L012/bin/ext_d; E640=/home/user/Erdos-757/experiments/20261017-2150-i11-n27/bin/ext_d
EF=/home/user/Erdos-757/experiments/prover/L016/bin/ext_d_fast; EM=bin/ext_d_fast_mine
gcc -O2 -Wall -o $EM /home/user/Erdos-757/experiments/prover/L016/src/ext_d_fast.c 2>/dev/null; cmp $EM $EF && echo "own build of src/ext_d_fast.c byte-identical to the prover's bin/ext_d_fast" || echo "own build differs in bytes from the prover's binary (flags/paths); behaviour compared below"
gcc -O2 -Wall -o bin/ext_d_640_mine /home/user/Erdos-757/experiments/prover/L016/src/ext_d_maxp640.c 2>/dev/null; cmp bin/ext_d_640_mine $E640 && echo "own build of src/ext_d_maxp640.c byte-identical to the worker's bin/ext_d" || echo "own 640 build differs in bytes"
total=0
run() { name=$1; args=$2; file=$3; cnt=$(wc -l < $file); total=$((total+cnt)); 
  for b in E256 E640 EF EM; do nice -n 10 timeout 1500 ${!b} $args < $file > out/reg/$name.$b.out 2> out/reg/$name.$b.err; echo $? > out/reg/$name.$b.rc; done
  r256=$(cat out/reg/$name.E256.rc); r640=$(cat out/reg/$name.E640.rc); rf=$(cat out/reg/$name.EF.rc); rm_=$(cat out/reg/$name.EM.rc)
  c1=$(cmp -s out/reg/$name.E640.out out/reg/$name.EF.out && echo IDENT || echo DIFF); c2=$(cmp -s out/reg/$name.EF.out out/reg/$name.EM.out && echo IDENT || echo DIFF)
  if [ "$r256" = 0 ]; then c3=$(cmp -s out/reg/$name.E256.out out/reg/$name.E640.out && echo IDENT || echo DIFF); else c3="n/a(rc256=$r256:$(cat out/reg/$name.E256.err|tr -d '\n'))"; fi
  pc=$(python3 src/paircount.py $(echo $args | cut -d' ' -f1) $(echo $args | cut -d' ' -f5) < $file)
  echo "$name [$args] inputs=$cnt rc(256,640,fast,mine)=$r256,$r640,$rf,$rm_ 640-vs-fast=$c1 fast-vs-mine=$c2 256-vs-640=$c3 | $pc | $(tail -1 out/reg/$name.EF.out | cut -c1-150)"; }
python3 src/sample.py out/in_25_19_10_3.txt 600 1 > out/reg/s1.txt; python3 src/sample.py out/in_25_19_10_3.txt 200 2 > out/reg/s1b.txt; python3 src/sample.py out/in_25_19_10_3.txt 100 3 > out/reg/s1c.txt
python3 src/sample.py out/in_26_22_11_3.txt 800 4 > out/reg/s2.txt; python3 src/sample.py out/in_26_22_11_3.txt 200 5 > out/reg/s2b.txt
python3 src/sample.py out/in_24_16_9_3_d3.txt 300 6 > out/reg/s4.txt; python3 src/sample.py out/in_23_21_10_3.txt 400 7 > out/reg/s5.txt
run s1_24v "24 9 10 3 2" out/reg/s1.txt; run s1b_24v_noprune "24 9 10 3 2 noprune" out/reg/s1b.txt; run s1c_24v_wrongTG "24 8 10 3 2" out/reg/s1c.txt; run s1d_24v_TGeqT_d1 "24 9 9 1 2" out/reg/s1c.txt; run s1e_24v_d2 "24 9 10 2 2" out/reg/s1c.txt
run s2_25v "25 10 11 3 2" out/reg/s2.txt; run s2b_25v_noprune "25 10 11 3 2 noprune" out/reg/s2b.txt; run s2c_25v_wrongTG11 "25 11 11 3 2" out/reg/s2b.txt
run s3_26v_top "26 11 12 3 2" out/in_27_25_12_3.txt; run s3b_26v_top_noprune "26 11 12 3 2 noprune" out/in_27_25_12_3.txt
run s4_23v_d3 "23 8 9 3 2" out/reg/s4.txt; run s4b_23v_d2_all "23 8 9 2 1" out/in_24_16_9_3_d2.txt
run s5_22v "22 9 10 3 2" out/reg/s5.txt; run s5b_22v_noprune "22 9 10 3 2 noprune" out/reg/s5.txt
run s6_26v_sparse_27_19 "26 10 11 3 2" out/in_27_19_11_3.txt; run s6b_26v_sparse_27_14_d2 "26 9 10 2 2" out/in_27_14_10_3_d2.txt; run s6c_26v_sparse_27_14_d3 "26 9 10 3 2" out/in_27_14_10_3_d3.txt
run s7_25v_sparse_26_16_d2 "25 9 10 2 2" out/in_26_16_10_3_d2.txt; run s7b_25v_sparse_26_16_d3 "25 9 10 3 2" out/in_26_16_10_3_d3.txt
run s8_26v_27_13 "26 9 10 2 1" out/in_27_13_10_2.txt
echo "TOTAL inputs compared: $total"
