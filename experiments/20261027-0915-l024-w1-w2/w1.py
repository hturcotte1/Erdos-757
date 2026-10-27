"""W1: G2-iii empty-boundary assemblies.  k non-rich pieces F_1..F_k (disjoint), k+1 further edges ("star edges") with all
vertices in the pieces, each meeting >= 2 pieces, linear, Delta <= 3, Claim B (no choice of minimum transversals of the
pieces has a union meeting all k+1 edges).  Complete level search (WLOG labelling, see README).
Usage: python3 w1.py <k> <part> <nparts> [nmin]   (types are split round-robin)"""
import sys, itertools, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from hyp24 import *
from w1types import types

def popc(x): return bin(x).count('1')
def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b

class Setup:
    def __init__(self, Ps, need2=True):
        self.Ps = Ps; self.k = k = len(Ps)
        self.offs = []; o = 0
        for P in Ps: self.offs.append(o); o += P['n']
        self.N = N = o
        self.E0 = []
        self.piece_of = {}
        for i, (P, o) in enumerate(zip(Ps, self.offs)):
            self.E0 += [tuple(x + o for x in e) for e in P['edges']]
            for x in range(P['n']): self.piece_of[x + o] = i
        self.d0 = degrees(N, self.E0)
        self.MT = [[T << o for T in P['mts']] for P, o in zip(Ps, self.offs)]
        # hitbits[i][x] (global x): bitset over transversals of piece i containing x
        self.hitbits = []
        for i, P in enumerate(Ps):
            hb = {}
            for x in range(P['n']):
                gx = x + self.offs[i]; b = 0
                for t, T in enumerate(self.MT[i]):
                    if T >> gx & 1: b |= 1 << t
                hb[gx] = b
            self.hitbits.append(hb)
        self.full_t = [(1 << len(self.MT[i])) - 1 for i in range(k)]
        covered = set()
        for e in self.E0:
            for a, b in itertools.combinations(e, 2): covered.add((a, b))
        usable = [x for x in range(N) if self.d0[x] <= 2]
        cands = []
        for a, b, c in itertools.combinations(usable, 3):
            if (a, b) in covered or (a, c) in covered or (b, c) in covered: continue
            if need2 and len({self.piece_of[a], self.piece_of[b], self.piece_of[c]}) < 2: continue
            cands.append((a, b, c))
        self.cands = cands
        self.nc = len(cands)
        self.cmask = [(1 << a) | (1 << b) | (1 << c) for a, b, c in cands]
        self.cap = [3 - d for d in self.d0]
        self.cw = [0] * N   # cand_with[x]
        for idx, (a, b, c) in enumerate(cands):
            for x in (a, b, c): self.cw[x] |= 1 << idx
        self.incompat = []
        for idx, (a, b, c) in enumerate(cands):
            self.incompat.append((self.cw[a] & self.cw[b]) | (self.cw[a] & self.cw[c]) | (self.cw[b] & self.cw[c]))
        # per candidate, per piece: hit bitset
        self.chit = []
        for idx, e in enumerate(cands):
            row = [0] * k
            for x in e: row[self.piece_of[x]] |= self.hitbits[self.piece_of[x]][x]
            self.chit.append(row)
        self.all_c = (1 << self.nc) - 1

    def classes(self, cl):
        """for each piece: dict pattern -> bitset of transversals having exactly that pattern (cl = list of candidate idx)."""
        res = []
        for i in range(self.k):
            cur = {self.full_t[i]: 0}
            for j, ci in enumerate(cl):
                h = self.chit[ci][i]
                nxt = {}
                for B, pat in cur.items():
                    a = B & h
                    if a: nxt[a] = pat | (1 << j)
                    r = B & ~h
                    if r: nxt[r] = pat
                cur = nxt
            d = {}
            for B, pat in cur.items(): d.setdefault(pat, []).append(B)
            res.append(d)
        return res

    def witness_U(self, cl):
        """a union of minimum transversals (one per piece) meeting all clauses in cl, or None."""
        full = (1 << len(cl)) - 1
        cls = self.classes(cl)
        dp = {0: 0}
        for i in range(self.k):
            nd = {}
            for a, Ua in dp.items():
                for pat, Bs in cls[i].items():
                    key = a | pat
                    if key not in nd:
                        B = Bs[0]; t = (B & -B).bit_length() - 1
                        nd[key] = Ua | self.MT[i][t]
            dp = nd
        return dp.get(full)

    def union_all_U(self, cl):
        """union of all transversals that occur in SOME combination covering all clauses; (False, 0) if none."""
        full = (1 << len(cl)) - 1
        cls = self.classes(cl)
        k = self.k
        sets = [set(cls[i].keys()) for i in range(k)]
        # prefix/suffix OR sets
        pre = [{0}]
        for i in range(k):
            pre.append({a | p for a in pre[-1] for p in sets[i]})
        if full not in pre[k]: return False, 0
        suf = [None] * (k + 1); suf[k] = {0}
        for i in range(k - 1, -1, -1):
            suf[i] = {a | p for a in suf[i + 1] for p in sets[i]}
        U = 0
        for i in range(k):
            others = {a | b for a in pre[i] for b in suf[i + 1]}
            for pat, Bs in cls[i].items():
                if any(pat | w == full for w in others):
                    for B in Bs:
                        for gx, hb in self.hitbits[i].items():
                            if B & hb: U |= 1 << gx
        return True, U

    def claimB_brute(self, cl):
        full = (1 << len(cl)) - 1
        cls = self.classes(cl)
        pats = [list(c.keys()) for c in cls]
        for combo in itertools.product(*pats):
            o = 0
            for p in combo: o |= p
            if o == full: return False
        return True

    def tau_plus_one_witness(self, cl):
        """True iff some combination of min transversals covers all but at most one clause (then tau <= sum tau + 1)."""
        K = len(cl); cls = self.classes(cl)
        pats = [list(c.keys()) for c in cls]
        full = (1 << K) - 1
        for combo in itertools.product(*pats):
            o = 0
            for p in combo: o |= p
            for j in range(K):
                if o | (1 << j) == full: return True
        return False

def search(S, stats, c1range=None):
    K = S.k + 1
    sols = set()
    full_bits = S.all_c
    def avoid_bits(U):
        r = 0
        for x in bits(U): r |= S.cw[x]
        return r
    Nmask_all = (1 << S.N) - 1
    def rec(chosen, allowed_base, used_cnt, lowmask):
        L = len(chosen)
        stats['nodes'] += 1
        if L == K:
            sols.add(frozenset(chosen)); return
        if L == K - 1:
            ok, U = S.union_all_U(chosen)
            allowed = allowed_base
            if ok:
                allowed &= ~avoid_bits(U)
        else:
            U = S.witness_U(chosen)
            allowed = allowed_base
            if U is not None:
                allowed &= ~avoid_bits(U)
        while allowed:
            b = allowed & -allowed
            allowed ^= b
            ci = b.bit_length() - 1
            # add edge ci
            e = S.cands[ci]
            nb = allowed_base & ~S.incompat[ci] & ~b
            newc = []
            for x in e:
                used_cnt[x] += 1
                if used_cnt[x] >= S.cap[x]: nb &= ~S.cw[x]
            chosen.append(ci)
            rec(chosen, nb, used_cnt, lowmask)
            chosen.pop()
            for x in e: used_cnt[x] -= 1
    # e1 = minimum-index edge of the solution
    for c1 in (range(S.nc) if c1range is None else c1range):
        e = S.cands[c1]
        used = [0] * S.N
        nb = S.all_c & ~((1 << (c1 + 1)) - 1) & ~S.incompat[c1]
        for x in e:
            used[x] += 1
            if used[x] >= S.cap[x]: nb &= ~S.cw[x]
        rec([c1], nb, used, 0)
    return sols

def connected(S, edges):
    par = list(range(S.N))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in S.E0 + edges:
        for y in e[1:]: par[f(y)] = f(e[0])
    return len({f(x) for x in range(S.N)}) == 1

def claimE(S, edges):
    k = S.k
    for r in range(1, k + 1):
        for Y in itertools.combinations(range(k), r):
            vm = 0
            for i in Y:
                vm |= ((1 << S.Ps[i]['n']) - 1) << S.offs[i]
            if sum(1 for e in edges if any(vm >> x & 1 for x in e)) < r + 1: return False
    return True

def process(S, sols, pieces, stats, out):
    import hyp24
    for sol in sorted(sols, key=lambda s: sorted(s)):
        cl = sorted(sol)
        assert S.claimB_brute(cl)
        stats['claimB'] += 1
        edges = [tuple(sorted(S.cands[c])) for c in cl]
        conn = connected(S, edges); cE = claimE(S, edges)
        if conn: stats['connected'] += 1
        if cE: stats['claimE'] += 1
        E = S.E0 + edges
        n = S.N
        if not in_C3(n, E): continue
        stats['inC3'] += 1
        if cE: stats['inC3_claimE'] += 1
        sumtau = sum(P['tau'] for P in S.Ps)
        if S.tau_plus_one_witness(cl): t = sumtau + 1
        else: t = hyp24.tau(n, E)
        stats['tau_eq_sum_plus1' if t == sumtau + 1 else 'tau_other'] += 1
        A = CN * n + CM * len(E) - CT * t
        rec = dict(types=[P['name'] for P in S.Ps], edges=E, star=edges, claimE=cE, connected=conn, tau=t, A=A)
        if A >= 0:
            stats['A_nonneg'] += 1
        else:
            stats['A_neg'] += 1
            D, fam, ncop = def_certificate(n, E, pieces, -A)
            if fam: assert family_def(n, E, [(Sm, w) for (Sm, w, nm) in fam]) == D
            rec.update(DEF=D, P=A + D, family=[(nm, [x for x in range(n) if Sm >> x & 1]) for (Sm, w, nm) in fam])
            if A + D < 0:
                stats['Pneg'] += 1
                if cE: stats['Pneg_claimE'] += 1
                print('NEGATIVE P', rec, flush=True)
            else:
                stats['A_neg_Pnonneg'] += 1
        out.append(rec)

if __name__ == '__main__':
    k = int(sys.argv[1]); part = int(sys.argv[2]); nparts = int(sys.argv[3])
    nmin = int(sys.argv[4]) if len(sys.argv) > 4 else 25
    t0 = time.time()
    pieces = load_pieces(); byname = {P['name']: P for P in pieces}
    T = types(k, pieces, nmin)
    mine = [t for i, t in enumerate(T) if i % nparts == part]
    tot = {}
    allout = []
    per_type = []
    keys = ['nodes', 'claimB', 'connected', 'claimE', 'inC3', 'inC3_claimE', 'tau_eq_sum_plus1', 'tau_other', 'A_nonneg', 'A_neg',
            'A_neg_Pnonneg', 'Pneg', 'Pneg_claimE']
    print(f'k={k} part {part}/{nparts} types {len(mine)} of {len(T)} nmin {nmin}', flush=True)
    for ti, names in enumerate(mine):
        ts = time.time()
        Ps = [byname[nm] for nm in names]
        S = Setup(Ps)
        stats = {kk: 0 for kk in keys}
        sols = search(S, stats)
        out = []
        process(S, sols, pieces, stats, out)
        per_type.append(dict(types=names, ncands=S.nc, stats=stats, sec=round(time.time() - ts, 1)))
        for kk in keys: tot[kk] = tot.get(kk, 0) + stats[kk]
        allout += out
        print(ti, names, 'N', S.N, 'cands', S.nc, stats, f'{time.time()-ts:.0f}s total {time.time()-t0:.0f}s', flush=True)
        json.dump(dict(k=k, part=part, nparts=nparts, nmin=nmin, done_types=ti + 1, of=len(mine), totals=tot, per_type=per_type, configs=allout),
                  open(f'/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2/w1_k{k}_p{part}of{nparts}_n{nmin}.json', 'w'))
    print('TOTAL', tot, f'{time.time()-t0:.0f}s', flush=True)
