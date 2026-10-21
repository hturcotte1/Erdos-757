#!/bin/bash
# (L016) C2: binaries and Python files against L012/L014 and the worker's build
cd /home/user/Erdos-757/experiments/prover/L016; W=../../20261017-2150-i11-n27
for b in enum_conn filt canon realize realize_extra; do cmp bin/$b ../L012/bin/$b && echo "bin/$b byte-identical to ../L012/bin/$b"; done
cmp bin256/ext_d ../L012/bin/ext_d && echo "bin256/ext_d (L012 ext_d.c unchanged, MAXP 256) byte-identical to ../L012/bin/ext_d"
echo "diff ../L012/indep/ext_d.c src/ext_d_maxp640.c:"; diff ../L012/indep/ext_d.c src/ext_d_maxp640.c
cmp src/ext_d_maxp640.c $W/src/ext_d_maxp640.c && echo "src/ext_d_maxp640.c identical to the worker's src/ext_d_maxp640.c"
cmp bin/ext_d $W/bin/ext_d && echo "bin/ext_d (MAXP 640) byte-identical to the worker's bin/ext_d"
echo "diff src/ext_d_maxp640.c src/ext_d_fast.c: $(diff src/ext_d_maxp640.c src/ext_d_fast.c | wc -l) lines (ext_d_fast_diff.txt)"; diff src/ext_d_maxp640.c src/ext_d_fast.c > ext_d_fast_diff.txt
cmp fast/bin/ext_d bin/ext_d_fast && echo "fast/bin/ext_d = bin/ext_d_fast"
for b in canon filt enum_conn; do cmp fast/bin/$b bin/$b && echo "fast/bin/$b = bin/$b"; done
diff engine.py ../L012/engine.py && echo "engine.py identical to ../L012/engine.py"; diff decomp22.py ../L012/decomp22.py && echo "decomp22.py identical to ../L012/decomp22.py"
for f in stream.py run_cells.py tree.py gen_inputs.py input_counts.py decomp_check.py ext_validate.py pyverify.py; do diff $f ../L014/$f && echo "$f identical to ../L014/$f"; done
for f in engine.py decomp22.py stream.py run_cells.py; do diff $f fast/$f && echo "fast/$f identical to $f"; done
gcc --version | head -1
sha256sum bin/* bin256/* fast/bin/* engine.py decomp22.py stream.py run_cells.py src/*.c ../L012/indep/ext_d.c
