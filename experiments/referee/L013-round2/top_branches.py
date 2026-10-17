import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_ref import decomps
D_ = sys.argv[1]
tops = [(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3),
        (21,18,9,3),(23,15,9,3),(24,14,9,3),(24,19,10,3),(25,18,10,3)]
def size(typ, d):
    if typ == (1,0,0): return 1
    p = os.path.join(D_, 'cell_%d_%d_%d_D%d.txt' % (typ + (d,)))
    if not os.path.exists(p): return 'nofile'
    return sum(1 for l in open(p) if l.startswith('FOUND:'))
for key in tops:
    p = os.path.join(D_, 'cell_%d_%d_%d_D%d.txt' % key)
    reps = sum(1 for l in open(p) if l.startswith('FOUND:')); info = json.loads([l for l in open(p) if l.startswith('INFO ')][0][5:])
    print('CELL', key, 'classes', reps, 'route', info['route'], 'connected_hits', info.get('connected_hits'))
    for b in info.get('branches', []):
        print('  branch d=%d tp=%d Sp=%d decs=%d inputs=%d ext=%s' % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], b.get('ext')))
        for dec, sz in b['dec']:
            print('     ', dec, 'inputs', sz, 'cells', [(tuple(x), size(tuple(x), b['d'])) for x in dec if tuple(x) != (3,1,1)][:6])
