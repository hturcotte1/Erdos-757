import sys, math, json
from plan2 import *
def size_of(dec, known):
    """dec = list of (comps) -> (size or None, unknown list)"""
    if dec['comps'] is None: return 0, []
    size = 1; unk = []
    for ck, kk in dec['comps']:
        c = known.get(ck)
        if c is None: unk.append(ck); continue
        size *= math.comb(c + kk - 1, kk)
    return size, unk
if __name__ == '__main__':
    name = sys.argv[1]; tops = tops_for(name); seen = build(tops)
    known = {k: v['count'] for k, v in seen.items() if v['exists']}
    new = sorted([k for k, v in seen.items() if not v['exists']], key=lambda k: (k[0], k[1], k[3]))
    for k in new:
        v = seen[k]; print(k, 's=%d' % (3*k[0]+2*k[1]-11*k[2]), 'direct' if v['direct'] else '')
        for b in v['branches']:
            tot = 0; unkset = set(); parts = []
            for dec in b['decs']:
                sz, unk = size_of(dec, known); tot += sz; unkset |= set(unk)
                if unk or sz > 1000: parts.append(('%s' % ('+'.join('%dx%s' % (kk, c[:3]) for c, kk in dec['comps'])) if dec['comps'] else 'void', sz, unk))
            print('   d=%d tp=%d S\'=%d ndec=%d known_inputs=%d unknown_cells=%s' % (b['d'], b['tp'], b['Sp'], b['ndec'], tot, sorted(unkset)))
            for p in sorted(parts, key=lambda p: -p[1])[:6]: print('        ', p)
