#!/bin/bash
# after glue32_c.py has finished (glue32_c.log has a line 'c connected ...'): test the (c)-route classes with the C port
cd "$(dirname "$0")"
python3 embed_obs.py glue32_classes_c.txt c 32
./rexact_c 32 < glue32_classes_c.txt | grep RES | tee glue32_c_rexact_c.txt | awk '{print $3}' | sort | uniq -c
