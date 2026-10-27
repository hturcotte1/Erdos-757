import re, glob, collections
from hg import tau_of, degrees, in_class_C
def load(fn):
    G = []
    for line in open(fn):
        if not line.startswith('FOUND'): continue
        E = [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)]
        G.append(E)
    return G
NAMES = ['10_7_4', '12_10_5', '13_8_5', '14_12_6', '15_11_6', '17_13_7', '19_16_8', '22_17_9', '8_5_3']
for fn in ['cells13/cells/cell_%s_D3.txt' % c for c in NAMES]:
    G = load(fn)
    cnt = collections.Counter()
    for E in G:
        d = degrees(E)
        n = len(d); m = len(E); t = tau_of(E)
        s = 3*n + 2*m - 11*t
        conn = True
        ds = collections.Counter(d.values())
        cnt[(n, m, t, s, tuple(sorted(ds.items())))] += 1
    print(fn.split('/')[-1], len(G), sorted(cnt.items()))
