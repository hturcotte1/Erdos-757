import sys, os, time, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
n, m, t, D, d, k = map(int, sys.argv[1:7]); celldir = sys.argv[7]
tp = t - 1; Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
lines = []
for dec in rlib.my_decomps(n - 1, m - d, Sp):
    try: lines += list(rlib.inputs_for(dec, celldir, d, n - 1))
    except FileNotFoundError: pass
random.seed(1); smp = random.sample(lines, min(k, len(lines)))
t0 = time.time()
r = subprocess.run([rlib.REXT, 'ext', str(n - 1), str(tp), str(d), str(d - 1)], input='\n'.join(smp) + '\n', capture_output=True, text=True)
print(len(lines), 'inputs; sample', len(smp), 'secs %.2f' % (time.time() - t0), r.stderr.strip())
