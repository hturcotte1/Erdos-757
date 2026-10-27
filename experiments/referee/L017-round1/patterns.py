# Referee L017 round 1: independent enumeration of the Hall-deficient distributions of the six co-vertices
# a,b | c,d | e,f of a degree-3 vertex over r components (every component met), up to symmetry.
import itertools
def has_matching(pairs_nbrs):
    # pairs_nbrs: list of 3 sets of components; is there an SDR?
    for perm in itertools.permutations(range(3)):
        pass
    comps = set().union(*pairs_nbrs)
    for choice in itertools.product(*[sorted(s) for s in pairs_nbrs]):
        if len(set(choice)) == 3: return True
    return False
def canon(assign, r):
    # assign: tuple of 6 component labels for (a,b,c,d,e,f); symmetries: permute pairs, swap within pairs, relabel comps
    best = None
    for pp in itertools.permutations(range(3)):
        for sw in itertools.product((0, 1), repeat=3):
            seq = []
            for j in pp:
                x, y = assign[2*j], assign[2*j+1]
                if sw[j]: x, y = y, x
                seq += [x, y]
            # relabel components in order of first appearance
            rel = {}; out = []
            for c in seq:
                if c not in rel: rel[c] = len(rel)
                out.append(rel[c])
            t = tuple(out)
            if best is None or t < best: best = t
    return best
total = {}
for r in range(1, 7):
    orbits_def = set(); orbits_all = set()
    for assign in itertools.product(range(r), repeat=6):
        if len(set(assign)) != r: continue      # every component contains a co-vertex
        nb = [{assign[0], assign[1]}, {assign[2], assign[3]}, {assign[4], assign[5]}]
        c = canon(assign, r)
        orbits_all.add(c)
        if not has_matching(nb): orbits_def.add(c)
    total[r] = (len(orbits_all), sorted(orbits_def))
    print('r=%d: %d distributions up to symmetry, %d Hall-deficient:' % (r, len(orbits_all), len(orbits_def)))
    for o in sorted(orbits_def):
        desc = []
        for j in range(3):
            x, y = o[2*j], o[2*j+1]
            desc.append(('in F%d' % (x+1)) if x == y else ('split F%d/F%d' % (x+1, y+1)))
        print('   ', o, '; '.join(desc))
print('total Hall-deficient patterns:', sum(len(v[1]) for v in total.values()))
