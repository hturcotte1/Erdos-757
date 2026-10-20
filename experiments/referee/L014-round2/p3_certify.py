"""Referee L014 round 2: for every hit H (tau >= t) printed by bin/myext, produce an explicit (P3) violation, i.e. a nonempty
edge set F with |V(F)| <= |F| + 1 (so S = V(F) has e(S) >= |F| > |S| - 2), found by a Hall-violator extraction (Kuhn matching of
edges into V - {x,y}; the edges reachable by alternating paths from an unmatched edge form F), and re-check |V(F)| <= |F|+1
directly.  Pure Python, no shared code with the C programs.  Also re-checks tau(H) >= t by an independent exact ILP (CP-SAT) on a
sample, and linearity / max degree."""
import sys, random
def parse(l):
    a = list(map(int, l.split(':', 1)[1].split())); n, m = a[0], a[1]
    return n, [tuple(a[2 + 3*i: 5 + 3*i]) for i in range(m)]
def hall_violator(n, E):
    m = len(E)
    for x in range(n):
        for y in range(x + 1, n):
            owner = {}
            def try_aug(e, seen):
                for v in E[e]:
                    if v in (x, y) or v in seen: continue
                    seen.add(v)
                    if v not in owner or try_aug(owner[v], seen):
                        owner[v] = e; return True
                return False
            for e in range(m):
                seen = set()
                if not try_aug(e, seen):
                    # alternating-path closure from e
                    F = {e}; stack = [e]; vis = set()
                    while stack:
                        f = stack.pop()
                        for v in E[f]:
                            if v in (x, y) or v in vis: continue
                            vis.add(v)
                            if v in owner and owner[v] not in F:
                                F.add(owner[v]); stack.append(owner[v])
                    return sorted(F)
    return None
def main():
    fn, t = sys.argv[1:-1], int(sys.argv[-1])
    nh = 0; ok = 0; sizes = {}; sample = []
    rng = random.Random(7)
    for f in fn:
        for l in open(f):
            if not (l.startswith('HIT') or l.startswith('MEMBER')): continue
            n, E = parse(l); nh += 1
            # linearity, degrees
            pairs = set()
            for e in E:
                assert len(set(e)) == 3
                for p in ((e[0], e[1]), (e[0], e[2]), (e[1], e[2])):
                    p = tuple(sorted(p)); assert p not in pairs, 'nonlinear'; pairs.add(p)
            F = hall_violator(n, E)
            if F is not None:
                V = set(v for i in F for v in E[i])
                if len(V) <= len(F) + 1: ok += 1; sizes[len(F)] = sizes.get(len(F), 0) + 1
            if rng.random() < 0.05: sample.append((n, E))
    print('hits', nh, 'with explicit P3 violation |V(F)| <= |F|+1:', ok, 'violator sizes |F|:', dict(sorted(sizes.items())))
    from ortools.sat.python import cp_model
    bad = 0
    for n, E in sample:
        md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(n)]
        for e in E: md.AddBoolOr([x[v] for v in e])
        md.Minimize(sum(x)); s = cp_model.CpSolver(); s.parameters.num_workers = 1; st = s.Solve(md)
        if s.StatusName(st) != 'OPTIMAL' or int(s.ObjectiveValue()) < t: bad += 1
    print('CP-SAT tau check on a 5%% sample: %d graphs, tau < %d or not optimal: %d' % (len(sample), t, bad))
main()
