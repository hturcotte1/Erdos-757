"""Theorem 3 (L020) case classification at a degree-3 vertex, with direct checks of every stated conclusion.
Own code (imports only hgr2 from this folder)."""
from hgr2 import HG, in_C, popc

def slack(n, m, t):
    return 3 * n + 2 * m - 11 * t

def analyse(K, v):
    fails = []
    eidx = [i for i in range(len(K.E)) if K.inc[v] >> i & 1]
    assert len(eidx) == 3
    P = [tuple(u for u in K.E[i] if u != v) for i in eidx]
    Gmask = K.full & ~K.inc[v]
    GV = [u for u in K.V if u != v]
    comps, iso = K.components(GV, Gmask)
    nK, mK, tK = len(K.V), len(K.E), K.tau()
    sK = slack(nK, mK, tK)
    tG = K.tau_mask(Gmask)
    sG = slack(nK - 1, mK - 3, tG)
    # (i)
    flat = [u for p in P for u in p]
    if len(set(flat)) != 6: fails.append("i:not distinct")
    for u in flat:
        if K.deg(u, Gmask) != K.deg(u) - 1: fails.append("i:deg")
    for p in P:
        if K.inc[p[0]] & K.inc[p[1]] & Gmask: fails.append("i:pair inside edge of G")
    if tG != tK - 1: fails.append("i:tau drop %d" % (tK - tG))
    if sG != sK + 2: fails.append("i:slack")
    cid = {}
    for k, (Vc, em) in enumerate(comps):
        for u in Vc: cid[u] = k
    for y in iso: cid[y] = 'Y'
    cells = []
    for (Vc, em) in comps:
        n_, m_, t_ = len(Vc), popc(em), K.tau_mask(em)
        cells.append((n_, m_, t_))
        s_ = slack(n_, m_, t_)
        if not (0 <= s_ <= 3): fails.append("ii:comp slack")
        if not any(u in Vc for u in flat): fails.append("ii:no co-vertex")
        if max(K.deg(u, em) for u in Vc) > 3: fails.append("ii:Delta")
        # (iii) free choice
        for x in Vc:
            if K.tau_mask(em & ~K.inc[x]) != t_ - 1: fails.append("iii:free choice"); break
    ssum = sum(slack(*c) for c in cells)
    # (ii)
    if len(iso) > 1: fails.append("ii:|Y|>1")
    if iso:
        if sK != 1 or ssum != 0: fails.append("ii:Y nonempty but not s=1 / tight")
        for y in iso:
            if y not in flat or K.deg(y) != 1: fails.append("ii:Y not co-vertex of degree 1")
    else:
        if ssum != sK + 2: fails.append("ii:slack sum")
    def NC(k, x, y):
        Vc, em = comps[k]
        if K.deg(x, em) > 2 or K.deg(y, em) > 2: return False
        return K.tau_mask(em & ~K.inc[x] & ~K.inc[y]) != K.tau_mask(em) - 2
    def common_edge(k, x, y):
        return bool(K.inc[x] & K.inc[y] & comps[k][1])
    r = len(comps)
    pat, detail = None, None
    if not iso:
        if r == 1:
            pat = 'a'
        elif r == 2:
            ty = [cid[p[0]] if cid[p[0]] == cid[p[1]] else 's' for p in P]
            ins = [t for t in ty if t != 's']
            if not ins:
                pat = 'b'
                for k in (0, 1):
                    xs = [p[0] if cid[p[0]] == k else p[1] for p in P]
                    if not (NC(k, xs[0], xs[1]) and NC(k, xs[0], xs[2]) and NC(k, xs[1], xs[2])):
                        fails.append("b:cond")
            elif len(ins) == 2 and ins[0] != ins[1]:
                pat = 'e'
                js = [j for j in range(3) if ty[j] == 's'][0]
                for k in (0, 1):
                    pin = [P[j] for j in range(3) if ty[j] == k][0]
                    z = P[js][0] if cid[P[js][0]] == k else P[js][1]
                    if not (NC(k, z, pin[0]) and NC(k, z, pin[1]) and not common_edge(k, pin[0], pin[1])):
                        fails.append("e:cond")
            elif len(ins) == 1:
                pat = 'f'
                k1 = ins[0]; k2 = 1 - k1
                P1 = [P[j] for j in range(3) if ty[j] != 's'][0]
                spl = [P[j] for j in range(3) if ty[j] == 's']
                ce = [p[0] if cid[p[0]] == k1 else p[1] for p in spl]
                df = [p[1] if cid[p[0]] == k1 else p[0] for p in spl]
                ok = all(NC(k1, x, y) for x in P1 for y in ce) and NC(k2, df[0], df[1])
                if not ok: fails.append("f:cond")
                Vc, em = comps[k1]
                w = max(K.V) + 1
                EF = [K.E[i] for i in range(len(K.E)) if em >> i & 1] + [tuple(sorted((w,) + tuple(P1))), tuple(sorted((w,) + tuple(ce))) ]
                if in_C(list(Vc) + [w], EF): fails.append("f:F1+w in C")
            else:
                pat = 'c'; fails.append("iv:two pairs in one component with r=2")
        else:
            pat = 'd'; fails.append("iv:r>=3 without Y")
    else:
        y = iso[0]
        j3 = [j for j in range(3) if y in P[j]][0]
        f = [u for u in P[j3] if u != y][0]
        if K.deg(f) not in (2, 3): fails.append("v:deg f")
        P12 = [P[j] for j in range(3) if j != j3]
        ty = [cid[p[0]] if cid[p[0]] == cid[p[1]] else 's' for p in P12]
        cf = cid[f]
        if r == 1:
            pat = 'i1'
            Vc, em = comps[0]
            # no min transversal of F1 meets P1, P2 and contains f  <=>  tau((F1-f)+w(P1,P2)) = tau(F1-f)+1
            w = max(K.V) + 1
            EF = [K.E[i] for i in range(len(K.E)) if (em & ~K.inc[f]) >> i & 1]
            H1 = HG([u for u in Vc if u != f], EF)
            H2 = HG([u for u in Vc if u != f] + [w], EF + [tuple(sorted((w,) + tuple(P12[0]))), tuple(sorted((w,) + tuple(P12[1])))])
            if H2.tau() != H1.tau() + 1: fails.append("i1:cond")
            if H1.tau() != K.tau_mask(em) - 1: fails.append("i1:free choice f")
        elif r == 2:
            if ty[0] != 's' and ty[1] != 's':
                if ty[0] == ty[1]:
                    pat = 'i2-excl'; fails.append("v:two pairs one comp r=2")
                else:
                    pat = 'i2-1'
                    P1 = P12[0] if ty[0] == cf else P12[1]
                    if not (NC(cf, P1[0], f) and NC(cf, P1[1], f)): fails.append("i2-1:cond")
            elif (ty[0] == 's') != (ty[1] == 's'):
                P1 = P12[0] if ty[0] != 's' else P12[1]
                P2 = P12[1] if ty[0] != 's' else P12[0]
                k1 = cid[P1[0]]; k2 = 1 - k1
                c = P2[0] if cid[P2[0]] == k1 else P2[1]
                d = P2[1] if c == P2[0] else P2[0]
                if cf == k1:
                    pat = 'i2-2'
                    if not (NC(k1, P1[0], f) and NC(k1, P1[1], f)): fails.append("i2-2:cond")
                else:
                    pat = 'i2-3'
                    if not (NC(k1, P1[0], c) and NC(k1, P1[1], c) and NC(k2, d, f)): fails.append("i2-3:cond")
            else:
                pat = 'i2-4'
                k1 = cf; k2 = 1 - k1
                a = P12[0][0] if cid[P12[0][0]] == k1 else P12[0][1]
                b = P12[0][1] if a == P12[0][0] else P12[0][0]
                c = P12[1][0] if cid[P12[1][0]] == k1 else P12[1][1]
                d = P12[1][1] if c == P12[1][0] else P12[1][0]
                if not (NC(k1, f, a) and NC(k1, f, c) and NC(k2, b, d)): fails.append("i2-4:cond")
        elif r == 3:
            pat = 'i3'
            ins = [p for p, t in zip(P12, ty) if t != 's']
            if len(ins) != 1 or cid[ins[0][0]] != cf: fails.append("i3:shape")
            else:
                P1 = ins[0]
                if not (NC(cf, P1[0], f) and NC(cf, P1[1], f)): fails.append("i3:cond")
        else:
            pat = 'i>3'; fails.append("v:r>3")
    return dict(pattern=pat, cells=sorted(cells), iso=len(iso), sK=sK, fails=fails)
