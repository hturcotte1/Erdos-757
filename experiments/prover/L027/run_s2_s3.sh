#!/bin/bash
# Re-run of the panel judge's checks S2 and S3 (experiments/prover/e1hub-synthesis/checks/checks.py,
# the judge's own code, unmodified) for the Sanity checks (E) of L027. Sequential, one process, nice.
set -u
OUT="$(cd "$(dirname "$0")" && pwd)"
CHK="$OUT/../e1hub-synthesis/checks/checks.py"
cd "$OUT/../L017/out"
timeout 1200 nice -n 10 python3 "$CHK" S2 \
  L012/cells/cell_3_1_1_D3.txt L012/cells/cell_8_5_3_D3.txt L012/cells/cell_10_7_4_D3.txt \
  L012/cells/cell_12_10_5_D3.txt L012/cells/cell_14_12_6_D3.txt L012/cells/cell_15_11_6_D3.txt \
  L012/cells/cell_17_13_7_D3.txt L012/cells/cell_19_16_8_D3.txt L012/cells/cell_22_17_9_D3.txt \
  L016/cells_new/runB2/cell_26_22_11_D3.txt > "$OUT/S2_rerun_output.txt" 2>&1
echo "S2 exit $?" >> "$OUT/S2_rerun_output.txt"
timeout 2400 nice -n 10 python3 "$CHK" S3 \
  L014/cells/cell_5_2_1_D3.txt L013/cells/cell_9_7_3_D2.txt L013/cells/cell_12_8_4_D2.txt \
  L013/cells/cell_15_9_5_D2.txt L013/cells/cell_18_10_6_D2.txt L013/cells/cell_21_11_7_D2.txt \
  L016/cells_new/runA/cell_24_12_8_D2.txt > "$OUT/S3_rerun_output.txt" 2>&1
echo "S3 exit $?" >> "$OUT/S3_rerun_output.txt"
