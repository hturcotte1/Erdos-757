"""(2) Q8-violating states in the abstract data: core check.  (3) local free-move types."""
import sys, os, json, gzip, glob, itertools
from collections import Counter, defaultdict
from fractions import Fraction as F
from common import *
sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/q8-abstract')
sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/q8-omega-inequality')
from fastcores import has_core
from e757.cpsat_model import constraint_violations, load_cores
from e757.core import ap_edges
HERE = os.path.dirname(os.path.abspath(__file__))
CORES = load_cores(*sorted(glob.glob('/home/user/Erdos-757/data/forbidden_ordered_n*.json')))
def load(path):
    p = os.path.join(HERE, path)
    return [json.loads(l) for l in gzip.open(p, 'rt')] if os.path.exists(p) else []
def slack(t): return 3 * t['R'] + 2 * t['e2'] + 4 * t['e1'] - 7 * t['tau']
absrows = load('abstract_census_tuples.jsonl.gz') + load('abstract_census_all500_tuples.jsonl.gz') + load('abstract_witness_tuples.jsonl.gz') + load('abstract_fresh_tuples.jsonl.gz')
# ---- (2) violators
viol = {}   # key: edges tuple -> info
for r in absrows:
    for t in r['tuples']:
        if slack(t) < 0:
            key = tuple(map(tuple, r['edges']))
            v = viol.setdefault(key, dict(names=[], n=r['n'], edges=r['edges'], states=[]))
            v['names'].append(r['name']); v['states'].append(dict(t))
print('distinct violating hypergraphs', len(viol))
rep = []
for key, v in viol.items():
    E = [tuple(e) for e in v['edges']]; n = v['n']
    cv = constraint_violations(n, E, True, True, None)
    tags = sorted({x[0] for x in cv})
    fullcore = has_core(n, E)
    cc = None
    if fullcore:
        cv2 = constraint_violations(n, E, False, False, CORES)
        cc = min(len(x[3]) for x in cv2) if cv2 else None
    rep.append(dict(names=v['names'][:3], n=n, edges=v['edges'], K30K31=tags, violates_core=bool(fullcore), min_core_edges_violated=cc, states=v['states']))
surv = [r for r in rep if not r['K30K31'] and not r['violates_core']]
print('violators passing K30,K31 and full core library:', len(surv))
print('violators violating K30/K31:', sum(1 for r in rep if r['K30K31']), ' violating some core:', sum(1 for r in rep if r['violates_core']))
print('min core size violated histogram:', Counter(r['min_core_edges_violated'] for r in rep))
json.dump(dict(n_violating_hypergraphs=len(rep), n_survivors=len(surv), survivors=surv, violators=rep[:200]), open(os.path.join(HERE, 'violators.json'), 'w'), indent=1)
# ---- (3) local types
def traces(E, S, D):
    tr = {e & ~D for e in E if e & S == e}
    return [t for t in tr if not any(u != t and u & t == u for u in tr)]
def local_types(E, S, D):
    K = traces(E, S, D); R = S & ~D; out = []
    for v in range(32):
        if not R >> v & 1: continue
        e = [0, 0, 0, 0]
        for t in K:
            if t >> v & 1: e[bin(t).count('1')] += 1
        out.append((e[3], e[2], e[1]))
    return out
def ftype(ty):
    e3, e2, e1 = ty
    dele = 2 * e2 + 4 * e1 >= 4          # 3/7 + 2/7 e2 + 4/7 e1 >= 1
    avoid = (e1 == 0 and e3 + e2 <= 1)   # 2/7 e3 + 2/7 e2 <= 3/7
    return ('D' if dele else '') + ('A' if avoid else '') or 'HARD'
def summarize(states, label):
    cnt = Counter(); nst = 0; allhard = 0; nverts = 0; hist = Counter(); irr_cnt = Counter(); nR0 = 0
    for E, S, D in states:
        ts = local_types(E, S, D)
        if not ts: nR0 += 1; continue
        nst += 1
        fl = [ftype(t) for t in ts]
        ih = all(x == 'HARD' for x in fl)
        allhard += ih
        if ih:
            hist[len(ts)] += 1
            for t in ts: irr_cnt[t] += 1
        for t, f in zip(ts, fl): cnt[t] += 1; nverts += 1
    return dict(label=label, states=nst, states_with_R_empty_skipped=nR0, vertices=nverts, states_with_no_free_vertex=allhard,
                irreducible_by_R_size=dict(sorted(hist.items())), types={str(k): v for k, v in sorted(cnt.items())},
                types_in_irreducible_states={str(k): v for k, v in sorted(irr_cnt.items())})
def emasks(edges): return [mask(e) for e in edges]
res = {}
# abstract violating states (all examples)
vs = [(emasks(r['edges']), s['S'], s['D']) for r in rep for s in r['states']]
res['abstract_violators'] = summarize(vs, 'abstract Q8-violating states (slack -1), one state per (hypergraph,tuple)')
# abstract tight states (examples, slack 0)
ts_ = []
for r in absrows:
    for t in r['tuples']:
        if slack(t) == 0: ts_.append((emasks(r['edges']), t['S'], t['D']))
res['abstract_tight_examples'] = summarize(ts_, 'abstract slack-0 example states (one per hypergraph per tuple)')
# realizable tight: all equality states of the record sets via q8 binary PRINTEQ
from q8lib import run_cases
real = load('realizable_tuples.jsonl.gz')
rs = []
for r in real:
    if r['src'] != 'record': continue
    ms = emasks(r['edges'])
    out = run_cases([(0, r['n'], ms, 0, 0, 0)], vcap=-1, printeq=True) if False else None
    import subprocess
    inp = f"0 {r['n']} {len(ms)} {' '.join(map(str, ms))} 0 0 0\n"
    o = subprocess.run([os.path.join('/home/user/Erdos-757/experiments/falsify/q8-omega-inequality', 'q8'), '0'], input=inp, capture_output=True, text=True, env=dict(os.environ, PRINTEQ='1')).stdout
    c = 0
    for line in o.splitlines():
        if line.startswith('EQ'):
            kv = dict(x.split('=') for x in line.split()[2:]); rs.append((ms, int(kv['S']), int(kv['D']))); c += 1
    print(r['name'], 'equality states', c)
res['realizable_tight_all_equality_states'] = summarize(rs, 'realizable record sets: ALL Q8-equality states')
# realizable tight from random sets (examples)
rr = []
for r in real:
    if r['src'].startswith('rand'):
        for t in r['tuples']:
            if slack(t) <= 0: rr.append((emasks(r['edges']), t['S'], t['D']))
res['realizable_random_tight_examples'] = summarize(rr, 'random realizable n=12,14: slack-0 example states') if rr else None
json.dump(res, open(os.path.join(HERE, 'local_types.json'), 'w'), indent=1)
for k, v in res.items():
    if v: print(k, v['states'], 'states,', v['vertices'], 'vertices, states with no free vertex:', v['states_with_no_free_vertex'])
