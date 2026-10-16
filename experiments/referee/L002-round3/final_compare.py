"""Referee round 3: combine the per-split SAT model files, classify F7 (own test), compare the F7-free set with the
census DFS output, check reflection closure / self-symmetry, and write all models as 'i,j,k ...' lines for ./vr.
Usage: python3 final_compare.py scratchdir"""
import sys, gzip, json, hashlib
from f7split import has_f7
S = sys.argv[1]
N = 12
allm = set(); free = set(); f7c = 0; lines = 0
for k in range(2, 12):
    for l in gzip.open('%s/sat_k%d.txt.gz' % (S, k), 'rt'):
        lines += 1
        es = tuple(sorted(tuple(map(int, x.split(','))) for x in l.split()))
        assert len(es) == 10 and es not in allm
        allm.add(es)
        if has_f7(es):
            f7c += 1
        else:
            free.add(es)
census = set()
for l in gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/n12_m10_all.jsonl.gz', 'rt'):
    census.add(tuple(sorted(map(tuple, json.loads(l)))))
refl = lambda es: tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for (i, j, k) in es))
closed = all(refl(e) in allm for e in allm)
selfsym = sum(1 for e in allm if refl(e) == e)
canon = sum(1 for e in free if e <= refl(e))
print('SAT models: lines=%d distinct=%d f7=%d f7free=%d' % (lines, len(allm), f7c, len(free)))
print('census=%d census-minus-SATfree=%d SATfree-minus-census=%d' % (len(census), len(census - free), len(free - census)))
print('reflection-closed=%s self-symmetric=%d f7free_up_to_reflection=%d' % (closed, selfsym, canon))
with gzip.open('%s/sat_all_lines.txt.gz' % S, 'wt') as fo:
    for e in sorted(allm):
        fo.write(' '.join('%d,%d,%d' % t for t in e) + '\n')
