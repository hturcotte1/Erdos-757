#!/bin/bash
# Referee L011: class-level rebuild / extension steps C4-C8 with the referee's own programs (exact commands of the review).
cd /home/user/Erdos-757/experiments/referee/L011-round1
bi() { python3 -I src/build_inputs.py "$@"; }
for M in C all; do
  # C4 (21,12,8), G = H - v = [AP^4, (8,5,3)]
  bi out/in_c4_$M.txt $M AP AP AP AP 8_5_3
  ./bin/rext 20 8 3 < out/in_c4_$M.txt > out/ext_c4_$M.txt
  # C5 (X20): X - w on 19 points, 9 types of (19,11) slack 2
  bi out/in_x20_1_$M.txt $M AP AP AP 10_8_4; bi out/in_x20_2_$M.txt $M AP AP 13_9_5; bi out/in_x20_3_$M.txt $M AP 6_3_2 10_7_4
  bi out/in_x20_4_$M.txt $M AP 8_5_3 8_5_3; bi out/in_x20_5_$M.txt $M AP 16_10_6; bi out/in_x20_6_$M.txt $M 6_3_2 13_8_5
  bi out/in_x20_7_$M.txt $M 8_5_3 11_6_4 || true; bi out/in_x20_8_$M.txt $M 9_4_3 10_7_4; bi out/in_x20_9_$M.txt $M 19_11_7
  cat out/in_x20_[1-9]_$M.txt > out/in_x20_$M.txt; ./bin/rext 19 8 3 < out/in_x20_$M.txt > out/ext_x20_$M.txt
  # C6 (21,17,9), G = (20,14,8) slack 0: [AP,(17,13,7)], [AP^2,(14,12,6)], [(10,7,4)^2]  ([(20,14,8)] empty by X20)
  bi out/in_c6_1_$M.txt $M AP 17_13_7; bi out/in_c6_2_$M.txt $M AP AP 14_12_6; bi out/in_c6_3_$M.txt $M 10_7_4 10_7_4
  cat out/in_c6_?_$M.txt > out/in_c6_$M.txt; ./bin/rext 20 9 3 < out/in_c6_$M.txt > out/ext_c6_$M.txt
  # C7 (X21): X - w on 20 points, 14 types of (20,10) slack 3 (ISO = isolated point)
  bi out/in_x21_01_$M.txt $M ISO AP AP AP 10_7_4; bi out/in_x21_02_$M.txt $M ISO AP AP 13_8_5; bi out/in_x21_03_$M.txt $M ISO AP 16_9_6
  bi out/in_x21_04_$M.txt $M ISO 19_10_7; bi out/in_x21_05_$M.txt $M AP AP AP AP 8_6_3; bi out/in_x21_06_$M.txt $M AP AP AP 11_7_4
  bi out/in_x21_07_$M.txt $M AP AP 6_3_2 8_5_3; bi out/in_x21_08_$M.txt $M AP AP 14_8_5; bi out/in_x21_09_$M.txt $M AP 6_3_2 11_6_4
  bi out/in_x21_10_$M.txt $M AP 8_5_3 9_4_3; bi out/in_x21_11_$M.txt $M AP 17_9_6; bi out/in_x21_12_$M.txt $M 6_3_2 14_7_5
  bi out/in_x21_13_$M.txt $M 9_4_3 11_6_4; bi out/in_x21_14_$M.txt $M 20_10_7
  cat out/in_x21_??_$M.txt > out/in_x21_$M.txt; ./bin/rext 20 8 3 < out/in_x21_$M.txt > out/ext_x21_$M.txt
  # C8 (22,16,9), G = (21,13,8) slack 1 ([(21,13,8)] empty by X21; [(10,7,4),(11,6,4)] has no inputs)
  bi out/in_c8_1_$M.txt $M AP AP AP 12_10_5; bi out/in_c8_2_$M.txt $M AP AP 15_11_6; bi out/in_c8_3_$M.txt $M AP 8_5_3 10_7_4
  bi out/in_c8_4_$M.txt $M AP 18_12_7; bi out/in_c8_5_$M.txt $M 8_5_3 13_8_5
  cat out/in_c8_?_$M.txt > out/in_c8_$M.txt; ./bin/rext 21 9 3 < out/in_c8_$M.txt > out/ext_c8_$M.txt
done
for x in "c4 21" "x20 20" "c6 21" "x21 21" "c8 22"; do set -- $x
  for M in C all; do echo "$1 $M: $(tail -n 1 out/ext_$1_$M.txt) | $(./bin/rfilt $2 HIT < out/ext_$1_$M.txt)"; done
  ./bin/rfilt $2 HIT v < out/ext_$1_C.txt > out/v_$1.txt
done
python3 -I src/certify.py out/v_c4.txt 21 notinC 8 20; python3 -I src/certify.py out/v_x20.txt 20 disc 8 20
python3 -I src/certify.py out/v_c6.txt 21 notinC 9 12; python3 -I src/certify.py out/v_x21.txt 21 disc 8 10
python3 -I src/certify.py out/v_c8.txt 22 notinC 9 6
