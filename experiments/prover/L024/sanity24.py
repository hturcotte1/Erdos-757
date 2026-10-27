"""L024 sanity checks (own code, hyp24.py; L021's kt.py is not imported).
S1  E1-hubs: for every connected G' with max degree <= 3 and A(G') <= 15 in the six stored cells where the judge's probe
    found b-configurations, every b-configuration {a,b,c} (vertices of degree <= 2, not an edge, no two in a common
    minimum transversal) with H = G' + E1-hub(a,b,c) in C_3: check tau(H) = tau(G') + 2, A(H) = A(G') - 16, and compute
    DEF(H) exactly (branch and bound to the end) and P(H).  The judge reported 186 such H, all with P = 0.
S2  Identity of Lemma A step 4 / Lemma 4.4: for triples {a,b,c} with two of them in a common minimum transversal and
    H in C_3: tau(H) = tau(G') + 1 and A(H) = A(G') + 116.
S3  Proposition 2 membership: for graphs R of stored cells, R + {p,q,z} (p,q of degree <= 2 sharing no edge, z new)
    and R + {p,z1,z2} (d(p) <= 2) lie in C_3.
Run: timeout 3000 nice -n 10 python3 sanity24.py > sanity24_output.txt"""
import sys, re, itertools, time, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import *
t0 = time.time()
pieces = load_pieces()
BASE = '/home/user/Erdos-757/experiments/prover/L017/out/'
def read_cell(path):
    out = []
    for l in open(path):
        if l.startswith('FOUND'):
            out.append([tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)])
    return out
def nv(E): return 1 + max(max(e) for e in E)
def connected(n, E):
    adj = [set() for _ in range(n)]
    for e in E:
        for x in e:
            adj[x] |= set(e)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n
cells = ['L012/cells/cell_6_3_2_D3.txt', 'L012/cells/cell_11_7_4_D3.txt', 'L012/cells/cell_12_6_4_D3.txt',
         'L012/cells/cell_13_9_5_D3.txt', 'L013/cells/cell_18_9_6_D3.txt', 'L013/cells/cell_19_12_7_D3.txt']
S1 = dict(hubs=0, tau_ok=0, A_ok=0, P0=0, Pneg=0, Ppos=0); S1cells = {}
S2 = dict(tested=0, ok=0)
hub_cells = {}
for c in cells:
    gs = read_cell(BASE + c)
    cnt = 0
    for E in gs:
        n = nv(E); m = len(E); d = degrees(n, E)
        if max(d) > 3 or not connected(n, E): continue
        t = tau(n, E); A0 = CN * n + CM * m - CT * t
        if A0 > 15: continue
        mts = min_transversals(n, E, t)
        low = [x for x in range(n) if d[x] <= 2]
        co = set()
        for x, y in itertools.combinations(low, 2):
            b = (1 << x) | (1 << y)
            if any(T & b == b for T in mts): co.add((x, y))
        Es = set(E)
        for a, b, cc in itertools.combinations(low, 3):
            if (a, b, cc) in Es: continue
            v, x, y, z = n, n + 1, n + 2, n + 3
            EH = E + [(x, y, z), tuple(sorted((a, v, x))), tuple(sorted((b, v, y))), tuple(sorted((cc, v, z)))]
            nH = n + 4
            bconf = not ((a, b) in co or (a, cc) in co or (b, cc) in co)
            if not bconf:
                if S2['tested'] < 400 and in_C3(nH, EH):
                    S2['tested'] += 1
                    tH = tau(nH, EH)
                    if tH == t + 1 and CN * nH + CM * len(EH) - CT * tH == A0 + 116: S2['ok'] += 1
                continue
            if not in_C3(nH, EH): continue
            S1['hubs'] += 1; cnt += 1
            tH = tau(nH, EH); AH = CN * nH + CM * len(EH) - CT * tH
            if tH == t + 2: S1['tau_ok'] += 1
            if AH == A0 - 16: S1['A_ok'] += 1
            D, fam, ncop = def_certificate(nH, EH, pieces, 10 ** 9)
            P = AH + D
            if P == 0: S1['P0'] += 1
            elif P < 0: S1['Pneg'] += 1; print('NEGATIVE', c, E, (a, b, cc))
            else: S1['Ppos'] += 1
            key = (nH, len(EH), tH)
            hub_cells[key] = hub_cells.get(key, 0) + 1
    S1cells[c] = cnt
    print('S1', c, 'hubs', cnt, S1, f'[{time.time()-t0:.0f}s]', flush=True)
print('S1 TOTAL', S1, 'per G-cell', S1cells, 'H cells', hub_cells, flush=True)
print('S2', S2, flush=True)
# S3
random.seed(2024)
S3 = dict(R=0, two=0, two_ok=0, one=0, one_ok=0)
for c in ['L012/cells/cell_13_9_5_D3.txt', 'L012/cells/cell_15_11_6_D3.txt', 'L012/cells/cell_17_13_7_D3.txt',
          'L013/cells/cell_19_12_7_D3.txt', 'L012/cells/cell_14_12_6_D3.txt', 'L012/cells/cell_12_10_5_D3.txt']:
    gs = read_cell(BASE + c)
    random.shuffle(gs)
    for E in gs[:25]:
        n = nv(E); d = degrees(n, E)
        if max(d) > 3: continue
        S3['R'] += 1
        share = set()
        for e in E:
            for a, b in itertools.combinations(e, 2): share.add((a, b))
        low = [x for x in range(n) if d[x] <= 2]
        for p, q in itertools.combinations(low, 2):
            if (p, q) in share: continue
            S3['two'] += 1
            if in_C3(n + 1, E + [(p, q, n)]): S3['two_ok'] += 1
        for p in low:
            S3['one'] += 1
            if in_C3(n + 2, E + [(p, n, n + 1)]): S3['one_ok'] += 1
    print('S3', c, S3, f'[{time.time()-t0:.0f}s]', flush=True)
print('S3 TOTAL', S3)
print('done', f'[{time.time()-t0:.0f}s]')
