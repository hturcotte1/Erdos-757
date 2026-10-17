"""Compare per-graph flags: my genbg hook ('G n= m= tau= f7= p3= C= dmax=:' lines), my definitional hyp.py ('CHK ...' lines)
and the prover's filter_hits (SURVIVOR lines = in C; plus its SUMMARY counts). Graphs are matched by their edge text."""
import sys, re
def parse(path, prefix):
    out = {}
    for l in open(path):
        if not l.startswith(prefix): continue
        head, body = l.split(':', 1)
        d = dict(kv.split('=') for kv in head.split()[1:])
        out[' '.join(re.findall(r'\([\d,]+\)', body))] = d
    return out
g = parse(sys.argv[1], 'G '); c = parse(sys.argv[2], 'CHK ')
surv = {' '.join(re.findall(r'\([\d,]+\)', l.split(':', 1)[1])) for l in open(sys.argv[3]) if l.startswith('SURVIVOR:')}
assert set(g) == set(c), (len(g), len(c))
bad = 0
for k, d in g.items():
    e = c[k]
    for f in ('tau', 'f7', 'p3', 'C', 'dmax'):
        if d[f] != e[f]: bad += 1; print('MISMATCH hook vs definitional', f, d[f], e[f], k)
    if (d['C'] == '1') != (k in surv): bad += 1; print('MISMATCH hook vs prover filter (in C?)', d['C'], k in surv, k)
print(sys.argv[1], 'graphs', len(g), 'inC', sum(d['C'] == '1' for d in g.values()), 'prover survivors', len(surv), 'mismatches', bad)
