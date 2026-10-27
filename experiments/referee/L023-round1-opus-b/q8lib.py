"""Referee L023 (opus-b): the standard Q8 and a search for all copies of Q8 in a 3-graph (own code)."""
import itertools
a, b = 0, 1; c = [None, 2, 3, 4, 5, 6, 7]
Q8 = [(a, c[1], c[2]), (a, c[3], c[4]), (a, c[5], c[6]), (b, c[2], c[3]), (b, c[4], c[5]), (b, c[6], c[1])]
def q8_copies(E):
    inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(tuple(e))
    out = []
    for A, B in itertools.permutations(sorted(inc), 2):
        for ea in itertools.combinations(inc[A], 3):
            if B in set().union(*map(set, ea)): continue
            la = [tuple(sorted(set(e) - {A})) for e in ea]
            Va = set().union(*map(set, la))
            if len(Va) != 6: continue
            for eb in itertools.combinations(inc[B], 3):
                lb = [tuple(sorted(set(e) - {B})) for e in eb]
                Vb = set().union(*map(set, lb))
                if Vb != Va or A in Vb: continue
                # build the hexagon c1..c6: c1c2 in la, c2c3 in lb, c3c4 in la, c4c5 in lb, c5c6 in la, c6c1 in lb
                sa = [set(p) for p in la]; sb = [set(p) for p in lb]
                for start in la:
                    for orient in (start, start[::-1]):
                        seq = [orient[0], orient[1]]
                        ok = True
                        for step in range(4):
                            pool = sb if step % 2 == 0 else sa
                            nxt = [p for p in pool if seq[-1] in p and (set(p) - {seq[-1]}).isdisjoint(seq)]
                            if len(nxt) != 1: ok = False; break
                            seq.append((nxt[0] - {seq[-1]}).pop())
                        if not ok or len(set(seq)) != 6: continue
                        # map standard Q8 -> X: 0->A, 1->B, c_j -> seq[j-1]
                        phi = {0: A, 1: B}
                        for j in range(6): phi[2 + j] = seq[j]
                        img = set(frozenset(phi[v] for v in e) for e in Q8)
                        Es = set(frozenset(e) for e in E)
                        if img <= Es and len(set(phi.values())) == 8:
                            out.append((A, B, tuple(seq), sorted(tuple(sorted(phi[v] for v in e)) for e in Q8)))
                        break
                    else:
                        continue
                    break
    return out

