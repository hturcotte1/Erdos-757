"""Self-test of ref2.py on known objects and against a second, recursive tau / (P3) implementation."""
import itertools, random
from ref2 import *

F7 = [frozenset(e) for e in [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]]
# AG(2,3): points (a,b) in Z3^2 -> 3a+b; lines {p, p+d, p+2d}
pts = [(a, b) for a in range(3) for b in range(3)]
lines = set()
for p in pts:
    for dvec in [(0, 1), (1, 0), (1, 1), (1, 2)]:
        lines.add(frozenset(3 * ((p[0] + k * dvec[0]) % 3) + (p[1] + k * dvec[1]) % 3 for k in range(3)))
AG = sorted(lines, key=sorted)
FANO = [frozenset(e) for e in [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]]
print('F7: copies', len(f7_copies(F7)), 'tau', all_min_T(range(7), F7)[0],
      'slack', slack(7, 5, all_min_T(range(7), F7)[0]), 'linear', is_linear(F7), 'P3', p3_ok(range(7), F7))
print('AG(2,3): lines', len(AG), 'F7 copies', len(f7_copies(AG)), 'P3', p3_ok(range(9), AG))
print('Fano: F7 copies', len(f7_copies(FANO)))


def tau_rec(E):
    E = [set(e) for e in E]
    best = [len(set().union(*E)) if E else 0]

    def rec(rem, k):
        if k >= best[0]:
            return
        if not rem:
            best[0] = k
            return
        e = rem[0]
        for x in e:
            rec([f for f in rem if x not in f], k + 1)
    rec(E, 0)
    return best[0]


def p3_rec(V, E):
    V = sorted(V)
    for k in range(2, len(V) + 1):
        for S in itertools.combinations(V, k):
            Ss = set(S)
            if sum(1 for e in E if e <= Ss) > k - 2:
                return False
    return True


rng = random.Random(7)
mm_t = mm_p = 0
for _ in range(300):
    n = rng.randint(5, 10)
    E = []
    pairs = set()
    for _ in range(rng.randint(1, 14)):
        e = frozenset(rng.sample(range(n), 3))
        ps = set(itertools.combinations(sorted(e), 2))
        if not ps & pairs:
            E.append(e)
            pairs |= ps
    t, Ts = all_min_T(range(n), E)
    mm_t += (t != tau_rec(E))
    # every returned set is a transversal of size t
    assert all(len(T) == t and all(e & T for e in E) for T in Ts)
    mm_p += (p3_ok(range(n), E) != p3_rec(range(n), E))
print('random 300: tau mismatches', mm_t, 'P3 mismatches', mm_p)
