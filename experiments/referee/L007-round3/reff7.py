"""Referee F7 detector, straight from the definition: H contains F7 iff there is an injective map
phi:{0..6}->V(H) with phi(e) in E(H) for each of the 5 edges e of F7 (not necessarily induced).
Backtracking over phi(0),phi(1),...,phi(6); an F7-edge is checked as soon as its 3 vertices are mapped."""
import itertools, random
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def contains(edges, pattern=F7, k=7):
    E = set(frozenset(e) for e in edges)
    V = sorted(set().union(*map(set, edges))) if edges else []
    # edges of the pattern that become checkable once vertex i is mapped
    chk = {i: [e for e in pattern if max(e) == i] for i in range(k)}
    phi = {}
    def rec(i, used):
        if i == k: return True
        for v in V:
            if v in used: continue
            phi[i] = v
            if all(frozenset(phi[x] for x in e) in E for e in chk[i]):
                if rec(i+1, used | {v}): return True
        phi.pop(i, None)
        return False
    return rec(0, frozenset())
def linear(edges):
    seen=set()
    for e in edges:
        for p in itertools.combinations(sorted(e),2):
            if p in seen: return False
            seen.add(p)
    return True
if __name__ == '__main__':
    fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    ag23 = []  # AG(2,3): points (x,y) in Z3^2 -> 3x+y; lines
    pts = [(x,y) for x in range(3) for y in range(3)]
    lines=set()
    for p in pts:
        for d in [(0,1),(1,0),(1,1),(1,2)]:
            L = frozenset(((p[0]+t*d[0])%3*3+(p[1]+t*d[1])%3) for t in range(3)); lines.add(L)
    ag23 = [tuple(sorted(L)) for L in lines]
    assert len(ag23)==12
    f8 = [L for L in ag23 if 8 not in L]
    rnd = random.Random(1); perm = list(range(20)); rnd.shuffle(perm)
    f7_relab = [tuple(perm[x] for x in e) for e in F7]
    l13 = [tuple(sorted({i%13,(i+1)%13,(i+3)%13})) for i in range(13)]
    tests = {
      'F7': (F7, True), 'F7 relabelled into 0..19': (f7_relab, True), 'AG(2,3)': (ag23, True), 'AG(2,3) minus a point (F8)': (f8, True),
      'F7 + pendant edge': (F7+[(6,7,8)], True),
      'Fano plane': (fano, False), 'Fano minus two lines': (fano[:5], False), 'Fano minus lines 0,1': (fano[2:], False),
      'L(13) cyclic {i,i+1,i+3}': (l13, False),
      'F7 minus an edge': (F7[:4], False), 'F7 with edge 246 replaced by 247': (F7[:4]+[(2,4,7)], False),
      'F7 with 135 replaced by 137, 246 by 246': (F7[:3]+[(1,3,7),(2,4,6)], False),
    }
    ok=True
    for name,(ed,want) in tests.items():
        got = contains(ed)
        print(f'{name:45s} linear={linear(ed)} contains_F7={got} expected={want}', '' if got==want else '  <-- WRONG')
        ok &= (got==want)
    print('ALL CONTROLS OK' if ok else 'CONTROL FAILURE')
