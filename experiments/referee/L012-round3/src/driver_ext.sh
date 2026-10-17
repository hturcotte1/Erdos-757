#!/bin/bash
# Referee L012 round 3: sequential extension jobs after the route-4 run (one process): route 20, then the top-level branches of the
# two large recursive cells (22,17,9,4) and (19,16,8,4) with my xext (T = t; tau(G) = t-1 is checked inside xext).
cd /home/user/Erdos-757/experiments/referee/L012-round3
while [ ! -f logs/xext_r4.done ]; do sleep 10; done
nice -n 5 ./bin/xext 22 10 3 2 < out/my_r20_inputs.txt > out/xext_r20.txt 2> logs/xext_r20.err; echo done > logs/xext_r20.done
nice -n 5 ./bin/xext 21 9 4 3 < out/br_22_17_9_D4_d4.txt > out/xbr_22_17_9_D4_d4.txt 2> logs/xbr_22_17_9_D4_d4.err; echo done > logs/xbr_22_17_9_D4_d4.done
nice -n 5 ./bin/xext 18 8 4 3 < out/br_19_16_8_D4_d4.txt > out/xbr_19_16_8_D4_d4.txt 2> logs/xbr_19_16_8_D4_d4.err; echo done > logs/xbr_19_16_8_D4_d4.done
nice -n 5 ./bin/xext 18 8 3 2 < out/br_19_16_8_D4_d3.txt > out/xbr_19_16_8_D4_d3.txt 2> logs/xbr_19_16_8_D4_d3.err; echo done > logs/xbr_19_16_8_D4_d3.done
nice -n 5 ./bin/xext 21 9 3 2 < out/br_22_17_9_D4_d3.txt > out/xbr_22_17_9_D4_d3.txt 2> logs/xbr_22_17_9_D4_d3.err; echo done > logs/xbr_22_17_9_D4_d3.done
echo alldone > logs/driver.done
