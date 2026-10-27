"""Certified shortcut: if a hypergraph contains (as a sub-hypergraph, injective vertex map, edges to edges) a pattern shown non-realizable by
rexact.decide (obstructions.json, exact), it is non-realizable: a (4,5)-set realizing X restricts to the point set of the image, whose AP
hypergraph contains the image edges.  usage: embed_obs.py classfile tag n"""
import sys, json, re
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
obs = json.load(open('obstructions.json'))
OBS = []; seen = set()
for o in obs:
    k = json.dumps(o['subedges'])
    if k not in seen: seen.add(k); OBS.append(o)
def embeds(P, X):
    Xs = [frozenset(e) for e in X]; inc = {}
    for i, e in enumerate(Xs):
        for v in e: inc.setdefault(v, []).append(i)
    # order pattern edges so each shares a vertex with earlier ones when possible
    order = [0]; rem = list(range(1, len(P)))
    while rem:
        nxt = max(rem, key=lambda i: len(set(P[i]) & {v for j in order for v in P[j]})); order.append(nxt); rem.remove(nxt)
    PE = [P[i] for i in order]
    def rec(k, mp, used, usedE):
        if k == len(PE): return True
        e = PE[k]; mapped = [v for v in e if v in mp]
        if mapped: cand = set(inc.get(mp[mapped[0]], []))
        else: cand = set(range(len(Xs)))
        for xi in cand:
            if xi in usedE: continue
            xe = sorted(Xs[xi]); mp2 = dict(mp); u2 = set(used); ok = True
            # assign unmapped pattern vertices to unused X vertices in this edge, trying all permutations
            import itertools
            un = [v for v in e if v not in mp]; fixed_img = {mp[v] for v in e if v in mp}
            if not fixed_img <= Xs[xi]: continue
            free = [x for x in xe if x not in fixed_img]
            if len(free) != len(un): continue
            for perm in itertools.permutations(free):
                if any(x in used for x in perm): continue
                m3 = dict(mp); 
                for v, x in zip(un, perm): m3[v] = x
                if rec(k + 1, m3, used | set(perm), usedE | {xi}): return True
        return False
    return rec(0, {}, set(), set())
if __name__ == '__main__':
    fn, tag, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    res = []
    for ci, l in enumerate(l for l in open(fn) if l.startswith('FOUND:')):
        X = parse(l); hit = None
        for oi, o in enumerate(OBS):
            if embeds([tuple(e) for e in o['subedges']], X): hit = oi; break
        res.append(dict(cls=ci, obstruction=hit))
    json.dump(dict(obstructions=[dict(k=o['k'], nverts=o['nverts'], subedges=o['subedges']) for o in OBS], classes=res), open('embed_%s.json' % tag, 'w'))
    print(tag, 'classes', len(res), 'with obstruction', sum(r['obstruction'] is not None for r in res), 'without', [r['cls'] for r in res if r['obstruction'] is None])
