# SA over induced subsets (size s in 28..40) of big class-C hypergraphs that come from (4,5)-sets / disjoint unions; minimise slack = 3s+2m-11tau
import sys, os, subprocess, re, json, glob, concurrent.futures as cf
from common import *
iters, workers, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
bases = sorted(glob.glob('bases/*.txt'))
jobs = []
for b in bases:
    N = int(open(b).readline().split()[0])
    for s in range(28, 41):
        if s < N: jobs.append((b, N, s))
def run(job):
    b, N, s = job
    env = dict(os.environ, I11_OUT='out/low_sub_%s.txt' % tag)
    p = subprocess.run([I11, 'subsa', b, str(s), str(iters), str(11 * s + N), '3.0', '0.4'], capture_output=True, text=True, env=env, timeout=7200)
    m = re.search(r'evals=(\d+) best_slack=(-?\d+)', p.stdout)
    return dict(base=os.path.basename(b)[:-4], N=N, size=s, evals=int(m.group(1)), best_slack=int(m.group(2)))
res = []
with cf.ThreadPoolExecutor(workers) as ex:
    for r in ex.map(run, jobs):
        res.append(r); print(r, flush=True)
        if r['best_slack'] < 0: print('!!! NEGATIVE', r, flush=True)
json.dump(res, open('out/subsa_%s.json' % tag, 'w'))
