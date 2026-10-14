import json, sys, collections
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/gl-tight-structure')
from lemmas import *
from e757.saturated import map_of_set, edges_of_map
from e757.core import KNOWN, ap_edges, alpha, is_45_set
R = '/home/user/Erdos-757/'
out = {}
def new(): return collections.Counter()
# 1 records
sets = {}
for k, v in json.load(open(R + 'data/small_records.json'))['sets'].items(): sets['rec_' + k] = v['set']
for k, v in KNOWN.items(): sets['KNOWN_' + k[:12]] = v
fails_all = []
st = new()
for name, A in sets.items():
    A = sorted(A); n = len(A); lo, hi, mid = map_of_set(A)
    edges = [tuple(sorted(e)) for e in edges_of_map(mid)]
    tau = n - alpha(A)
    s = new()
    f = check_all(n, edges, s, name)
    print(name, 'n', n, 'm', len(edges), 'tau', tau, 'GLtight', tau == n // 2 - 1 if n % 2 == 0 else 'odd', dict(s), f)
    st.update(s); fails_all += [(name, x) for x in f]
out['records'] = dict(st)
# 2a witnesses
st = new()
W = json.load(open(R + 'experiments/20261014-0500-slack-landscape/witnesses.json'))
nw = 0
for kind in W:
    for key, w in W[kind].items():
        n, m = w['n'], w['m']
        if n % 2 == 0 and m == n - 2 and w['tau'] == n // 2 - 1:
            nw += 1; f = check_all(n, w['edges'], st, (kind, key)); fails_all += [((kind, key), x) for x in f]
print('witness cells', nw, dict(st)); out['witnesses'] = dict(st)
# 2b census
st = new(); cnt = 0
for line in open(R + 'experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl'):
    line = line.strip()
    if not line: continue
    try: e = json.loads(line)
    except Exception: continue
    edges = e if isinstance(e, list) else e['edges']
    cnt += 1
    f = check_all(12, edges, st, cnt); fails_all += [(('census', cnt), x) for x in f]
print('census lines', cnt, dict(st)); out['census'] = dict(st)
json.dump({'summary': out, 'failures': fails_all[:50], 'nfail': len(fails_all)}, open('main_results.json', 'w'), indent=1, default=str)
print('FAILURES', len(fails_all), fails_all[:5])
