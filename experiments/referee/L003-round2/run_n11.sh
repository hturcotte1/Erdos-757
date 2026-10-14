#!/bin/bash
# Referee L003 round 2: n = 11 saturated enumeration, three pruning modes, strictly sequential, one niced process at a time.
# Each step is a separate computation well under 20 minutes.
D=/home/user/Erdos-757/experiments/referee/L003-round2
cd $D
LOG=$D/run_n11.log
: > $LOG
t() { local s=$(date +%s); "$@"; local e=$(date +%s); echo "  [$(( e - s )) s] $*" >> $LOG; }
# (1) K30 + linearity
t bash -c "nice -n 10 ./satcheck 11 1 1 | gzip > sat_n11_k1_l1.txt.gz"
zcat sat_n11_k1_l1.txt.gz | grep '^STATS' >> $LOG
# (2) linearity only (no K30)
t bash -c "nice -n 10 ./satcheck 11 0 1 | gzip > sat_n11_k0_l1.txt.gz"
zcat sat_n11_k0_l1.txt.gz | grep '^STATS' >> $LOG
# (3) K30 only (no linearity), split by R[1] = 2..10
for r1 in 2 3 4 5 6 7 8 9 10; do
  t bash -c "nice -n 10 ./satcheck 11 1 0 $r1 | gzip > sat_n11_k1_l0_r$r1.txt.gz"
  zcat sat_n11_k1_l0_r$r1.txt.gz | grep '^STATS' >> $LOG
done
echo DONE >> $LOG
