# Referee round 2: brute force of slack decompositions (connected types of C with n<=N: m<=n-2, n<=2m+1, 1<=tau<=m, I11 slack>=0;
# plus the isolated vertex (1,0,0) of slack 3).  No HY.  Partition-first enumeration.
def conn_types(N, S):
    out = []
    for nk in range(3, N + 1):
        for mk in range(1, nk - 1):
            if nk > 2 * mk + 1: continue
            for tk in range(1, mk + 1):
                s = 3 * nk + 2 * mk - 11 * tk
                if 0 <= s <= S: out.append((nk, mk, tk, s))
    return out
def partitions(N, maxp):
    if N == 0: yield (); return
    for p in range(min(N, maxp), 0, -1):
        if p == 2: continue
        for r in partitions(N - p, p): yield (p,) + r
def decomps(N, M, S):
    types = conn_types(N, S); byn = {}
    for ty in types: byn.setdefault(ty[0], []).append(ty)
    byn[1] = [(1, 0, 0, 3)]
    res = set()
    for part in partitions(N, N):
        if any(p not in byn for p in part): continue
        def rec(i, m, s, chosen):
            if i == len(part):
                if m == M and s == S: res.add(tuple(sorted(c[:3] for c in chosen)))
                return
            for ty in byn[part[i]]:
                if i > 0 and part[i] == part[i - 1] and ty < chosen[-1]: continue
                if m + ty[1] > M or s + ty[3] > S: continue
                rec(i + 1, m + ty[1], s + ty[3], chosen + [ty])
        rec(0, 0, 0, [])
    return sorted(res)
