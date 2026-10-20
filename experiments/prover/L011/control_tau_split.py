"""(L011) For a control file (HIT lines): compute tau exactly (pure Python, brute force over vertex subsets in increasing size) and,
for the extensions with tau = TG+1, report how many lie in C (linear, F7-free by Lemma F, (P3)) and how many are connected.
Usage: control_tau_split.py FILE NV TG"""
import re, sys, itertools
f, NV, TG = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def tau(es):
    for k in range(0, NV + 1):
        for S in itertools.combinations(range(NV), k):
            s = set(S)
            if all(s & set(e) for e in es): return k
def in_C(es):
    E = [frozenset(e) for e in es]
    if any(len(a & b) >= 2 for a, b in itertools.combinations(E, 2)): return False
    for F in itertools.combinations(E, 5):
        U = frozenset().union(*F)
        if len(U) == 7 and sorted(sum(v in e for e in F) for v in U) == [2, 2, 2, 2, 2, 2, 3]: return False
    for r in range(1, len(E) + 1):
        for F in itertools.combinations(E, r):
            if len(frozenset().union(*F)) < r + 2: return False
    return True
def connected(es):
    adj = {v: set() for v in range(NV)}
    for e in es:
        for a in e: adj[a].update(e)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x] - seen: seen.add(y); st.append(y)
    return len(seen) == NV
n = high = highC = highCconn = 0
for l in open(f):
    if not l.startswith('HIT:'): continue
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
    n += 1
    if tau(es) == TG + 1:
        high += 1
        if in_C(es): highC += 1; highCconn += connected(es)
print(f, 'extensions', n, '| with tau = %d:' % (TG + 1), high, '| of these in C:', highC, '| in C and connected:', highCconn)
