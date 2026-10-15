"""Referee L004, check E: reproducibility of stored per-prefix outputs. Re-runs the census engine (fresh build of the
committed source HEAD:e757/c/ordered_dfs.c -> ./census_bin) on a random sample of prefixes, with the same arguments
as the driver (n=14 T=8 m_min=12 m_exact=12 f7=1 progress=0 refl=1 mode=enum pre=<prefix>), and compares the
solution set, nodes, leaves and solutions with the stored .jsonl.gz / .done files.
usage: python3 rerun_engine.py K MAXTIME SEED"""
import json, gzip, os, random, subprocess, sys, time
K, MAXT, SEED = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
R = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/n14/results'
HERE = os.path.dirname(os.path.abspath(__file__))
pl = open(os.path.join(R, 'n14_m12_prefixes.txt')).read().split()
cand = []
EXCL = set(json.load(open(os.path.join(HERE, 'cube_sets.json')))['sample_idx'])
for q, p in enumerate(pl):
    d = json.load(open(os.path.join(R, 'n14_m12_prefix_%05d.done' % q)))
    if 10 < float(d["time"]) <= MAXT and q not in EXCL: cand.append(q)
random.seed(SEED)
pick = sorted(random.sample(cand, K))
bad = 0; t0 = time.time()
for q in pick:
    d = json.load(open(os.path.join(R, 'n14_m12_prefix_%05d.done' % q)))
    out = subprocess.run(['nice', '-n', '10', os.path.join(HERE, 'census_bin'), 'n=14', 'T=8', 'm_min=12', 'm_exact=12', 'f7=1',
                          'progress=0', 'refl=1', 'mode=enum', 'pre=' + pl[q]], capture_output=True, text=True, check=True).stdout
    sols = set(); st = {}
    for l in out.splitlines():
        if l.startswith('SOL'):
            sols.add(tuple(sorted(tuple(map(int, t.split(','))) for t in l.split()[2:])))
        elif l.startswith('DONE'):
            st = dict(kv.split('=') for kv in l.split()[1:])
    stored = set(tuple(sorted(tuple(e) for e in json.loads(l))) for l in gzip.open(os.path.join(R, 'n14_m12_prefix_%05d.jsonl.gz' % q), 'rt'))
    same = (sols == stored and st['nodes'] == d['nodes'] and st['leaves'] == d['leaves'] and st['solutions'] == d['solutions'])
    bad += not same
    print(q, pl[q], 'sols', len(sols), 'nodes', st['nodes'], 'stored', d['nodes'], 'leaves', st['leaves'], d['leaves'], 'SAME' if same else 'DIFF', flush=True)
print('rerun prefixes', len(pick), 'differences', bad, 'time %.0f' % (time.time() - t0))
