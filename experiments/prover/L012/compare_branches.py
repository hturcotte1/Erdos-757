"""(L012) Compare every extension branch of the prover's engine (inputs, F7-free hits, hits in C) with the falsifier's EXT lines
(graphs, finals_after_F7, hits_after_hall).  These counts are isomorphism invariants of the input lists, so they must agree exactly
when the class lists agree."""
import re, sys, ast
mine = {}
for l in open('out/engine.log'):
    m = re.match(r'\s*BRANCH \((\d+), (\d+), (\d+), (\d+)\) d=(\d+) tp=(\d+) .*inputs=(\d+) (\{.*\})?', l)
    if m:
        k = tuple(map(int, m.groups()[:6])); ext = ast.literal_eval(m.group(8)) if m.group(8) else {}
        mine[k] = (int(m.group(7)), ext.get('hits_F7free', 0), ext.get('hits_in_C', 0))
theirs = {}
F = '/home/user/Erdos-757/experiments/20261017-1030-n23-record-cell/'
for f in sys.argv[1:]:
    for l in open(F + f):
        m = re.match(r'\s*EXT c_(\d+)_(\d+)_(\d+)_D(\d+)_d(\d+)_tp(\d+) SUMMARY graphs=(\d+) .*finals_after_F7=(\d+) hits_after_hall=(\d+)', l)
        if m:
            g = list(map(int, m.groups())); theirs[tuple(g[:6])] = (g[6], g[7], g[8])
        m = re.match(r"\s*RECURSE \((\d+), (\d+), (\d+), (\d+)\) d=(\d+) tau'=(\d+) slack'=(\d+) partitions=(\d+) G-prime=0", l)
        if m:
            g = list(map(int, m.groups())); theirs.setdefault(tuple(g[:6]), (0, 0, 0))
common = sorted(set(mine) & set(theirs))
diff = [(k, mine[k], theirs[k]) for k in common if mine[k] != theirs[k]]
print('prover branches', len(mine), '| falsifier branches', len(theirs), '| common', len(common), '| different', diff)
print('only prover:', [(k, mine[k]) for k in sorted(set(mine) - set(theirs))])
print('only falsifier:', [(k, theirs[k]) for k in sorted(set(theirs) - set(mine))])
