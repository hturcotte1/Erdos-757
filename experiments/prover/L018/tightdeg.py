import re, glob, collections
from hg import tau_of, degrees, in_class_C
def load(fn):
    G = []
    for line in open(fn):
        if not line.startswith('FOUND'): continue
        E = [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)]
        G.append(E)
    return G
for fn in sorted(glob.glob('cells13/cells/*.txt')):
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
