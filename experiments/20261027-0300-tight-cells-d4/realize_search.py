"""[bonus] Realizability of the connected hypergraphs of a cell file as (4,5)-sets with exactly these 3-APs.
Backtracking over midpoint labelings (each edge: which vertex is the middle; midpoints pairwise distinct), pruning with a generic point of the
solution space of the AP equations mod p = 2^61-1 (forced equal points, forced weak-Sidon violation x_a+x_b=x_c+x_d for {a,b}!={c,d}, a!=b, c!=d).
Leaves are re-checked exactly (e757.core.realize: rational generic point, extra APs, is_45_set).  usage: realize_search.py cellfile n timelimit_s"""
import sys, re, random, time, itertools
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import realize
P = (1 << 61) - 1
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def nullspace_point(rows, n, rnd):
    # rows: list of dict col->coef (ints). returns random vector in the nullspace mod P (list) or None if empty.
    M = [[r.get(c, 0) % P for c in range(n)] for r in rows]; piv = []; r0 = 0
    for c in range(n):
        pr = None
        for i in range(r0, len(M)):
            if M[i][c]: pr = i; break
        if pr is None: continue
        M[r0], M[pr] = M[pr], M[r0]; inv = pow(M[r0][c], P - 2, P); M[r0] = [x * inv % P for x in M[r0]]
        for i in range(len(M)):
            if i != r0 and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % P for x, y in zip(M[i], M[r0])]
        piv.append(c); r0 += 1
    free = [c for c in range(n) if c not in piv]
    x = [0] * n
    for f in free: x[f] = rnd.randrange(P)
    for i, c in enumerate(piv):
        x[c] = (-sum(M[i][f] * x[f] for f in free)) % P
    return x
def ok_point(x, n):
    if len(set(x)) < n: return False
    seen = set()
    for a in range(n):
        for b in range(a + 1, n):
            s = (x[a] + x[b]) % P
            if s in seen: return False
            seen.add(s)
    return True
def search(E, n, tlimit, seed=0):
    rnd = random.Random(seed); m = len(E); t0 = time.time(); stats = dict(nodes=0, leaves=0, timeout=False)
    # order edges by BFS over vertices
    order = []; rem = list(range(m)); cov = set()
    while rem:
        best = max(rem, key=lambda i: (len(cov & set(E[i])), -i)); order.append(best); rem.remove(best); cov |= set(E[best])
    lab = [None] * m; used = set(); rows = []; found = []
    def rec(k):
        if time.time() - t0 > tlimit: stats['timeout'] = True; return True
        if k == m:
            stats['leaves'] += 1
            labeled = [lab[i] for i in range(m)]
            ok, res = realize(labeled, n, tries=3, seed=1)
            if ok: found.append((labeled, res)); return True
            return False
        i = order[k]; e = E[i]
        for mid in e:
            if mid in used: continue
            a, c = [v for v in e if v != mid]
            row = {a: 1, c: 1, mid: -2}
            stats['nodes'] += 1
            x = nullspace_point(rows + [row], n, rnd)
            if not ok_point(x, n): continue
            lab[i] = (a, mid, c); used.add(mid); rows.append(row)
            if rec(k + 1): return True
            rows.pop(); used.discard(mid); lab[i] = None
        return False
    rec(0)
    return found, stats, round(time.time() - t0, 1)
if __name__ == '__main__':
    fn, n, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    for ci, l in enumerate([l for l in open(fn) if l.startswith('FOUND:')]):
        found, stats, secs = search(parse(l), n, tl)
        print('class', ci, 'REALIZED' if found else ('TIMEOUT' if stats['timeout'] else 'NOT-REALIZABLE'), stats, secs, 's', (found[0][1] if found else ''), flush=True)
