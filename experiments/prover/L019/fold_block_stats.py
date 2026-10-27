"""C2 (L019): why foldings leave C on the stored lists. For each fold (x of degree 2, u,w non-adjacent in different x-edges):
classify H° as in C, or failing linearity (N), F7-freeness (F), e(S)<=|S|-2 (P); for every fold with n <= 17 also test the
tight-set criterion of Lemma 5.3 (P fails iff H has S with u,w in S, x not in S, |S|>=3, e(S)=|S|-2): mismatches must be 0."""
import sys, itertools, collections
from hg import *
from check_folding import fold

def main(path, K):
    cnt = collections.Counter(); crit_fail = 0; tsz = collections.Counter()
    for (n, m, t, E) in read_cell(path, K):
        d = degrees(n, E)
        inE = set()
        for e in E:
            for a, b in itertools.permutations(e, 2): inE.add((a, b))
        for x in range(n):
            if d[x] != 2: continue
            e1, e2 = [e for e in E if x in e]
            for u in [y for y in e1 if y != x]:
                for w in [y for y in e2 if y != x]:
                    if (u, w) in inE: cnt['adjacent'] += 1; continue
                    n2, E2 = fold(n, E, x, u, w)
                    lin = linear(E2); f7 = has_f7(E2) if lin else None; pp = p3(E2)
                    key = ('N' if not lin else '') + ('F' if f7 else '') + ('P' if not pp else '')
                    cnt[key or 'inC'] += 1
                    ts = tight_set_exists(n, E, x, u, w) if n <= 17 else 'skip'
                    if ts != 'skip':
                        if (not pp) != (ts is not None): crit_fail += 1
                        if not pp: tsz[ts] += 1
    print(path.split('/')[-1], K, dict(cnt), 'criterion mismatches:', crit_fail, 'blocking tight-set sizes:', dict(tsz))

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
