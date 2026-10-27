# for the 141 graphs of pendant_census_n13_R2.txt: max distance from the nearest pendant vertex of the vertices of the smallest Red set found
import re, collections
cnt = collections.Counter()
for line in open('pendant_census_n13_R2.txt'):
    if "('global'" not in line: continue
    n = int(line.split()[0])
    Z = tuple(map(int, re.search(r"\('global', \d+, \(([^)]*)\)\)", line).group(1).replace(' ', '').strip(',').split(',')))
    E = [tuple(map(int, t.split('.'))) for t in line.split()[-int(line.split()[1]):]]
    nb = collections.defaultdict(set); d = collections.Counter()
    for e in E:
        for v in e: nb[v] |= set(e); d[v] += 1
    pend = [v for v in range(n) if d[v] == 1]
    best = None
    for y in pend:
        dist = {y: 0}; fr = [y]
        while fr:
            nf = []
            for u in fr:
                for w in nb[u]:
                    if w not in dist: dist[w] = dist[u] + 1; nf.append(w)
            fr = nf
        r = max(dist[z] for z in Z)
        best = r if best is None else min(best, r)
    cnt[(len(Z), best)] += 1
print('(|Z|, radius from nearest pendant needed) counts:', sorted(cnt.items()))
