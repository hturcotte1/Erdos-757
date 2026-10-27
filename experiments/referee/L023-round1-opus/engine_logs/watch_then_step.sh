#!/bin/bash
# wait for my cell(17,15,7,3) to be DONE in the GAP run, stop that run (my own processes only), then start the one-step run of cell(21,19,9,3)
P=/dev/shm/L023ref/engine_run/progress.jsonl
timeout 7200 bash -c "until grep -q '\"cell\": \[17, 15, 7, 3\]' $P 2>/dev/null; do sleep 10; done"
date -u +"17_15_7_DONE_SEEN %FT%TZ"
kill 2879 2878 2>/dev/null
sleep 2
pkill -f "/dev/shm/L023ref/engine_run/bin/" 2>/dev/null
date -u +"GAP_RUN_STOPPED %FT%TZ"
/dev/shm/L023ref/step2119/run_step.sh > /dev/shm/L023ref/step2119/run_step.log 2>&1
date -u +"STEP_DONE %FT%TZ"
