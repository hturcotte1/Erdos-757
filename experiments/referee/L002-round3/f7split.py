"""Referee round 3: classify patterns (lines 'm i,j,k ...') by F7 containment.
F7 = {012,034,056,135,246}: a centre c lying in three edges ('arms', pairwise meeting only in c by linearity)
plus two edges avoiding c, each meeting every arm in exactly one vertex, the two being disjoint.
Usage: python3 f7split.py in.txt.gz free_out.txt.gz  -> prints counts by (m, f7) and writes F7-free lines."""
import sys, gzip
from collections import Counter
from itertools import combinations


def has_f7(edges):
    E = [frozenset(e) for e in edges]
    inc = {}
    for e in E:
        for v in e:
            inc.setdefault(v, []).append(e)
    for c, es in inc.items():
        if len(es) < 3:
            continue
        for arms in combinations(es, 3):
            A = [a - {c} for a in arms]
            if (A[0] & A[1]) or (A[0] & A[2]) or (A[1] & A[2]):
                continue
            trans = [e for e in E if c not in e and all(len(e & a) == 1 for a in A)]
            for s, u in combinations(trans, 2):
                if not (s & u):
                    return True
    return False


if __name__ == '__main__':
    cnt = Counter()
    with gzip.open(sys.argv[1], 'rt') as fi, gzip.open(sys.argv[2], 'wt') as fo:
        for line in fi:
            f = line.split()
            m = int(f[0])
            es = [tuple(map(int, t.split(','))) for t in f[1:]]
            h = has_f7(es)
            cnt[(m, h)] += 1
            if not h:
                fo.write(' '.join(f[1:]) + '\n')
    for k in sorted(cnt):
        print('m=%d f7=%d count=%d' % (k[0], k[1], cnt[k]))
