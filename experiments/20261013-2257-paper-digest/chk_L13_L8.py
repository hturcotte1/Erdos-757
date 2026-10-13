import itertools
def tau(n,E):
    for k in range(n+1):
        for T in itertools.combinations(range(n),k):
            if all(set(T)&set(e) for e in E): return k
def L(n): return [tuple(sorted(((i)%n,(i+1)%n,(i+3)%n))) for i in range(n)]
def linear(E): return all(len(set(a)&set(b))<=1 for a,b in itertools.combinations(E,2))
for n in (8,13):
    E=L(n); print('L',n,len(set(E)),'tau',tau(n,E),'linear',linear(E))
# F8
pts=[(x,y) for x in range(3) for y in range(3)]
lines=set()
for p,q in itertools.combinations(pts,2):
    lines.add(frozenset(r for r in pts if ((r[0]-p[0])*(q[1]-p[1])-(r[1]-p[1])*(q[0]-p[0]))%3==0))
V=pts[1:]; idx={p:i for i,p in enumerate(V)}
F8=[tuple(sorted(idx[p] for p in l)) for l in lines if pts[0] not in l]
S=set(map(frozenset,F8)); E=L(8)
for perm in itertools.permutations(range(8)):
    if all(frozenset(perm[v] for v in e) in S for e in E): print('L(8) ~ F8 (AG(2,3) minus a point)'); break
# F7-freeness of L(13): any 5 edges forming F7? brute: F7 = vertex v with 3 disjoint-otherwise edges (v,a,b),(v,c,d),(v,e,f) and two edges abc..: 135, 246 type
def has_F7(n,E):
    Es=[frozenset(e) for e in E]
    for v in range(n):
        inc=[e for e in Es if v in e]
        for tri in itertools.combinations(inc,3):
            pairs=[tuple(e-{v}) for e in tri]
            # need two edges e4,e5 each meeting each pair in one vertex, disjoint from each other, avoiding v, using all 6 points
            pts6=[x for p in pairs for x in p]
            if len(set(pts6))<6: continue
            cands=[e for e in Es if v not in e and e<=set(pts6) and all(len(e&set(p))==1 for p in pairs)]
            for a,b in itertools.combinations(cands,2):
                if not a&b: return True
    return False
print('L13 F7?',has_F7(13,L(13)),'L8 F7?',has_F7(8,L(8)))
