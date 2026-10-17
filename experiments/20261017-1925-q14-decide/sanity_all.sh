#!/bin/bash
cd "$(dirname "$0")"
./sanity.sh plain 10 8 4 > out/sanity_plain_10_8_4.log 2>&1
./sanity.sh plain 19 16 8 > out/sanity_plain_19_16_8.log 2>&1
./sanity.sh stream 19 16 8 > out/sanity_stream_19_16_8.log 2>&1
./sanity.sh stream 17 11 6 > out/sanity_stream_17_11_6.log 2>&1
./sanity.sh stream 10 8 4 > out/sanity_stream_10_8_4.log 2>&1
./sanity.sh plain 23 21 10 > out/sanity_plain_23_21_10.log 2>&1
