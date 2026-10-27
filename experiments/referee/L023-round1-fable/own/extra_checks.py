"""Extra own checks: (1) Q8 == the 6 lines of AG(2,3) through two points a,b other than ab, on the 8 points other than the third point
of ab; (2) H(A_base) and H(C25) contain no Q8; (3) second proof of Theorem 3: for each X_i and each degree-4 vertex w whose deletion
leaves a (14,12,6) component K, K is isomorphic to entry 5 or 7 (0-based) of the archived refereed list cell(14,12,6,4), and K is
NOT realizable by my SDR decider (counts 807/667/140 or 799/587/212 expected)."""
import re, sys, json
from itertools import combinations, product
sys.argv = ['x']
import importlib.util
spec = importlib.util.spec_from_file_location('ro', 'realize_own.py'); ro = importlib.util.module_from_spec(spec); spec.loader.exec_module(ro)
spec2 = importlib.util.spec_from_file_location('tl', 'toplevel_own.py'); tl = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(tl)
Q8 = [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 7, 2)]
# (1) AG(2,3)
pts = [(x, y) for x in range(3) for y in range(3)]
lines = set()
for p, q in combinations(pts, 2):
    r = ((2 * q[0] - p[0]) % 3, (2 * q[1] - p[1]) % 3); lines.add(frozenset((p, q, r)))
assert len(lines) == 12
a, b = (0, 0), (1, 0); ab = next(l for l in lines if a in l and b in l); c = next(iter(ab - {a, b}))
six = [l for l in lines if (a in l or b in l) and l != ab]
assert len(six) == 6 and all(c not in l for l in six)
rest = [p for p in pts if p != c]; idx = {p: i for i, p in enumerate(rest)}
E6 = [tuple(sorted(idx[p] for p in l)) for l in six]
print('AG(2,3) piece isomorphic to Q8:', tl.isomorphic(Q8, E6) is not None)
# (2) Q8-freeness of H(A_base), H(C25)
def ap_edges(A):
    return [tuple(sorted((x, y, z))) for x, y, z in combinations(sorted(A), 3) if x + z == 2 * y]
def has_Q8(E):
    V = sorted(set(v for e in E for v in e)); at = {v: [e for e in E if v in e] for v in V}
    for a in V:
        for b in V:
            if a == b: continue
            for ea in combinations(at[a], 3):
                Sa = set(v for e in ea for v in e if v != a)
                if len(Sa) != 6 or b in Sa: continue
                for eb in combinations(at[b], 3):
                    if set(v for e in eb for v in e if v != b) == Sa and a not in Sa: return True
    return False
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B11 = [0, 2009010, 2901878, 3392944, 3459949, 3705482, 3750000, 3794746, 3884010, 4018020, 7500000]
C25 = sorted(A_BASE + [10 ** 9 + 7919 * x for x in B11])
print('Q8 in H(A_base):', has_Q8(ap_edges(A_BASE)), '; Q8 in H(C25):', has_Q8(ap_edges(C25)), '; Q8 in Q8:', has_Q8(Q8))
# (3) 14-vertex pieces
txt = open(ro.CERT).read(); X = []
for line in txt.splitlines():
    m = re.match(r'^X_(\d) FOUND: (.*)$', line.strip())
    if m: X.append([tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', m.group(2))])
L14 = tl.load_list((14, 12, 6, 4)); print('archived cell(14,12,6,4): %d entries' % len(L14))
res14 = {}
for i, E in enumerate(X):
    V = tl.verts(E); d = tl.degrees(E, V)
    for w in V:
        if d[w] != 4: continue
        Ew = [e for e in E if w not in e]; Vw = [u for u in V if u != w]
        adj = {u: set() for u in Vw}
        for e in Ew:
            for x in e:
                for y in e:
                    if x != y: adj[x].add(y)
        seen = set()
        for s in Vw:
            if s in seen: continue
            st = [s]; seen.add(s); comp = {s}
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); comp.add(y); st.append(y)
            EK = [e for e in Ew if set(e) <= comp]
            if len(comp) == 14 and len(EK) == 12:
                cls = [j for j in range(len(L14)) if tl.isomorphic(EK, L14[j]) is not None]
                key = tuple(cls)
                if key not in res14:
                    cnt, reals = ro.realize_sdr(EK); res14[key] = cnt
                print('X_%d - %d: (14,12) component = entry %s of cell(14,12,6,4); realize_sdr %s' % (i, w, cls, json.dumps(res14[key])))
# the other 9 entries of cell(14,12,6,4) are realizable? (control: at least some REAL)
ctl = []
for j in range(len(L14)):
    cnt, reals = ro.realize_sdr(L14[j]); ctl.append((j, cnt['labellings'], cnt['REAL']))
print('cell(14,12,6,4) entries (index, labellings, REAL):', ctl)
