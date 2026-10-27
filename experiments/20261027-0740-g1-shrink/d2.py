"""(D2) trace patterns: H - v has two special components F1, F2; all three edges at v meet V(F1) u V(F2).
For every unordered pair of pieces: enumerate all triples of edge types (a_j in F1, b_j in F2, outer rest) satisfying
Claim B (no pair of minimum transversals T1, T2 meets every edge at v), then test sub-extensions
(S in {F1+F2, F1, F2}, Q' = vertices of the edges J not in S) with I11 (n<=27) and with KT-minimality.
usage: python3 d2.py i j   (piece indices, i<=j)  or  python3 d2.py all <maxpairs>"""
import sys, json, itertools, time
from g1lib import *
from kt import deficiency, A_value
from d1 import parts_of
PIECES = load_pieces()

class Side:
    def __init__(self, P):
        self.P = P
        self.minT = min_transversals(masks(P.edges), P.tau)
        self.parts = [()] + parts_of(P)
        self.s = slack(P.n, P.m, P.tau)

def make_types(S1, S2):
    n2T = len(S2.minT); full2 = (1 << n2T) - 1
    types = []
    for a in S1.parts:
        for b in S2.parts:
            sz = len(a) + len(b)
            if sz < 1 or sz > 2: continue
            am = sum(1 << x for x in a); bm = sum(1 << x for x in b)
            cov1 = sum(1 << i for i, T in enumerate(S1.minT) if T & am)
            cov2 = sum(1 << j for j, T in enumerate(S2.minT) if T & bm)
            C = 0
            for i in range(len(S1.minT)):
                row = full2 if (cov1 >> i) & 1 else cov2
                C |= row << (i * n2T)
            types.append(dict(a=a, b=b, am=am, bm=bm, out=2 - sz, nf1=len(b) + 2 - sz, nf2=len(a) + 2 - sz,
                              cov1=cov1, cov2=cov2, C=C))
    return types

def build_full(S1, S2, ts):
    """returns n, edges, vertex sets: V1 = 0..n1-1, V2 = n1..n1+n2-1, v, outer ids; vedges list of (type, edge tuple, outer list)"""
    P1, P2 = S1.P, S2.P
    n1, n2 = P1.n, P2.n
    edges = list(P1.edges) + [tuple(x + n1 for x in e) for e in P2.edges]
    v = n1 + n2; nxt = v + 1; ved = []
    for t in ts:
        vs = [v] + list(t['a']) + [x + n1 for x in t['b']]
        o = []
        while len(vs) < 3: vs.append(nxt); o.append(nxt); nxt += 1
        edges.append(tuple(vs)); ved.append((t, tuple(vs), o))
    return nxt, edges, ved

def heavy(S1, S2, ts, stats, mode='I'):
    """exact sub-extension tests for one Claim-B pattern.  returns dict kill info or None"""
    P1, P2 = S1.P, S2.P
    n1, n2 = P1.n, P2.n
    n, edges, ved = build_full(S1, S2, ts)
    v = n1 + n2
    V1 = set(range(n1)); V2 = set(range(n1, n1 + n2))
    W1 = -A_value(P1.n, P1.m, P1.tau); W2 = -A_value(P2.n, P2.m, P2.tau)
    inC = None
    res = None
    for Sname in ('both', 'F1', 'F2'):
        for J in range(1, 8):
            Js = [j for j in range(3) if (J >> j) & 1]
            Qp = set()
            for j in Js:
                for x in ved[j][1]:
                    if x == v: continue
                    if Sname == 'both' and (x in V1 or x in V2): continue
                    if Sname == 'F1' and x in V1: continue
                    if Sname == 'F2' and x in V2: continue
                    Qp.add(x)
            base = set([v]) | Qp
            if Sname in ('both', 'F1'): base |= V1
            if Sname in ('both', 'F2'): base |= V2
            if Sname == 'F1' and not any(x in V1 for (_, vs, _) in ved for x in vs): continue
            if Sname == 'F2' and not any(x in V2 for (_, vs, _) in ved for x in vs): continue
            nn = len(base)
            nQ2 = len(Qp & V2); nQ1 = len(Qp & V1)
            exact = (Sname == 'F1' and nQ2 >= 3) or (Sname == 'F2' and nQ1 >= 3)
            if not exact:
                inc = [x for x in range(3) if all((y == v) or (y in base) for y in ved[x][1])]
                mm = (P1.m if Sname in ('both', 'F1') else 0) + (P2.m if Sname in ('both', 'F2') else 0) + len(inc)
                if Sname == 'both':
                    t = 0 if (not inc or (ts[inc[0]]['C'] if len(inc) == 1 else __import__('functools').reduce(lambda x, y: x & y, [ts[x]['C'] for x in inc]))) else 1
                elif Sname == 'F1':
                    t = 0 if (not inc or (all(ts[x]['a'] for x in inc) and __import__('functools').reduce(lambda x, y: x & y, [ts[x]['cov1'] for x in inc]))) else 1
                else:
                    t = 0 if (not inc or (all(ts[x]['b'] for x in inc) and __import__('functools').reduce(lambda x, y: x & y, [ts[x]['cov2'] for x in inc]))) else 1
                tauS = (P1.tau if Sname in ('both', 'F1') else 0) + (P2.tau if Sname in ('both', 'F2') else 0)
                tauB = tauS + t
                sB = slack(nn, mm, tauB); AB = A_value(nn, mm, tauB)
                if (mode == 'I' and (sB >= 0 or nn > 27)) or (mode == 'K' and AB >= 0): continue
                Uv = sorted(base); nn, ee = induced(n, edges, Uv)
                assert len(ee) == mm
            else:
                Uv = sorted(base); nn, ee = induced(n, edges, Uv)
                tauB = tau_masks(masks(ee))
                sB = slack(nn, len(ee), tauB); AB = A_value(nn, len(ee), tauB)
            kill_I = (mode == 'I') and sB < 0 and nn <= 27
            kill_K = False; PB = None
            if mode == 'K' and AB < 0:
                # quick lower bound: DEF >= W(S pieces) - 35 * #(included v-edges meeting S)
                Wsum = (W1 if Sname in ('both', 'F1') else 0) + (W2 if Sname in ('both', 'F2') else 0)
                nmeet = 0
                for x in range(3):
                    vs = ved[x][1]
                    if any((y in V1 and Sname in ('both', 'F1')) or (y in V2 and Sname in ('both', 'F2')) for y in vs) and all((y == v) or (y in base) for y in vs): nmeet += 1
                if AB + max(0, Wsum - 35 * nmeet) >= 0: continue
                PB = AB + deficiency(nn, ee, PIECES, proper=True)
                kill_K = PB < 0
            if not (kill_I or kill_K): continue
            # variants with an unknown extra edge g inside Q' (>=1 outer vertex, no two on one v-edge)
            edge_of = {}
            for (t, vs, o) in ved:
                for x in vs:
                    if x != v: edge_of[x] = vs
            outer_set = set(x for (_, _, o) in ved for x in o)
            killI_all = kill_I; killK_all = kill_K
            for g in itertools.combinations(sorted(Qp), 3):
                if not (set(g) & outer_set): continue
                if len({edge_of[x] for x in g}) < 3: continue
                idx = {x: i for i, x in enumerate(Uv)}
                ee2 = ee + [tuple(idx[x] for x in g)]
                if not in_C(nn, ee2): continue
                tau2 = tau_masks(masks(ee2))
                if slack(nn, len(ee2), tau2) >= 0: killI_all = False
                if A_value(nn, len(ee2), tau2) + deficiency(nn, ee2, PIECES, proper=True) >= 0: killK_all = False
            if not (killI_all or killK_all): continue
            if inC is None: inC = in_C(n, edges)
            info = dict(S=Sname, J=J, n=nn, m=len(ee), tau=tauB, s=sB, A=AB, P=PB, killI=killI_all, killKT=killK_all, inC=inC)
            return info
    return None

def run_pair(S1, S2, store_limit=2000, verbose=True):
    t0 = time.time()
    types = make_types(S1, S2)
    W1 = -A_value(S1.P.n, S1.P.m, S1.P.tau); W2 = -A_value(S2.P.n, S2.P.m, S2.P.tau)
    n12 = S1.P.n + S2.P.n + 1
    N = len(types)
    cnt = dict(types=N, claimB=0, candidates=0, killed_I11_or_KT=0, killed_I11=0, killed_KT_only=0, killed_notC_only=0)
    kills = []; surv_examples = []
    s1, s2 = S1.s, S2.s
    for i in range(N):
        ti = types[i]
        for j in range(i + 1, N):
            tj = types[j]
            if ti['am'] & tj['am'] or ti['bm'] & tj['bm']: continue
            Cij = ti['C'] & tj['C']
            am2 = ti['am'] | tj['am']; bm2 = ti['bm'] | tj['bm']
            for k in range(j + 1, N):
                tk = types[k]
                if am2 & tk['am'] or bm2 & tk['bm']: continue
                if not (am2 | tk['am']) or not (bm2 | tk['bm']): continue
                if Cij & tk['C']: continue            # coverable: Claim B fails
                cnt['claimB'] += 1
                ts = (ti, tj, tk)
                # cheap necessary condition for any kill (t <= 1 everywhere; forced F2-edges -> candidate)
                cand = False
                for J in range(1, 8):
                    Js = [x for x in range(3) if (J >> x) & 1]
                    # both
                    oJ = sum(ts[x]['out'] for x in Js)
                    inc = [x for x in range(3) if x in Js or ts[x]['out'] == 0]
                    k_ = len(inc)
                    tb = 0 if k_ <= 1 else 1
                    if -(W1 + W2) + 27 * (1 + oJ) + 35 * k_ - 132 * tb < 0: cand = True; break
                    if s1 + s2 + 3 * (1 + oJ) + 2 * k_ - 11 * tb < 0: cand = True; break
                    # F1 only
                    q1 = sum(ts[x]['nf1'] for x in Js); inc1 = [x for x in range(3) if x in Js or ts[x]['nf1'] == 0]
                    if any(ts[x]['a'] for x in range(3)):
                        tb = 0 if (len(inc1) <= 1 and all(ts[x]['a'] for x in inc1)) else 1
                        if q1 >= 3 or -W1 + 27 * (1 + q1) + 35 * len(inc1) - 132 * tb < 0 or s1 + 3 * (1 + q1) + 2 * len(inc1) - 11 * tb < 0: cand = True; break
                    q2 = sum(ts[x]['nf2'] for x in Js); inc2 = [x for x in range(3) if x in Js or ts[x]['nf2'] == 0]
                    if any(ts[x]['b'] for x in range(3)):
                        tb = 0 if (len(inc2) <= 1 and all(ts[x]['b'] for x in inc2)) else 1
                        if q2 >= 3 or -W2 + 27 * (1 + q2) + 35 * len(inc2) - 132 * tb < 0 or s2 + 3 * (1 + q2) + 2 * len(inc2) - 11 * tb < 0: cand = True; break
                if not cand: continue
                cnt['candidates'] += 1
                r = heavy(S1, S2, ts, cnt, 'I') or heavy(S1, S2, ts, cnt, 'K')
                if r:
                    cnt['killed_I11_or_KT'] += 1
                    cnt['killed_I11' if r['killI'] else 'killed_KT_only'] += 1
                    if len(kills) < store_limit:
                        kills.append(dict(types=[[list(t['a']), list(t['b'])] for t in ts], **r))
    cnt['time_s'] = round(time.time() - t0, 1)
    if verbose: print(S1.P.name, S2.P.name, cnt, flush=True)
    return cnt, kills

if __name__ == '__main__':
    sides = [Side(P) for P in PIECES]
    if sys.argv[1] == 'all':
        maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        out = {}
        for i in range(maxn):
            for j in range(i, maxn):
                c, k = run_pair(sides[i], sides[j])
                out[sides[i].P.name + ' x ' + sides[j].P.name] = dict(counts=c, kills=k)
        json.dump(out, open('d2_results_small.json', 'w'))
    else:
        i, j = int(sys.argv[1]), int(sys.argv[2])
        run_pair(sides[i], sides[j])
