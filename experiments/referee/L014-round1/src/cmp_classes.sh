#!/bin/bash
# usage: cmp_classes.sh N FILE_A FILE_B : compares the sets of isomorphism classes of the FOUND lines of two files
# (labelg canonical forms of the incidence graphs). EQUAL iff the two class sets coincide; A may contain several labelled copies per class.
cd /home/user/Erdos-757/experiments/referee/L014-round1
N=$1; A=$2; B=$3; set -o pipefail
ca=$(mktemp -p out); cb=$(mktemp -p out)
grep '^FOUND' $A | ./bin/hg2g6 $N 2>/dev/null | ./bin/labelg -q | LC_ALL=C sort > $ca
grep '^FOUND' $B | ./bin/hg2g6 $N 2>/dev/null | ./bin/labelg -q | LC_ALL=C sort > $cb
na=$(wc -l < $ca); nb=$(wc -l < $cb); ua=$(uniq $ca | wc -l); ub=$(uniq $cb | wc -l)
onlya=$(LC_ALL=C comm -23 <(uniq $ca) <(uniq $cb) | wc -l); onlyb=$(LC_ALL=C comm -13 <(uniq $ca) <(uniq $cb) | wc -l)
echo "CMP N=$N A=$(basename $A) lines=$na classes=$ua | B=$(basename $B) lines=$nb classes=$ub | onlyA=$onlya onlyB=$onlyb $( [ $onlya -eq 0 ] && [ $onlyb -eq 0 ] && echo CLASS-SETS-EQUAL || echo DIFFERENT) $( [ $ub -eq $nb ] && echo B-one-per-class || echo B-HAS-DUPLICATES)"
rm -f $ca $cb
