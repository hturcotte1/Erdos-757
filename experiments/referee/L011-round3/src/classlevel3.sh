#!/bin/bash
# Referee round 3: class-level rebuild/final steps with ext3 (direct tau test on H, generic F7 embedding, P3, connectivity on all points)
cd /home/user/Erdos-757/experiments/referee/L011-round3
run() { local name=$1 NG=$2 TG=$3 in=$4; s=$(date +%s); nice -n 5 ./bin/ext3 $NG $TG 3 1 < $in > out/ext_$name.txt; e=$(date +%s); echo "$name: $(tail -n 1 out/ext_$name.txt) [$((e-s)) s]" | tee -a logs/classlevel3.txt; }
case "$1" in
 x20) run x20 19 7 out/in_x20_all.txt ;;
 x21) run x21 20 7 out/in_x21_all.txt ;;
 c8)  run c8 21 8 out/in_c8_all.txt ;;
 c6)  run c6 20 8 out/in_c6_all.txt ;;
esac
