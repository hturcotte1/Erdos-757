"""L026 C11: the minimality-free identities of Theorem 12(i),(j) (12.9, 12.10) on the stored hubs.
For every stored E1-hub H = G' (+) (a,b,c) (connected Delta<=3 G' with A(G') <= 15, b-configuration, H in C_3)
and every outer vertex t of G'-degree 2 with partners p, q:
  C_hub = component of H - t containing v, Q = C_hub - {v,x,y,z};
  if p, q non-adjacent: M = Q + w + {w,p,q} must be in C_3, connected, with tau(C_hub) = tau(M) + 1 and
     A(M) = A(C_hub) - 19;
  always: tau(C_hub) = tau(Q) + 1 if some minimum transversal of Q meets {p,q}, else tau(Q) + 2.
Usage: python3 replacement_check.py <cell files ...>"""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
st = dict(hubs=0, deg2=0, nonadj=0, M_inC3=0, id_ok=0, id_fail=0, tauQ_ok=0, tauQ_fail=0)
for f in sys.argv[1:]:
    for E in L.read_found(f):
        n = L.nv(E); m = len(E); d = L.degs(n, E)
        if max(d) > 3 or len(L.components(n, E)) != 1: continue
        t0 = L.tau(E)
        if L.A_val(n, m, t0) > 15: continue
        T = L.all_min_transversals(E, t0)
        co = set()
        for tr in T:
            vs = [i for i in range(n) if tr >> i & 1]
            for pr in itertools.combinations(vs, 2): co.add(pr)
        adj = [set() for _ in range(n)]
        for e in E:
            for u in e:
                for w in e:
                    if u != w: adj[u].add(w)
        Es = set(tuple(sorted(e)) for e in E)
        low = [u for u in range(n) if d[u] <= 2]
        for a, b, c in itertools.combinations(low, 3):
            if (a, b) in co or (a, c) in co or (b, c) in co or (a, b, c) in Es: continue
            nH, EH = L.hub(n, E, a, b, c)
            if not L.in_C3(nH, EH): continue
            st['hubs'] += 1
            v, x, y, z = n, n + 1, n + 2, n + 3
            for tv, (p, q) in ((a, (b, c)), (b, (a, c)), (c, (a, b))):
                if d[tv] != 2: continue
                st['deg2'] += 1
                keep = [u for u in range(nH) if u != tv]
                Ew = L.induced(EH, keep)
                comps = L.components(len(keep), Ew)
                Ch = [C for C in comps if keep.index(v) in C][0]
                Chv = [keep[i] for i in Ch]
                E_ch = L.induced(EH, Chv)
                tau_ch = L.tau(E_ch); A_ch = L.A_val(len(Chv), len(E_ch), tau_ch)
                Qv = [u for u in Chv if u not in (v, x, y, z)]
                E_Q = L.induced(EH, Qv)
                tQ = L.tau(E_Q) if E_Q else 0
                TQ = L.all_min_transversals(E_Q, tQ) if E_Q else [0]
                ip, iq = Qv.index(p), Qv.index(q)
                meets = any((tr >> ip & 1) or (tr >> iq & 1) for tr in TQ)
                if tau_ch == tQ + (1 if meets else 2): st['tauQ_ok'] += 1
                else: st['tauQ_fail'] += 1; print('TAUQ FAIL', E, (a, b, c), tv)
                if q in adj[p]: continue
                st['nonadj'] += 1
                wv = len(Qv)
                EM = E_Q + [(wv, ip, iq)]
                nM = len(Qv) + 1
                ok = L.in_C3(nM, EM) and len(L.components(nM, EM)) == 1
                if ok: st['M_inC3'] += 1
                tM = L.tau(EM); AM = L.A_val(nM, len(EM), tM)
                if tau_ch == tM + 1 and AM == A_ch - 19: st['id_ok'] += 1
                else: st['id_fail'] += 1; print('ID FAIL', E, (a, b, c), tv, tau_ch, tM, A_ch, AM)
    print(f.split('/')[-1], st, flush=True)
print('TOTAL', st)
