#!/usr/bin/env bash
# sequential timing runs; usage: run_gl_timings.sh out.jsonl
cd "$(dirname "$0")"
out=$1
run() { # n T m variant solver limit
  timeout $(( $6 + 30 )) python3 gl_timing.py $1 $2 $3 $4 $5 $6 >> $out 2>/dev/null || echo "{\"n\":$1,\"T\":$2,\"variant\":\"$4\",\"solver\":\"$5\",\"status\":\"KILLED\",\"limit\":$6}" >> $out
}
for cfg in "11 6 9 60" "12 6 10 60"; do
  set -- $cfg
  for v in none L R LR; do for s in glucose4 cadical195; do run $1 $2 $3 $v $s $4; done; done
done
for v in none L R LR; do run 13 7 11 $v glucose4 150; done
for v in none LR; do run 13 7 11 $v cadical195 150; done
