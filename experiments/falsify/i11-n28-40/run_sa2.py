# SA polishing from the best gluing graphs (degree cap 5 so that A_base-type pieces are allowed), m free in [m0-2, m0+2], connected graphs only
import sys, os, subprocess, json, re, glob, concurrent.futures as cf
from common import *
nlo, nhi, iters, workers, tag, nstarts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
d = json.load(open('out/glue_main.json'))['best']
jobs = []
os.makedirs('out/starts', exist_ok=True)
for n in range(nlo, nhi + 1):
    L = d.get(str(n), [])
    seen = set(); k = 0
    for g in sorted(L, key=lambda x: x['slack']):
        key = (g['m'], g['slack'])
        if key in seen: continue
        seen.add(key)
        f = 'out/starts/%s_%d_%d.txt' % (tag, n, k); open(f, 'w').write(line(n, [tuple(e) for e in g['edges']]) + "\n")
        jobs.append((n, g['m'], g['slack'], f)); k += 1
        if k >= nstarts: break
def run(job):
    n, m0, s0, f = job
    env = dict(os.environ, I11_OUT='out/low_sa2_%s.txt' % tag, I11_CONN='1', I11_DMAX='5')
    p = subprocess.run([I11, 'anneal', str(n), str(iters), str(7 + n * 31 + m0), '1.6', '0.3', '1.5', f, str(max(m0 - 2, (n - 1 + 1) // 2)), str(min(n - 2, m0 + 2))], capture_output=True, text=True, env=env, timeout=7200)
    o = p.stdout
    mm = re.search(r'best_slack=(-?\d+) \(m=(\d+) tau=(\d+)\) visits_slack<=1=(\d+)', o)
    if not mm: return dict(n=n, m0=m0, s0=s0, err=p.stderr[:200])
    return dict(n=n, m0=m0, start_slack=s0, best_slack=int(mm.group(1)), m=int(mm.group(2)), tau=int(mm.group(3)), visits_le1=int(mm.group(4)), best_graph=o.strip().split('\n')[-1][5:])
res = []
with cf.ThreadPoolExecutor(workers) as ex:
    for r in ex.map(run, jobs):
        res.append(r); print({k: v for k, v in r.items() if k != 'best_graph'}, flush=True)
        if r.get('best_slack', 0) < 0: print('!!! NEGATIVE', r, flush=True)
json.dump(res, open('out/sa2_%s.json' % tag, 'w'))
