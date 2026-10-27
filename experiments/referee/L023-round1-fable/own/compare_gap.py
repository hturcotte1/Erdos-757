"""Compare my recomputed GAP lists (engine/cells) with U1's copies (own/u1_gap): as exact sets of FOUND lines (same canon binary,
so canonical forms should coincide line by line) and as sets of edge-sets; print the INFO counters of both."""
import os, re, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p):
    F = set(); info = None
    for l in open(p):
        if l.startswith('FOUND:'): F.add(l.rstrip('\n'))
        if l.startswith('INFO '): info = json.loads(l[5:])
    return F, info
def edgesets(F):
    return set(frozenset(tuple(sorted(map(int, g))) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)) for l in F)
for k in ['23_17_9_D3', '17_15_7_D3', '20_16_8_D3', '21_19_9_D3', '24_20_10_D3']:
    mine = os.path.join(R, 'engine', 'cells', 'cell_%s.txt' % k); u1 = os.path.join(R, 'own', 'u1_gap', 'cell_%s.txt' % k)
    if not os.path.exists(mine): print('%-12s NOT RECOMPUTED (no file)' % k); continue
    Fm, im = load(mine); Fu, iu = load(u1)
    if im is None: print('%-12s INCOMPLETE (no INFO line yet): %d FOUND lines so far' % (k, len(Fm))); continue
    same_lines = Fm == Fu; same_sets = edgesets(Fm) == edgesets(Fu)
    print('%-12s mine %d classes, U1 %d classes; identical FOUND lines: %s; identical as edge sets: %s' % (k, len(Fm), len(Fu), same_lines, same_sets))
    for name, info in (('mine', im), ('U1  ', iu)):
        br = info.get('branches', [])
        print('   %s route=%s inputs=%s ext=%s hits_in_C=%s secs=%s' % (name, info.get('route'), [b.get('inputs') for b in br], [b.get('ext') for b in br], [b.get('hits_in_C') for b in br], info.get('secs')))
