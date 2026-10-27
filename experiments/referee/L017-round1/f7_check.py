# Referee L017 round 1: F7-containment and (P3) of the vertex-critical violators found (own backtracking).
import re, itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def contains_F7(n, E):
    Es = set(frozenset(e) for e in E)
    def rec(i, mp, used):
        if i == 7:
            return all(frozenset(mp[x] for x in f) in Es for f in F7)
        for v in range(n):
            if v in used: continue
            mp[i] = v
            ok = True
            for f in F7:
                if max(f) == i and frozenset(mp[x] for x in f) not in Es: ok = False; break
            if ok and rec(i + 1, mp, used | {v}): return True
            del mp[i]
        return False
    return rec(0, {}, frozenset())
def p3_violations(n, E):
    worst = None
    for k in range(2, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S); e = sum(1 for x in E if set(x) <= s)
            if e > k - 2: return (k, e)
    return None
for fn in ('vcrit_le11.txt', 'vcrit_12_13_D3.txt'):
    for line in open(os.path.join(HERE, fn)):
        if not line.startswith('VIOL crit=1'): continue
        n = int(re.search(r' n=(\d+)', line).group(1)); m = int(re.search(r' m=(\d+)', line).group(1))
        E = [tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([^)]*)\)', line)]
        print((n, m), 'contains F7:', contains_F7(n, E), ' first (P3) violation (|S|, e(S)):', p3_violations(n, E))
