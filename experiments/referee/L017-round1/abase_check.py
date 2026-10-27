# Referee L017 round 1: sanity checks of the certificate on A_base (own AP hypergraph and own co-transversality code).
import itertools, subprocess, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
idx = {a: i for i, a in enumerate(A)}
E = []
for i, j in itertools.combinations(range(len(A)), 2):
    s2 = A[i] + A[j]
    if s2 % 2 == 0 and s2 // 2 in idx and idx[s2 // 2] not in (i, j):
        E.append(tuple(sorted((i, idx[s2 // 2], j))))
E = sorted(set(E)); n = len(A); m = len(E)
deg = collections.Counter(v for e in E for v in e)
inp = '%d %d %s\n' % (n, m, ' '.join('%d %d %d' % e for e in E))
out = subprocess.run([os.path.join(HERE, 'src', 'cotrans')], input=inp, capture_output=True, text=True).stdout.split()
t = int(out[0].split('=')[1]); ncv = int(out[1].split('=')[1])
print('A_base: n=%d m=%d tau=%d s=%d degrees=%s non-co-transversal vertices=%d' % (n, m, t, 3*n+2*m-11*t, sorted(deg.values()), ncv))
# delete the degree-4 vertex
v = max(deg, key=lambda x: deg[x]); print('degree-4 vertex', A[v], deg[v])
W = [x for x in range(n) if x != v]; ren = {x: i for i, x in enumerate(W)}
E2 = [tuple(ren[x] for x in e) for e in E if v not in e]
inp2 = '%d %d %s\n' % (len(W), len(E2), ' '.join('%d %d %d' % e for e in E2))
out2 = subprocess.run([os.path.join(HERE, 'src', 'cotrans')], input=inp2, capture_output=True, text=True).stdout.split()
t2 = int(out2[0].split('=')[1]); print('A_base - 0: n=%d m=%d tau=%d s=%d' % (len(W), len(E2), t2, 3*len(W)+2*len(E2)-11*t2))
# components
adj = collections.defaultdict(set)
for e in E2:
    for x in e: adj[x] |= set(e) - {x}
seen = set(); comps = []
for x in range(len(W)):
    if x in seen: continue
    st = [x]; c = {x}; seen.add(x)
    while st:
        y = st.pop()
        for z in adj[y]:
            if z not in seen: seen.add(z); c.add(z); st.append(z)
    comps.append(c)
for c in comps:
    Ec = [e for e in E2 if set(e) <= c]
    print('  component size', len(c), 'edges', len(Ec))
