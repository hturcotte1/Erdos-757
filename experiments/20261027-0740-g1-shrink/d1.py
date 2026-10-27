"""(D1) trace patterns for the 32 pieces: enumerate, filter by C-membership, kill by L016's I11 on sub-extensions.
usage: python3 d1.py [piece-name-substring]"""
import sys, json, itertools, time
from g1lib import *

def parts_of(P):
    low = [x for x in range(P.n) if P.deg[x] <= 2]
    es = [set(e) for e in P.edges]
    parts = [(x,) for x in low] + [(a, b) for a, b in itertools.combinations(low, 2)
                                  if not any({a, b} <= e for e in es)]
    return parts

def build(P, traces, k):
    """vertex n_F = v; outer vertices after.  returns (nv, edges, vedges=[(trace_tuple, outer_list, edge_tuple)], outer_ids)"""
    v = P.n; nxt = P.n + 1; edges = list(P.edges); ved = []; outer = []
    for q in traces:
        if len(q) == 2: e = (v, q[0], q[1]); o = []
        else: o = [nxt]; outer.append(nxt); e = (v, q[0], nxt); nxt += 1
        edges.append(e); ved.append((q, o, e))
    if k == 2:
        p, qq = nxt, nxt + 1; nxt += 2; outer += [p, qq]
        e = (v, p, qq); edges.append(e); ved.append(((), [p, qq], e))
    return nxt, edges, ved, outer

def analyze(P, minT, traces, k, want_all=False):
    n, edges, ved, outer = build(P, traces, k)
    sF = slack(P.n, P.m, P.tau)
    res = {'traces': [list(q) for q in traces], 'k': k, 'n_full': n, 'outer': len(outer)}
    if not outer:
        res['status'] = 'void_no_outer'; return res
    inC = in_C(n, edges)
    res['inC'] = inC
    oset = outer
    best = None; killed = None; full = None
    for r in range(len(oset) + 1):
        for Qp in itertools.combinations(oset, r):
            Qs = set(Qp)
            inc = [(q, o, e) for (q, o, e) in ved if set(o) <= Qs]
            kU = len(inc)
            if kU == 0:
                t = 0
            else:
                tms = [sum(1 << x for x in q) for (q, o, e) in inc]
                t = 0 if (all(tms) and any(all(T & tm for tm in tms) for T in minT)) else 1
            nB = P.n + 1 + len(Qp); mB = P.m + kU
            s0 = slack(nB, mB, P.tau + t)
            if best is None or s0 < best[0]: best = (s0, Qp, nB, mB, P.tau + t)
            if len(Qp) == len(oset): full = (s0, Qp, nB, mB, P.tau + t)
            if s0 >= 0 or killed: continue
            # extra edges g inside Q' (not two vertices on one v-edge)
            edge_of = {}
            for (q, o, e) in ved:
                for x in o: edge_of[x] = e
            ok_kill = True
            for g in itertools.combinations(Qp, 3):
                if len({edge_of[x] for x in g}) < 3: continue
                if s0 + 2 < 0: continue     # even with tau unchanged the slack stays negative
                Uv = list(range(P.n + 1)) + list(Qp)
                nn, ee = induced(n, edges, Uv)
                gg = tuple(Uv.index(x) for x in g)
                ee2 = ee + [gg]
                if not in_C(nn, ee2): continue      # variant impossible
                tau2 = tau_masks(masks(ee2))
                if slack(nn, len(ee2), tau2) >= 0: ok_kill = False; break
            if ok_kill:
                killed = dict(Q=list(Qp), n=nB, m=mB, tau=P.tau + t, s=s0)
    res['I11_formula_kill'] = killed is not None
    res['full'] = dict(n=full[2], m=full[3], tau=full[4], s=full[0]) if full else None
    res['min_s_k0'] = dict(s=best[0], Q=list(best[1]), n=best[2], m=best[3], tau=best[4])
    if not inC: res['status'] = 'notC'
    elif killed: res['status'] = 'killedI11'; res['kill'] = killed
    else: res['status'] = 'survive'
    return res

def run_piece(P, verbose=True):
    t0 = time.time()
    em = masks(P.edges); minT = min_transversals(em, P.tau)
    parts = parts_of(P); pm = {q: sum(1 << x for x in q) for q in parts}
    # per-part bitset over minT
    pb = {q: sum(1 << i for i, T in enumerate(minT) if T & pm[q]) for q in parts}
    out = []; cnt = dict(total=0, void_no_outer=0, notC=0, killedI11=0, survive=0, I11_formula_kill_all=0)
    for k in (2, 3):
        for comb in itertools.combinations(parts, k):
            used = [x for q in comb for x in q]
            if len(used) != len(set(used)): continue
            acc = pb[comb[0]]
            for q in comb[1:]: acc &= pb[q]
            if acc: continue          # coverable: Claim B fails, pattern cannot occur
            r = analyze(P, minT, comb, k)
            cnt['total'] += 1; cnt[r['status']] += 1
            if r.get('I11_formula_kill'): cnt['I11_formula_kill_all'] += 1
            out.append(r)
    cnt['time_s'] = round(time.time() - t0, 1)
    if verbose: print(P.name, cnt, flush=True)
    return cnt, out

if __name__ == '__main__':
    pat = sys.argv[1] if len(sys.argv) > 1 else ''
    res = {}; allp = {}
    for P in load_pieces():
        if pat not in P.name: continue
        c, o = run_piece(P)
        res[P.name] = c; allp[P.name] = [r for r in o if r['status'] in ('survive',)]
    json.dump(dict(counts=res, survivors=allp), open('d1_results%s.json' % (('_' + pat) if pat else ''), 'w'))
