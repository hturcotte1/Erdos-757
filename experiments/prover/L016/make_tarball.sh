#!/bin/bash
# (L016) the new lists of this certificate: run A's 45 (out/cells), run F's heavy lists (out/cellsF), run B2's two (out/cellsB, as cellsB_*)
cd /home/user/Erdos-757/experiments/prover/L016; rm -rf out/tarstage; mkdir -p out/tarstage/cells_new/runA out/tarstage/cells_new/runF out/tarstage/cells_new/runB2
for k in $(cat listA.txt); do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cells/$f out/tarstage/cells_new/runA/; done
for k in 24,16,9,3 25,19,10,3 26,22,11,3 27,25,12,3; do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; [ -e out/cellsF/$f ] && cp out/cellsF/$f out/tarstage/cells_new/runF/; done
for k in 26,22,11,3 27,25,12,3; do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cellsB/$f out/tarstage/cells_new/runB2/; done
(cd out/tarstage && sha256sum cells_new/*/*.txt) > checksums_cells_new.txt
tar czf cells_new.tar.gz -C out/tarstage cells_new
ls -la cells_new.tar.gz; wc -l checksums_cells_new.txt
