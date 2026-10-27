#!/bin/bash
# unpack the stored class lists (L012-L016 and n=27 worker tarballs) into data/ (not committed, ~200 MB)
set -e; cd "$(dirname "$0")"; mkdir -p data/L012 data/L013 data/L014 data/L016 data/n27
tar xzf ../prover/L012/cells.tar.gz -C data/L012 --strip-components=1
tar xzf ../prover/L013/cells.tar.gz -C data/L013; tar xzf ../prover/L014/cells.tar.gz -C data/L014
tar xzf ../prover/L016/cells_new.tar.gz -C data/L016; tar xzf ../20261017-2150-i11-n27/cells_n27_new.tar.gz -C data/n27
