#!/bin/bash
# two workers; each: nice -n 10, timeout per command
cd "$(dirname "$0")"
run() { tag=$1; part=$2; np=$3; timeout 7200 nice -n 10 ./filt seeds_$tag.txt 3 $part $np > out/hits_${tag}_p${part}of${np}.txt 2> out/hist_${tag}_p${part}of${np}.txt; echo "done $tag $part/$np $(date -u +%H:%M)" >> out/progress.log; }
( run n12 0 2; run n14 0 1; run n13 0 2 ) &
( run n12 1 2; run n15 0 1; run n13 1 2 ) &
wait
