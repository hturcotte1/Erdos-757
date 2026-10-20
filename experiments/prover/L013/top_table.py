"""(L013, prover) Print, for each top-level cell, the recursion branches recorded in its INFO line (d, t', S', decompositions with the
number of inputs each, ext_d counters, filt summary, connected hits, classes).  Usage: python3 top_table.py CELLDIR n m t D [n m t D ...]"""
import sys, os, json
cd = sys.argv[1]; a = list(map(int, sys.argv[2:]))
for i in range(0, len(a), 4):
    key = tuple(a[i:i + 4]); fn = os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % key)
    lines = open(fn).read().splitlines(); reps = [l for l in lines if l.startswith('FOUND:')]
    info = json.loads([l for l in lines if l.startswith('INFO ')][0][5:])
    print('CELL %s classes=%d route=%s secs=%s connected_hits=%s' % (key, len(reps), info['route'], info.get('secs'), info.get('connected_hits')))
    for b in info.get('branches', []):
        e = b.get('ext', {})
        print("  branch d=%d t'=%d S'=%d: %d decompositions, %d inputs; ext_d: graphs=%s bad_tau=%s nodes=%s hits_F7free=%s hits_in_C=%s"
              % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], e.get('graphs'), e.get('bad_tau'), e.get('nodes'), e.get('hits_F7free'), e.get('hits_in_C')))
        for dec, size in b['dec']:
            print('      %-60s inputs %d' % (' + '.join('(%d,%d,%d)' % tuple(c) for c in dec), size))
    for f in info.get('filt', []): print('  filt:', f)
