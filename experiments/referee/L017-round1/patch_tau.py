src = open('test_iv.py').read()
old = '''def tau(V, E):
    V = sorted(V)
    if not E: return 0
    for k in range(1, len(V) + 1):
        for T in itertools.combinations(V, k):
            S = set(T)
            if all(S & e for e in E): return k'''
new = '''def tau(V, E):
    """exact transversal number by branching on an uncovered edge (with a packing lower bound)"""
    E = [frozenset(e) for e in E]
    best = [len(E)]
    def lb(rem):
        used = set(); c = 0
        for e in rem:
            if not (e & used): used |= e; c += 1
        return c
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + lb(rem) >= best[0]: return
        e = rem[0]
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]'''
assert old in src
open('test_iv.py', 'w').write(src.replace(old, new))
print('patched')
