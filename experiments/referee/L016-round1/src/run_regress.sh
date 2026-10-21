#!/bin/bash
# Referee L016 round 1: byte-level regressions of ext_d_fast against the Gosper builds (own random samples).
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R
cat out/chunks/chunk_00000.txt out/chunks/chunk_00034.txt out/chunks/chunk_00044.txt out/chunks/chunk_00045.txt out/chunks/chunk_00054.txt out/chunks/chunk_00061.txt out/chunks/chunk_00083.txt > out/in24_pool.txt
P="nice -n 10 timeout 3000 python3 src/regress.py"
$P file 101 out/in_26_22_11.txt 500 25 10 11 3 2
$P file 102 out/in_26_22_11.txt 300 25 10 11 3 2 noprune
$P file 103 out/in_26_22_11.txt 200 25 9 11 3 2
$P file 104 out/in_26_22_11.txt 100 25 10 10 1 2
$P file 105 out/in_26_22_11.txt 100 25 11 12 3 2
$P file 201 out/in24_pool.txt 500 24 9 10 3 2
$P file 202 out/in24_pool.txt 200 24 9 10 3 2 noprune
$P file 203 out/in24_pool.txt 200 24 8 10 3 2
$P file 204 out/in24_pool.txt 100 24 9 9 1 2
$P file 301 out/in_27_14_10_3_d3.txt 2 26 9 10 3 2
$P file 302 out/in_27_14_10_3_d3.txt 2 26 9 10 3 2 noprune
$P file 303 out/in_27_19_11_3_d3.txt 18 26 10 11 3 2
$P file 304 out/in_27_14_10_3_d2.txt 7 26 9 10 2 1
$P file 305 out/in_27_25_12.txt 334 26 11 12 3 2
$P file 306 out/in_27_25_12.txt 334 26 11 12 3 2 noprune
$P random 401 1200   # stopped after 7 min (too slow with 3 Gosper builds); replaced by the next line
$P random 402 400   # stopped (sparse graphs with isolated vertices give millions of HIT lines); replaced by the next line
$P random 403 300   # graphs without isolated vertices; stopped (some EP=3 cases too slow); replaced by the next line
$P random 404 150   # m >= 2NG/3, EP <= 2, 20 s per-run timeout (skipped runs counted)
$P random 405 1000  # as 404, 1000 graphs
