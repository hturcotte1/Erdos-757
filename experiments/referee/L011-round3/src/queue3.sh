#!/bin/bash
# wait for the cell enumerations to finish (frees one of the two process slots), then run the class-level steps in sequence
cd /home/user/Erdos-757/experiments/referee/L011-round3
while ! grep -q CELLS-DONE logs/cells3.txt; do sleep 10; done
./src/classlevel3.sh x20; ./src/classlevel3.sh x21; ./src/classlevel3.sh c8
# C6 needs the T17 classes (17,13,7)
python3 -I src/build_inputs3.py out/in_c6a.txt AP AP out/C_14_12_6_d3.txt:14; python3 -I src/build_inputs3.py out/in_c6b.txt AP out/C_17_13_7_d3.txt:17; python3 -I src/build_inputs3.py out/in_c6c.txt out/C_10_7_4_d3.txt:10:2; cat out/in_c6a.txt out/in_c6b.txt out/in_c6c.txt > out/in_c6_all.txt; wc -l out/in_c6_all.txt
./src/classlevel3.sh c6
echo CLASSLEVEL-DONE >> logs/classlevel3.txt
