"""Referee round 3, L006 -- Route X (own design, no repo imports): FULL-CENSUS check, Sidon definition only, organised by the point
in P_x instead of by AP hypergraphs.  For A with h(A)=7 and the list Ts of all Sidon 7-subsets:
  (x,y) deficient (h(A u{x,y}) <= 8)  <=>  for all T in Ts: T u {x,y} not Sidon.
(i)  x in P_x (3-AP third points of A; by symmetry this covers every pair with a point in P_x):  G_x = {T : T u {x} Sidon}.
     If G_x is empty, A u {x} has h = 7 (flag if A u {x} is (4,5)).  Otherwise (x,y) is deficient iff y lies in
     Y_x = cap_{T in G_x} K(T u {x}),  K(S) = {y notin S : S u {y} not Sidon} = {s2+s3-s1 : s1 notin {s2,s3}} u {(s1+s2)/2 : s1 != s2},
     a finite set: so ALL real y are covered.  Every y in Y_x is tested for (4,5) of B (flag if (4,5)).
(ii) x,y notin P_x and B (4,5): B is weak Sidon (K3), so the only sum coincidences in T u {x,y} are 3-APs {x,y,t}; a deficient point
     on exactly one such line {a,x,y} needs a in every T (checked: the intersection of all Ts is empty); on two lines it violates
     linearity (K6) -- the same argument as the claim, re-checked here only through 'core empty'.
Scaled by 4 so that every element of every K(T u {x}) is an integer.
Usage: python3 route_X.py START STOP OUT.jsonl  (census index range)"""
import gzip, json, itertools, sys, time
def is_sidon(S):
    seen = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True
def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})
def K_of(S):
    out = set(); Sl = list(S)
    for i, s2 in enumerate(Sl):
        for s3 in Sl[i:]:
            for s1 in Sl:
                if s1 != s2 and s1 != s3: out.add(s2 + s3 - s1)
    for s1, s2 in itertools.combinations(Sl, 2):
        assert (s1 + s2) % 2 == 0
        out.add((s1 + s2) // 2)
    return out - set(Sl)
def run_class(c, setv):
    A = sorted(4 * a for a in setv); As = set(A)
    tri = list(itertools.combinations(A, 3)); prs = list(itertools.combinations(A, 2))
    assert all(nd(q) >= 5 for q in itertools.combinations(A, 4))
    Ts = [T for T in itertools.combinations(A, 7) if is_sidon(T)]
    assert Ts and not any(is_sidon(T + (a,)) for T in Ts for a in A if a not in T)        # h(A) = 7 exactly
    core = set(A)
    for T in Ts: core &= set(T)
    KT = [K_of(T) for T in Ts]
    DF = [{t - u for t in T for u in T if t != u} for T in Ts]
    SL = [{T[i] + T[j] for i in range(7) for j in range(i, 7)} for T in Ts]
    TS = [set(T) for T in Ts]
    SPOT = (c % 25 == 0)
    Px = set()
    for a, b in prs:
        Px.add((a + b) // 2); Px.add(2 * a - b); Px.add(2 * b - a)
    Px -= As
    SA = {a + b for a, b in prs}          # pair sums of A (all distinct: A is (4,5), hence weak Sidon)
    s_ok = {}
    def single(v):
        # exact pre-filter: x + a = b + c (a parallelogram) means A u {v} is not weak Sidon, hence not (4,5) (K3: (4,5) => weak Sidon)
        if v not in s_ok: s_ok[v] = (not any(v + a in SA for a in A)) and all(nd((v,) + t) >= 5 for t in tri)
        return s_ok[v]
    def pair_ws(x, y):
        new = [x + a for a in A] + [y + a for a in A] + [x + y]
        return not any(v in SA for v in new) and len(set(new)) == len(new)
    n_def_pairs = 0; flags = []; n_empty_G = 0; n_x_with_Y = 0
    for x in sorted(Px):
        if any(x + a in SA for a in A): continue    # x + a = b + c: parallelogram, no (4,5) set contains A u {x}: no pair to test
        G = [i for i in range(len(Ts)) if x not in KT[i]]
        if not G:
            n_empty_G += 1
            if single(x): flags.append(('h(Aux)=7 and (4,5)', x))
            continue
        # Y_x = cap_{T in G} K(T u {x});  K(T u {x}) = (K(T) u {x+t-t' (t!=t'), 2x-t, t+t'-x (t<=t'), (x+t)/2}) minus T u {x}
        i0 = G[0]; T0 = Ts[i0]
        Y = set(KT[i0]) | {x + d for d in DF[i0]} | {2 * x - t for t in T0} | {s - x for s in SL[i0]} | {(x + t) // 2 for t in T0 if (x + t) % 2 == 0}
        Y -= As; Y.discard(x)
        for i in G[1:]:
            if not Y: break
            Ki, Di, Si, Ti = KT[i], DF[i], SL[i], TS[i]
            Y = {y for y in Y if y in Ki or (y - x) in Di or (2 * x - y) in Ti or (x + y) in Si or (2 * y - x) in Ti}
        if SPOT:   # spot classes: recompute Y_x the slow way, straight from K_of
            Yslow = None
            for i in G:
                Kx = K_of(Ts[i] + (x,)); Yslow = Kx if Yslow is None else (Yslow & Kx)
            assert Y == (Yslow - As - {x}), ('Y mismatch', c, x)
        if not Y: continue
        n_x_with_Y += 1
        for y in Y:
            n_def_pairs += 1
            # re-verify deficiency by the definition, then (4,5)
            if SPOT: assert all(not is_sidon(list(T) + [x, y]) for T in Ts)   # re-verify deficiency by the definition (spot classes)
            if single(x) and pair_ws(x, y) and single(y) and all(nd((x, y) + q) >= 5 for q in prs):
                flags.append(('deficient (4,5) pair', x, y))
    return {'class': c, 'n_maxT': len(Ts), 'core': sorted(core), 'Px': len(Px), 'x_empty_G': n_empty_G, 'x_with_deficient_y': n_x_with_Y,
            'deficient_ordered_pairs_x_in_Px': n_def_pairs, 'flags': [list(map(str, f)) for f in flags]}
if __name__ == '__main__':
    cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    if sys.argv[1] == 'perm':           # perm PART NPARTS OUT: seeded random order of all classes, part PART of NPARTS
        import random
        order = list(range(len(cen))); random.Random(16102026).shuffle(order)
        part, nparts, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        todo = order[part::nparts]
    else:
        lo, hi, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        todo = range(lo, min(hi, len(cen)))
    t0 = time.time()
    with open(out, 'w') as fo:
        for c in todo:
            fo.write(json.dumps(run_class(c, cen[c]['set'])) + '\n'); fo.flush()
    print('done', len(todo), round(time.time() - t0, 1), flush=True)
