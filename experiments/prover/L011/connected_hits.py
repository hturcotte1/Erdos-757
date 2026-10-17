"""(L011) Second route to the 'no connected member of C' conclusions: keep the CONNECTED hits first (vertex set {0..N-1}, a vertex in
no edge being its own component), write them as HIT lines to OUT, and report how many there are; OUT is then run through filter_hits.
Usage: connected_hits.py SRC OUT N"""
import re, sys
src, out, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
tot = conn = 0
with open(out, 'w') as f:
    for l in open(src):
        if not l.startswith('HIT:'): continue
        tot += 1
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
        adj = {v: set() for v in range(N)}
        for e in es:
            for a in e:
                adj[a].update(e)
        seen = {0}; st = [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if len(seen) == N: conn += 1; f.write(l)
print(src, 'hits', tot, 'connected (on %d vertices)' % N, conn)
