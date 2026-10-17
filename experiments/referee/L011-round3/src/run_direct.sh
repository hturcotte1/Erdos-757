#!/bin/bash
# Direct window searches (no rebuild): Delta<=2 cells; (21,12,>=8) Delta<=3; (21,13,>=8) Delta<=3 with F7 prune (= Lemma X21 directly)
cd /home/user/Erdos-757/experiments/referee/L011-round3
./src/cells3.sh "21 11 8 2" "21 12 8 2" "21 13 8 2" "21 12 8 3" "21 13 8 3 1"
echo DIRECT-DONE >> logs/cells3.txt
