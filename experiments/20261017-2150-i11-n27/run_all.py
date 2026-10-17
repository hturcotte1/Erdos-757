"""Bottom-up driver for the n=27 probe. NPROC=1, nice 19, per-cell timeout, 6 h total cap, >= 8 GB free disk check.
Order: closure of the cheap tops (27,13,10,2),(27,18,11,2),(27,14,10,3),(27,19,11,3) by (n,m); then the rest of the missing cells by (n,m) with the heavy chain
(24,16,9,3),(25,19,10,3),(26,22,11,3),(27,25,12,3) last (in this order)."""
import os, sys, json, re, time, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
CAP = float(os.environ.get('CAP_SECONDS', 6 * 3600)); T0 = time.time()
P = json.load(open('plan.json'))
HEAVY = ['(24, 16, 9, 3)', '(25, 19, 10, 3)', '(26, 22, 11, 3)', '(27, 25, 12, 3)']
def deps(k):
    out = set()
    for b in P[k]['branches']:
        for name, size in b['decs']:
            for m in re.finditer(r'(\d+)x\((\d+),(\d+),(\d+)\)', name):
                t = (int(m[2]), int(m[3]), int(m[4]), b['d'])
                if t[0] == 1: continue
                ks = str(t)
                if ks in P and not P[ks]['exists']: out.add(ks)
    return out
def clo(k, seen):
    for d in deps(k):
        if d not in seen: seen.add(d); clo(d, seen)
cheap = ['(27, 13, 10, 2)', '(27, 18, 11, 2)', '(27, 14, 10, 3)', '(27, 19, 11, 3)']
s = set(cheap)
for c in cheap: clo(c, s)
key = lambda k: eval(k)[:2]
order = sorted(s, key=key)
rest = [k for k in P if not P[k]['exists'] and k not in s and k not in HEAVY]
order += sorted(rest, key=key) + [h for h in HEAVY if h not in s]
# cheap tops last within the cheap block is automatic (n=27 largest)
env = dict(os.environ, CELLDIR=os.path.join(HERE, 'out', 'cells'), ENGINELOG=os.path.join(HERE, 'out', 'engine.log'), NPROC='1', MD='10')
print('order:', order, flush=True)
for k in order:
    n, m, t, D = eval(k)
    f = os.path.join('out', 'cells', 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    if os.path.exists(f): continue
    if not (m > 0): continue
    left = CAP - (time.time() - T0)
    if left < 60: print('CAP reached before', k, flush=True); break
    free = shutil.disk_usage('.').free / 2**30
    if free < 8: print('DISK LOW %.1f GB before %s: stop' % (free, k), flush=True); break
    tmo = int(left) if k in HEAVY or len(P[k]['branches']) and k in cheap else int(min(left, 2400))
    if k in HEAVY: tmo = int(left)
    print(time.strftime('%H:%M:%S'), 'START', k, 'timeout', tmo, 'free GB %.1f' % free, flush=True)
    r = subprocess.run(['nice', '-n', '19', 'timeout', str(tmo), 'python3', 'run_one.py', str(n), str(m), str(t), str(D)], env=env, stdout=open('out/run_%d_%d_%d_D%d.log' % (n, m, t, D), 'w'), stderr=subprocess.STDOUT)
    print(time.strftime('%H:%M:%S'), 'END', k, 'rc', r.returncode, flush=True)
    if r.returncode != 0:
        with open('progress.tsv', 'a') as pf: pf.write('%s\tFAILED_OR_TIMEOUT_rc%d\t%.0f\t-\t-\t-\t-\n' % (k.replace(' ', ''), r.returncode, time.time() - T0))
        if k in cheap + HEAVY: print('top/heavy cell failed; continuing with the rest', flush=True)
print('DRIVER DONE elapsed %.0f s' % (time.time() - T0), flush=True)
