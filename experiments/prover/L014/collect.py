"""(L014) Prints the numbers quoted in the certificate from the output files of this folder (for the final text)."""
import os, json, re, subprocess
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()
print('== big table'); print(sh('python3 big_table.py out/cells 14,10,5,3 13,10,5,3 11,9,4,3 17,11,6,3 20,12,7,3 15,13,6,3 18,14,7,3 21,15,8,3 19,17,8,3 22,18,9,3 21,18,9,3 23,21,10,3'))
print('== top'); print(sh('python3 top_info.py out/cells 23,21,10,3'))
for f in ['final_inputs_output.txt', 'final_noprune_output.txt', 'final_classify_output.txt', 'control_checks_output.txt', 'crosscheck_direct_output.txt', 'equiv_check_output.txt', 'md9_compare_output.txt']:
    if os.path.exists(f): print('==', f); print(sh('tail -n 12 %s | cut -c1-400' % f))
if os.path.exists('bf_final_output.txt'): print('== bf'); print(sh('head -1 bf_final_output.txt; tail -1 bf_final_output.txt; grep -c EQUAL bf_final_output.txt; grep -c DIFFERENT bf_final_output.txt'))
if os.path.exists('compare_cells_output.txt'): print('== compare'); print(sh('grep -v " EQUAL" compare_cells_output.txt | grep -v "^cell_.*mine=[0-9]*$" | head; grep SUMMARY compare_cells_output.txt'))
print('== resmon max'); print(sh("awk -F'\\t' 'BEGIN{a=0;b=0;c=0;d=0;e=1e18} {split($2,x,\" \"); if (x[1]>a) a=x[1]; if (x[2]>b) b=x[2]; if ($3>c) c=$3; if ($4>d) d=$4; if ($5<e) e=$5} END {print \"python total KB\", a, \"max single KB\", b, \"binaries KB\", c, \"out MB\", d, \"min free MB\", e}' out/resmon.tsv"))
