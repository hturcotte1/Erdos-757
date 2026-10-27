"""Consistency of U1's run records for the five GAP keys: my brute-force decompositions of (n-1, m-3, S') and the input counts
computed from the component list sizes (refereed / twice-computed lists in engine/cells; GAP lists from own/u1_gap) must equal the
INFO line (decompositions, inputs); also bad_tau = 0 and one branch (d = 3, tp = t-1) only."""
import os, re, json, math
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def nclasses(key):
    for d in (os.path.join(R, 'engine', 'cells'), os.path.join(R, 'own', 'u1_gap')):
        p = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key)
        if os.path.exists(p): return sum(1 for l in open(p) if l.startswith('FOUND:'))
    return None
def types_for(nk):
    if nk == 1: return [(1, 0, 0)]
    if nk < 3: return []
    return [(nk, mk, tk) for mk in range(math.ceil((nk - 1) / 2), nk - 1) for tk in range(1, mk + 1)
            if 17 * tk <= 5 * nk + 3 * mk and 3 * nk + 2 * mk - 11 * tk >= 0]
def decomps(N, M, S):
    res = set()
    def rec(nleft, mleft, sleft, minpart, cur):
        if nleft == 0:
            if mleft == 0 and sleft == 0: res.add(tuple(sorted(cur)))
            return
        for nk in range(minpart, nleft + 1):
            for typ in types_for(nk):
                sl = 3 * typ[0] + 2 * typ[1] - 11 * typ[2]
                if typ[1] <= mleft and sl <= sleft: rec(nleft - nk, mleft - typ[1], sleft - sl, nk, cur + [typ])
    rec(N, M, S, 1, []); return sorted(res)
for key in [(17, 15, 7, 3), (20, 16, 8, 3), (21, 19, 9, 3), (23, 17, 9, 3), (24, 20, 10, 3)]:
    n, m, t, D = key
    info = json.loads([l for l in open(os.path.join(R, 'own', 'u1_gap', 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('INFO ')][0][5:])
    dmin = max(1, math.ceil(3 * m / n)); branches = [(d, tp, 3 * (n - 1) + 2 * (m - d) - 11 * tp) for d in range(dmin, D + 1) for tp in (t - 1, t) if 3 * (n - 1) + 2 * (m - d) - 11 * tp >= 0]
    tot_inputs = 0; tot_decs = 0; missing = []
    for d, tp, Sp in branches:
        decs = decomps(n - 1, m - d, Sp); tot_decs += len(decs)
        for dec in decs:
            groups = {}
            for c in dec: groups[c] = groups.get(c, 0) + 1
            size = 1
            for typ, k in groups.items():
                c = 1 if typ == (1, 0, 0) else nclasses((typ[0], typ[1], typ[2], d))
                if c is None: missing.append((typ, d)); c = 0
                size *= math.comb(c + k - 1, k)
            tot_inputs += size
    br = info['branches']
    rec = [(b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], b.get('ext', {}).get('bad_tau')) for b in br]
    print('%s: my branches %s, decompositions %d, inputs %d%s | U1 record (d,tp,Sp,decs,inputs,bad_tau) %s, classes %d, secs %s -> %s' % (
        key, branches, tot_decs, tot_inputs, (' MISSING %s' % missing if missing else ''), rec, nclasses(key), info.get('secs'),
        'CONSISTENT' if (len(rec) == len(branches) and all(r[3] == len(decomps(n - 1, m - r[0], r[2])) for r in rec) and sum(r[4] for r in rec) == tot_inputs and all(r[5] == 0 for r in rec)) else 'MISMATCH'))
