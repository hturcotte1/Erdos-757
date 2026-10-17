#!/bin/bash
# canon.sh N M < graph6 lines (incidence bigraphs, N points then M edges) -> canonical graph6 (colour classes kept apart), one per line
ND=/home/user/Erdos-757/experiments/referee/L009-round2/out/nauty
F=$(printf 'a%.0s' $(seq 1 $1))$(printf 'b%.0s' $(seq 1 $2))
$ND/labelg -q -f$F
