#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L010-round3; P=/home/user/Erdos-757/experiments/prover/L010/out
s=$(date +%s); ./bin/myext 18 7 3 1000 < $P/inH19.txt > out/myhits_H19_proverinputs.txt; e=$(date +%s)
echo "myext 18 7 3 on inH19.txt: $(tail -1 out/myhits_H19_proverinputs.txt) [$((e-s)) s]"
grep ^HIT out/myhits_H19_proverinputs.txt | sort > out/tmp_mine_H19.txt; zcat $P/hitsH19.txt.gz | grep ^HIT | sort > out/tmp_prover_H19.txt
echo "lines mine=$(wc -l < out/tmp_mine_H19.txt) prover=$(wc -l < out/tmp_prover_H19.txt); $(cmp -s out/tmp_mine_H19.txt out/tmp_prover_H19.txt && echo 'C5 HIT SETS IDENTICAL' || echo 'C5 HIT SETS DIFFER')"
rm -f out/tmp_mine_H19.txt out/tmp_prover_H19.txt
s=$(date +%s); ./bin/myfilter HIT 19 notau all < out/myhits_H19_proverinputs.txt > out/myfilt_H19_proverinputs.txt; e=$(date +%s)
echo "myfilter on my C5 hits: $(tail -1 out/myfilt_H19_proverinputs.txt) [$((e-s)) s]"
echo C5DONE
