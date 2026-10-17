#!/bin/bash
# (L014) C2: the six binaries are byte-identical to experiments/prover/L012/bin; engine.py and decomp22.py identical to L012's.
cd /home/user/Erdos-757/experiments/prover/L014
for b in enum_conn filt ext_d realize realize_extra canon; do cmp bin/$b ../L012/bin/$b && echo "bin/$b byte-identical to ../L012/bin/$b"; done
diff engine.py ../L012/engine.py && echo "engine.py identical to ../L012/engine.py"
diff decomp22.py ../L012/decomp22.py && echo "decomp22.py identical to ../L012/decomp22.py"
gcc --version | head -1
sha256sum bin/* engine.py decomp22.py ../L012/indep/enum_conn.c ../L012/indep/ext_d.c ../L012/indep/filt.c ../L012/indep/canon.c stream.py run_cells.py
