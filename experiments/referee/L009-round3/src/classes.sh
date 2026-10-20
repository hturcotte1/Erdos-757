#!/bin/bash
# classes.sh N1 TAG < lines  -> sorted unique canonical graph6 strings (one per isomorphism class), via nauty labelg
D=/home/user/Erdos-757/experiments/referee/L009-round3
python3 $D/src/to_g6.py "$1" "$2" | $D/bin/labelg -q | sort -u
