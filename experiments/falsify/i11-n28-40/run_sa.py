# simulated annealing per window cell (n,m): maximise tau (exact) with a log-count tie-breaker, connected graphs only, class C maintained incrementally.
import sys, os, subprocess, json, re, collections, concurrent.futures as cf
from common import *
nlo, nhi, iters, workers, tag = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
reps = int(sys.argv[6]) if len(sys.argv) > 6 else 1
seed0 = int(sys.argv[7]) if len(sys.argv) > 7 else 100
dmax = os.environ.get('I11_DMAX', '3')
def cells(n):
    out = []
    for m in range(0, n - 1):
        lo = (3 * n + 2 * m) // 11 + 1; hy = (5 * n + 3 * m) // 17
        if lo <= min(hy, m) and n <= 2 * m + 1: out.append((m, lo))
    return out
jobs = [(n, m, lo, r) for n in range(nlo, nhi + 1) for (m, lo) in cells(n) for r in range(reps)]
def run(job):
    n, m, lo, r = job
    env = dict(os.environ, I11_OUT='out/low_sa_%s.txt' % tag, I11_CONN='1', I11_DMAX=dmax)
    lam = [1.5, 2.5, 1.0][r % 3]
    p = subprocess.run([I11, 'anneal', str(n), str(iters), str(seed0 + 1000 * n + 10 * m + r), '2.5', '0.3', str(lam), '-', str(m), str(m)], capture_output=True, text=True, env=env, timeout=7200)
    o = p.stdout
    mm = re.search(r'best_slack=(-?\d+) \(m=(\d+) tau=(\d+)\) visits_slack<=1=(\d+)', o)
    return dict(n=n, m=m, lo=lo, rep=r, best_slack=int(mm.group(1)), tau=int(mm.group(3)), visits_le1=int(mm.group(4)), evals=int(re.search(r'evals=(\d+)', o).group(1)),
                need_tau=lo, best_graph=o.strip().split('\n')[-1][5:])
res = []
with cf.ThreadPoolExecutor(workers) as ex:
    for r in ex.map(run, jobs):
        res.append(r); print(r['n'], r['m'], 'lo', r['lo'], 'best_slack', r['best_slack'], 'tau', r['tau'], 'evals', r['evals'], flush=True)
        if r['best_slack'] < 0: print('!!! NEGATIVE SLACK', r, flush=True)
json.dump(res, open('out/sa_%s.json' % tag, 'w'))
