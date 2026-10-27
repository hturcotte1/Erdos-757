#!/bin/bash
# L027 census of pairwise-NC non-edge triples on the ten stored near-tight lists (Delta <= 3).
OUT="$(cd "$(dirname "$0")" && pwd)"
cd "$OUT/../L017/out"
timeout 2400 nice -n 10 python3 "$OUT/census27.py" \
  L012/cells/cell_3_1_1_D3.txt L012/cells/cell_8_5_3_D3.txt L012/cells/cell_10_7_4_D3.txt \
  L012/cells/cell_12_10_5_D3.txt L012/cells/cell_14_12_6_D3.txt L012/cells/cell_15_11_6_D3.txt \
  L012/cells/cell_17_13_7_D3.txt L012/cells/cell_19_16_8_D3.txt L012/cells/cell_22_17_9_D3.txt \
  L016/cells_new/runB2/cell_26_22_11_D3.txt > "$OUT/census27_output.txt" 2>&1
echo "exit $?" >> "$OUT/census27_output.txt"
