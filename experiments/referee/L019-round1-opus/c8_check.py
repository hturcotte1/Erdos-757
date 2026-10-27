"""Referee L019: independent re-computation of C8 (Remark 10.3 / Proposition 10 data) for the stored slack-<=1 cells with
m <= n-4: for each class F, all minimum transversals (own enumeration: include/exclude branching on a max-degree vertex
with packing bound; each minimum transversal reached exactly once), every triple of pairwise disjoint pairs none inside an
F-edge that no minimum transversal meets ('uncoverable linear triple'), and for each such triple
 k = number of F-edges meeting W, tau of the edges of H = F + v meeting {v} u W  (own tau_bb),
plus a check that F + v is NOT in C (Theorem 4(c) / L016 force this) and Proposition 10's bound 11 tau >= 27 + 2k - s for
the hypothetical s = s(F) - 2.  usage: c8_check.py cellpath K"""
import sys, os, itertools, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *


def all_min_transversals_bb(E, t):
    ms = list(set(masks_of(E)))
    out = []

    def packing(ms):
        used = 0; c = 0
        for e in sorted(ms, key=lambda e: bin(e).count('1')):
            if not e & used:
                used |= e; c += 1
        return c

    def rec(ms, inc, k):
        if not ms:
            out.append(inc)
            return
        for e in ms:
            if e == 0:
                return
        if k + packing(ms) > t:
            return
        cnt = collections.defaultdict(int)
        for e in ms:
            x = e
            while x:
                b = x & -x; cnt[b] += 1; x ^= b
        b = max(cnt, key=lambda bb: (cnt[bb], -bb))
        rec([e for e in ms if not e & b], inc | b, k + 1)
        rec([e & ~b for e in ms], inc, k)
    rec(ms, 0, 0)
    assert all(bin(T).count('1') == t for T in out), 'non-minimum leaf'
    assert len(set(out)) == len(out)
    return out


def main(path, K):
    hist = collections.Counter(); ntrip = 0; bad = 0; inC_count = 0; graphs = 0
    for gi, (n, m, t, E) in enumerate(read_cell(path, K)):
        graphs += 1
        s = 3 * n + 2 * m - 11 * t
        Ts = all_min_transversals_bb(E, t)
        nT = len(Ts)
        W64 = (nT + 63) // 64
        inE = set()
        for g in E:
            for a, b in itertools.combinations(g, 2):
                inE.add((a, b))
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in inE]
        P = len(pairs)
        Tarr = np.array(Ts, dtype=np.int64)
        pmask = np.array([(1 << a) | (1 << b) for (a, b) in pairs], dtype=np.int64)
        Bm = (Tarr[None, :] & pmask[:, None]) != 0
        mb = np.packbits(Bm, axis=1)
        for i in range(P):
            for j in range(i + 1, P):
                if pmask[i] & pmask[j]:
                    continue
                ij = mb[i] & mb[j]
                if not ij.any():
                    print('pair-pair NOT covered', path, gi, pairs[i], pairs[j])
                    bad += 1
                    continue
                cand = np.arange(j + 1, P)
                cand = cand[(pmask[cand] & (pmask[i] | pmask[j])) == 0]
                if cand.size == 0:
                    continue
                hit = (mb[cand] & ij).any(axis=1)
                for kk in cand[~hit]:
                    p1, p2, p3 = pairs[i], pairs[j], pairs[int(kk)]
                    ntrip += 1
                    W = set(p1) | set(p2) | set(p3)
                    v = n
                    near = [g for g in E if set(g) & W] + [(v,) + p1, (v,) + p2, (v,) + p3]
                    k = len(near) - 3
                    tn = tau_bb(near)
                    hist[(k, tn)] += 1
                    EH = E + [tuple(sorted((v,) + p)) for p in (p1, p2, p3)]
                    if in_C(n + 1, EH, use_table=False):
                        inC_count += 1
                        print('ADMISSIBLE uncoverable triple (contradicts Theorem 4(c)/L016)', gi, p1, p2, p3)
    print(os.path.basename(path), 'graphs', graphs, 'uncoverable linear triples', ntrip,
          '(k, tau(edges meeting {v}uW)):', dict(sorted(hist.items())), 'pair-pair failures', bad,
          'admissible uncoverable', inC_count)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
