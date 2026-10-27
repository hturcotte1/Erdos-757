#!/bin/bash
# usage: gen15.sh n m dest   generate the census cell (n,m) from (n,m-1),(n-1,m-1),(n-2,m-1) (one-edge extension, canonical-deletion filter,
# nauty canonical form, sort -u).  dest = file.gz (stored gzipped) or '-' (plain stream on stdout, nothing stored).
# sources: n<=14 plain lists from the 0230 census (read only), n=15 lists from out/cls_15_m.txt.gz (own)
HERE=$(cd $(dirname $0) && pwd)
OLD=$HERE/../20261027-0230-red-config/out
CANON=$HERE/../prover/L012/bin/canon
n=$1; m=$2; dest=$3
src() { if [ -s $OLD/cls_$1_$2.txt ]; then cat $OLD/cls_$1_$2.txt; elif [ -s $HERE/out/cls_$1_$2.txt.gz ]; then zcat $HERE/out/cls_$1_$2.txt.gz; fi; }
body() {
  { for k in 2 1 0; do np=$((n-k))
      if [ -s $OLD/cls_${np}_$((m-1)).txt ] || [ -s $HERE/out/cls_${np}_$((m-1)).txt.gz ]; then src $np $((m-1)) | $HERE/bin/extend2 $np $k 3; fi
    done; } | $CANON $n 2>/dev/null | LC_ALL=C sort -u -S 1500M -T $HERE/out --compress-program=gzip
}
if [ "$dest" == "-" ]; then body; else body | gzip -1 > $dest.tmp && mv $dest.tmp $dest; fi
