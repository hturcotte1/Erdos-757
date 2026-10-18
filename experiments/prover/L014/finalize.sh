#!/bin/bash
# (L014) final summaries and tracked copies (run after post_checks2.sh).
cd /home/user/Erdos-757/experiments/prover/L014
python3 cells_summary.py out/cells > cells_summary_output.txt
python3 top_info.py out/cells 23,21,10,3 22,18,9,3 19,17,8,3 21,15,8,3 18,14,7,3 15,13,6,3 14,10,5,3 21,18,9,3 23,21,10,4 > top_info_output.txt
python3 big_table.py out/cells 14,10,5,3 13,10,5,3 11,9,4,3 12,10,5,3 17,11,6,3 20,12,7,3 15,12,6,3 17,14,7,3 20,15,8,3 15,13,6,3 18,14,7,3 21,15,8,3 19,17,8,3 21,18,9,3 22,18,9,3 23,21,10,3 23,21,10,4 > big_table_output.txt
python3 input_counts.py out/cells 23 21 10 3 > input_counts_output.txt
cat out/audit1_output.txt out/audit2_output.txt out/audit3_output.txt out/audit4_output.txt out/audit5_output.txt out/audit6_output.txt 2>/dev/null > audit_sample_output.txt
grep SUMMARY audit_sample_output.txt
(cd out && sha256sum cells/cell_*.txt) > checksums_cells.txt
tar czf cells.tar.gz -C out --exclude=cells/cell_15_13_6_D3.txt cells; gzip -c out/cells/cell_15_13_6_D3.txt > cell_15_13_6_D3.txt.gz   # each < 25 MB
ls -la cells.tar.gz cell_15_13_6_D3.txt.gz
cp out/progress.jsonl progress.jsonl; cp out/resmon.tsv resmon.tsv
