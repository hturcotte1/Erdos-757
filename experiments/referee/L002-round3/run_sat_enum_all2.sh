#!/usr/bin/env bash
# Referee round 3: full CDCL (CaDiCaL 1.5.3) enumeration of saturated (12, alpha<=7) patterns; one process per
# midpoint-1 split (each < 20 min), fresh solver per (midpoint 1, midpoint 10) cube.
cd /home/user/Erdos-757/experiments/referee/L002-round3
S=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
for idx in 0 1 2 3 4 5 6 7 8 9; do
  k=$((idx + 2))
  timeout 1150 python3 sat_enum_cubes2.py 12 7 1 10 cd15 $idx $S/sat_k${k}.txt.gz > sat_enum2_k${k}.log 2>&1
  echo "exit=$?" >> sat_enum2_k${k}.log
done
echo ALLDONE > sat_enum2_all.done
