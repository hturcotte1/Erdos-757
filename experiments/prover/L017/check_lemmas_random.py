"""L017, computation C6: illustrative random test of Theorem 2 (R), (R+) and (U) on random linear 3-graphs (these lemmas hold for every
3-graph; (U) needs only s(F - X) >= 0).  tau of every vertex subset by the exact DP of minimal_violators.HG.
Usage: python3 check_lemmas_random.py NGRAPHS SEED"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from minimal_violators import HG, bit

def random_linear(rng, n, tries):
    edges = []; used = set()
    for _ in range(tries):
        e = tuple(sorted(rng.sample(range(n), 3)))
        ps = [(e[0], e[1]), (e[0], e[2]), (e[1], e[2])]
        if any(p in used for p in ps): continue
        edges.append(e); used.update(ps)
    return edges

def main(NG, seed):
    rng = random.Random(seed); cnt = dict(R=0, Rp=0, U=0, Upred=0); bad = 0
    for it in range(NG):
        n = rng.randint(4, 11); H = HG(n, random_linear(rng, n, rng.randint(1, 3 * n)))
        V = H.full; tau = H.T[V]; s = H.slack(V)
        # (R): random Z, T = a random cover of the edges meeting Z
        for _ in range(5):
            Z = sum(bit(x) for x in range(n) if rng.random() < 0.3) or bit(rng.randrange(n))
            dZ = [e for e in H.em if e & Z]; T = 0
            for e in dZ:
                if not e & T:
                    xs = [x for x in range(n) if e >> x & 1]; T |= bit(rng.choice(xs))
            k = bin(T).count('1'); nz = bin(Z).count('1')
            ok = tau <= H.T[V & ~Z] + k and s >= H.slack(V & ~Z) + 3 * nz + 2 * len(dZ) - 11 * k
            cnt['R'] += 1; bad += (not ok)
        # (R+): random disjoint blocks W_i, random minimum transversals T_i (exact: any minimum transversal of F_i is fine;
        # we take the lexicographically first found by brute force), T_0 = greedy cover of the uncovered edges of E*
        verts = list(range(n)); rng.shuffle(verts); r = rng.randint(1, 3); blocks = []
        for i in range(r):
            sz = rng.randint(1, max(1, n // (r + 1)))
            blk = verts[:sz]; verts = verts[sz:]
            if blk: blocks.append(sum(bit(x) for x in blk))
        if blocks:
            W = 0
            for b in blocks: W |= b
            Tall = 0
            for b in blocks:
                t_b = H.T[b]
                # find a minimum transversal of H[b] by subset search on b (small)
                bs = [x for x in range(n) if b >> x & 1]
                for X in itertools.combinations(bs, t_b):
                    Xm = sum(bit(x) for x in X)
                    if all(e & Xm for e in H.em if e & b == e): Tall |= Xm; break
            Estar = [e for e in H.em if e & W and not any(e & b == e for b in blocks)]
            T0 = 0
            for e in Estar:
                if not e & (Tall | T0):
                    xs = [x for x in range(n) if e >> x & 1]; T0 |= bit(xs[0])
            R = V & ~W
            ok = s >= H.slack(R) + sum(H.slack(b) for b in blocks) + 2 * len(Estar) - 11 * bin(T0).count('1')
            cnt['Rp'] += 1; bad += (not ok)
        # (U): all X with |X| <= 3
        for k in (1, 2, 3):
            for X in itertools.combinations(range(n), k):
                Xm = sum(bit(x) for x in X)
                if H.slack(V & ~Xm) < 0: continue
                dX = sum(1 for e in H.em if e & Xm)
                cnt['U'] += 1
                if s < 2 * dX + 11 - 8 * k:
                    cnt['Upred'] += 1
                    if not H.in_min_T(Xm, V): bad += 1
    print('random linear 3-graphs: %d; (R) instances %d, (R+) instances %d, (U) instances %d of which %d with the hypothesis; failures: %d'
          % (NG, cnt['R'], cnt['Rp'], cnt['U'], cnt['Upred'], bad))

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
