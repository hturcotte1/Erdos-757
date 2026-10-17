"""VF2 comparison of every non-empty cell computed by src/myengine.py with the prover's (or, if absent there, L012's) list."""
import os, subprocess, sys
E = 'out/myeng'; P = 'out/prover_cells/cells'; L = 'out/l012cells/cells'
res = []
for f in sorted(os.listdir(E), key=lambda f: tuple(int(x) for x in f[5:-4].replace('D', '').split('_'))):
    n = int(f.split('_')[1])
    mine = sum(1 for l in open(os.path.join(E, f)) if l.startswith('FOUND'))
    if mine == 0: continue
    other = os.path.join(P, f) if os.path.exists(os.path.join(P, f)) else os.path.join(L, f)
    r = subprocess.run([sys.executable, 'src/iso_compare.py', str(n), os.path.join(E, f), other], capture_output=True, text=True).stdout.strip()
    res.append((f, mine, 'EQUAL' if r.endswith('EQUAL') else 'DIFF: ' + r))
    print(f, mine, res[-1][2][:80], flush=True)
print('non-empty engine cells compared:', len(res), 'EQUAL:', sum(1 for x in res if x[2] == 'EQUAL'))
