#!/bin/bash
# (L013) C7: re-validation of the final extension steps: the 12 top-level branches, then the branches of the five load-bearing connected
# sub-cells that rest on the recursion only (load_bearing_output.txt); nice 19.
cd "$(dirname "$0")"
nice -n 19 timeout 3000 python3 ext_validate.py out/cells 3 2026 23 14 9 3 2 8 23 14 9 3 3 8 23 20 10 3 3 9 24 12 9 2 2 8 24 13 9 3 2 8 24 13 9 3 3 8 24 18 10 3 3 9 25 17 10 3 3 9 25 22 11 3 3 10 26 15 10 3 2 9 26 15 10 3 3 9 26 21 11 3 3 10 > ext_validate_output.txt 2>&1
EXTVAL_JSON=ext_validate_sub_output.json nice -n 19 timeout 3000 python3 ext_validate.py out/cells 3 77 21 18 9 3 3 8 24 19 10 3 3 9 23 15 9 3 2 8 23 15 9 3 3 8 24 14 9 3 2 8 24 14 9 3 3 8 25 18 10 3 3 9 > ext_validate_sub_output.txt 2>&1
