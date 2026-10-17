#!/bin/bash
# wait for batch 2 to finish, then run batch 3
cd "$(dirname "$0")"
while pgrep -f run_crosscheck2.sh > /dev/null; do sleep 15; done
bash run_crosscheck3.sh
