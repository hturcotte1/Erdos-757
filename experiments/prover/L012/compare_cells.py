"""(L012) Compare the class counts of every cell computed by the prover's engine (out/engine.log) with the falsifier's engine logs."""
import re, sys
def parse(f):
    d = {}
    for l in open(f):
        m = re.match(r'\s*CELL \((\d+), (\d+), (\d+), (\d+)\) classes (\d+)', l)
        if m: d[tuple(map(int, m.groups()[:4]))] = int(m.group(5))
    return d
mine = parse('out/engine.log')
F = '/home/user/Erdos-757/experiments/20261017-1030-n23-record-cell/'
theirs = {}
for f in sys.argv[1:]: theirs.update(parse(F + f))
common = sorted(set(mine) & set(theirs)); diff = [k for k in common if mine[k] != theirs[k]]
print('prover cells', len(mine), '| falsifier cells', len(theirs), '| common', len(common), '| different counts', diff)
print('only prover:', sorted(set(mine) - set(theirs)))
print('only falsifier:', sorted(set(theirs) - set(mine)))
for k in [(22, 17, 9, 4), (19, 16, 8, 4), (14, 12, 6, 4), (12, 10, 5, 4), (10, 7, 4, 4), (8, 5, 3, 4), (21, 13, 8, 4), (18, 12, 7, 4), (21, 14, 8, 3), (18, 13, 7, 3), (15, 12, 6, 3), (15, 11, 6, 4)]:
    print(k, 'prover', mine.get(k), 'falsifier', theirs.get(k))
