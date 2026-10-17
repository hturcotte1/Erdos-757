"""Referee L011 r2: re-check, from the definitions in plain Python, the certificates printed by bin/rf for a list of graphs.
For each graph line (paired with its rf line): linearity; tau (by brute force over vertex subsets when --tau is given: no subset
of size tau-1 meets all edges, and a found transversal of size tau); F7 certificate -> an explicit injective map of F7 =
{012,034,056,135,246} whose five image triples are edges; (P3) certificate -> the edge set F has |V(F)| <= |F|+1; disconnection
-> a nonempty proper point set closed under edges.  Usage: python3 -I certify.py N GRAPHFILE RFFILE [--tau] [--inC-full]"""
import sys, re
from itertools import combinations
N = int(sys.argv[1]); G = [l for l in open(sys.argv[2]) if l.strip() and (('(' in l) or l[0].isdigit())]
R = [l for l in open(sys.argv[3]) if l.startswith('tau=')]
dotau = '--tau' in sys.argv; full = '--inC-full' in sys.argv
assert len(G) == len(R), (len(G), len(R))
def edges(l):
    if '(' in l: return [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
    v = list(map(int, l.split())); m = v[0]; return [tuple(v[1 + 3*i: 4 + 3*i]) for i in range(m)]
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
stats = dict(graphs=0, f7_cert_ok=0, p3_cert_ok=0, disc_cert_ok=0, inC_conn=0, tau_ok=0, full_inC_ok=0, bad=0)
for gl, rl in zip(G, R):
    E = edges(gl); S = set(frozenset(e) for e in E); stats['graphs'] += 1
    assert len(S) == len(E) and all(len(set(e)) == 3 for e in E)
    lin = all(len(a & b) <= 1 for a, b in combinations(S, 2))
    d = dict(x.split('=', 1) for x in rl.split())
    assert int(d['linear']) == int(lin)
    tau = int(d['tau'])
    if dotau:
        V = sorted(set().union(*S))
        ok = not any(all(set(T) & e for e in S) for T in combinations(V, tau - 1)) if tau >= 1 else True
        ok = ok and any(all(set(T) & e for e in S) for T in combinations(V, tau))
        stats['tau_ok'] += ok
        if not ok: stats['bad'] += 1; print('TAU FAIL', gl.strip())
    if d['f7'] != '-':
        v, a, b, c, i1, i2 = map(int, d['f7'].split(';'))
        ea, eb, ec, t1, t2 = (frozenset(E[i]) for i in (a, b, c, i1, i2))
        Pa, Pb, Pc = sorted(ea - {v}), sorted(eb - {v}), sorted(ec - {v})
        # map: 0->v, (1,2)->Pa in the order given by t1, (3,4)->Pb, (5,6)->Pc
        f = {0: v}
        for (x, y), P in (((1, 2), Pa), ((3, 4), Pb), ((5, 6), Pc)):
            if P[0] in t1: f[x], f[y] = P[0], P[1]
            else: f[x], f[y] = P[1], P[0]
        okf = v in ea and v in eb and v in ec and len(set(f.values())) == 7 and all(frozenset(f[u] for u in e) in S for e in F7)
        stats['f7_cert_ok'] += okf
        if not okf: stats['bad'] += 1; print('F7 CERT FAIL', gl.strip(), rl.strip())
    if int(d['p3']) >= 0:
        mask = int(d['p3']); Fs = [E[i] for i in range(len(E)) if mask >> i & 1]
        okp = len(Fs) >= 1 and len(set().union(*map(set, Fs))) <= len(Fs) + 1
        stats['p3_cert_ok'] += okp
        if not okp: stats['bad'] += 1; print('P3 CERT FAIL', gl.strip())
    comp = int(d['conn'])
    if comp > 1:
        start = E[0][0] if E else 0; R0 = {start}; ch = True
        while ch:
            ch = False
            for e in E:
                if set(e) & R0 and not set(e) <= R0: R0 |= set(e); ch = True
        okd = len(R0) < N
        stats['disc_cert_ok'] += okd
        if not okd: stats['bad'] += 1; print('DISC CERT FAIL', gl.strip())
    if d['f7'] == '-' and int(d['p3']) < 0 and lin:
        if comp == 1: stats['inC_conn'] += 1
        if full:   # independent full re-check of membership in C (slow): F7 over all 5-edge subsets, (P3) over all edge subsets
            okC = True
            for five in combinations(E, 5):
                vs = set().union(*map(set, five))
                if len(vs) != 7: continue
                # brute force: some vertex in exactly 3 of the five, the other two edges avoid it and partition the rest
                for v in vs:
                    at = [e for e in five if v in e]; oth = [set(e) for e in five if v not in e]
                    if len(at) == 3 and len(oth) == 2 and not (oth[0] & oth[1]) and all(len(oth[0] & set(e)) == 1 and len(oth[1] & set(e)) == 1 for e in at):
                        okC = False
            for k in range(1, len(E) + 1):
                for Fs in combinations(E, k):
                    if len(set().union(*map(set, Fs))) <= k + 1: okC = False; break
                if not okC: break
            stats['full_inC_ok'] += okC
            if not okC: stats['bad'] += 1; print('INC FULL FAIL', gl.strip())
print('CERTIFY', sys.argv[2], stats)
