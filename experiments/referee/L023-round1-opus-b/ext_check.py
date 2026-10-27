"""Referee L023 (opus-b): sampled completeness check of a stored cell list, with own code only (hg.py), for the GAP key
cell(20,16,8,3) (route: recursion, single branch d=3, t'=7, S'=6, 21 decompositions of (19,13)).

For each selected input G (disjoint union of class representatives of the child lists, own construction) the program
 (1) checks tau(G) = 7 exactly (own tau);
 (2) lists all 7-covers of G (own enumeration, all minimum covers);
 (3) lists ALL sets of 3 pairwise disjoint vertex pairs {p,q} of G, not inside an edge of G, with deg_G(p), deg_G(q) <= 2, such that every
     7-cover of G misses some pair completely (exactly the extensions X = G + {w,p_i,q_i} with tau(X) >= 8; tau(X) <= tau(G)+1 = 8);
 (4) keeps the X that are F7-free, satisfy (P3) and are connected (linearity and Delta <= 3 hold by construction);
 (5) looks up the own canonical form of every kept X in the own index of the stored list (index_list.py).
A kept X that is not in the index is a COMPLETENESS FAILURE of the stored list (X is a connected member of C with (20,16,8), Delta <= 3).
usage: python3 ext_check.py PLAN.json OUT.jsonl   (PLAN: list of [decomposition, list of input index tuples])"""
import sys, json, pickle, time, itertools, os
from hg import parse, canon, tau, covers_upto, has_F7, p3, connected, linear
HERE = os.path.dirname(os.path.abspath(__file__))
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
REF = os.path.join(HERE, 'ref', 'L014', 'cells')
UNREF = {(13, 11, 5), (16, 12, 6), (19, 13, 7)}   # unrefereed children (identical in U1 and the prover's repro3)
_cache = {}
def child(typ):
    if typ == (1, 0, 0): return [[]]
    if typ in _cache: return _cache[typ]
    fn = os.path.join(U1 if typ in UNREF else REF, 'cell_%d_%d_%d_D3.txt' % typ)
    L = [parse(l) for l in open(fn) if l.startswith('FOUND:')]
    _cache[typ] = L
    return L

def extensions(nG, E, t, d):
    """all sets of d pairwise disjoint admissible pairs killing every t-cover of G (tau(G) = t)."""
    deg = [0] * nG
    for e in E:
        for v in e: deg[v] += 1
    inside = set()
    for (a, b, c) in E:
        inside |= {(min(a, b), max(a, b)), (min(a, c), max(a, c)), (min(b, c), max(b, c))}
    covs = covers_upto(nG, E, t)
    pairs = [(p, q) for p in range(nG) for q in range(p + 1, nG) if deg[p] <= d - 1 and deg[q] <= d - 1 and (p, q) not in inside]
    pm = [(1 << p) | (1 << q) for (p, q) in pairs]
    kills = []
    for b in pm:
        k = 0
        for i, T in enumerate(covs):
            if not (T & b): k |= 1 << i
        kills.append(k)
    ALL = (1 << len(covs)) - 1
    by_cover = [[j for j in range(len(pairs)) if (kills[j] >> i) & 1] for i in range(len(covs))]
    sols = set()
    def complete(chosen, used, k, start):
        if k == 0: sols.add(tuple(sorted(chosen))); return
        for j in range(start, len(pairs)):
            if not (pm[j] & used) and j not in chosen:
                complete(chosen + [j], used | pm[j], k - 1, j + 1)
    def rec(chosen, used, killed, k):
        surv = ALL & ~killed
        if surv == 0:
            complete(chosen, used, k, 0); return
        if k == 0: return
        i = (surv & -surv).bit_length() - 1
        for j in by_cover[i]:
            if not (pm[j] & used):
                rec(chosen + [j], used | pm[j], killed | kills[j], k - 1)
    rec([], 0, 0, d)
    return [[pairs[j] for j in s] for s in sols], len(covs), len(pairs)

def main():
    plan = json.load(open(sys.argv[1])); out = open(sys.argv[2], 'a')
    idx = pickle.load(open(os.path.join(HERE, 'idx_20_16_8_D3.pkl'), 'rb'))
    n, t, d = 20, 8, 3
    tot = dict(inputs=0, ext=0, kept=0, missing=0, notF7free=0, notP3=0, disconnected=0)
    t0 = time.time()
    for dec, combos in plan:
        dec = [tuple(x) for x in dec]
        for combo in combos:
            E = []; off = 0
            for typ, ci in zip(dec, combo):
                rep = child(typ)[ci]
                E += [tuple(v + off for v in e) for e in rep]; off += typ[0]
            assert off == n - 1 and len(E) == 13 and linear(E)
            tG = tau(n - 1, E); assert tG == t - 1, ('bad tau', dec, combo, tG)
            sols, ncov, npairs = extensions(n - 1, E, t - 1, d)
            kept = 0; miss = []
            for s in sols:
                X = E + [(min(p, q, 19), sorted((p, q, 19))[1], max(p, q, 19)) for (p, q) in s]
                X = [tuple(sorted(e)) for e in X]
                if has_F7(n, X): tot['notF7free'] += 1; continue
                if not p3(n, X): tot['notP3'] += 1; continue
                if not connected(n, X): tot['disconnected'] += 1; continue
                kept += 1
                c, _ = canon(n, X)
                if c not in idx: miss.append(X)
            tot['inputs'] += 1; tot['ext'] += len(sols); tot['kept'] += kept; tot['missing'] += len(miss)
            out.write(json.dumps(dict(dec=dec, combo=list(combo), covers=ncov, pairs=npairs, ext=len(sols), kept=kept, missing=miss)) + '\n'); out.flush()
            if tot['inputs'] % 200 == 0: print('progress', json.dumps(tot), round(time.time() - t0), flush=True)
    print('SUMMARY', json.dumps(tot), 'secs', round(time.time() - t0), flush=True)

if __name__ == '__main__':
    main()
