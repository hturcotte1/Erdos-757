#!/bin/bash
# Referee L012 round 3: direct genbg (unmodified nauty 2.8.8) + own filter gcells for directly-enumerated lower cells of the recursion
# of the route-4/20 cells; compare class counts with the prover's cell files.  Waits for the census/closure chain to end (process cap).
cd /home/user/Erdos-757/experiments/referee/L012-round3
while [ ! -f logs/closure.done ]; do sleep 10; done
for c in "6 3 2 2" "6 3 2 3" "6 3 2 4" "9 4 3 3" "9 4 3 4" "8 6 3 3" "8 6 3 4" "10 8 4 3" "10 8 4 4" "11 7 4 3" "11 6 4 3" "11 6 4 4" "13 8 5 3" "13 8 5 4" "13 9 5 3" "14 8 5 3" "16 9 5 2" "16 10 6 3" "14 9 5 3" "17 10 6 3" "19 10 6 2"; do
  set -- $c; f=out/cells/cell_$1_$2_$3_D$4.txt
  if [ -f $f ]; then prov=$(grep -c '^FOUND' $f); else prov="nofile"; fi
  res=$(timeout 240 nice -n 5 ./bin/genbg -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) 2>/dev/null | nice -n 5 ./bin/gcells $1 $2 $3 $4 2>/dev/null | tail -1)
  echo "cell($1,$2,$3,D$4): prover=$prov genbg+gcells: $res"
done > logs/direct_cells.txt 2>&1
echo done > logs/direct_cells.done
