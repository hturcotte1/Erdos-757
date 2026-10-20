"""(L016) python3 top_info16.py CELLDIR key [key ...]: prints the class count and, per branch, the decompositions with their input
counts and the ext_d counters recorded in the INFO line of each cell file (engine.cell / stream.recurse)."""
import sys, os, json
d = sys.argv[1]
for k in sys.argv[2:]:
    n, m, t, D = map(int, k.split(','))
    p = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    lines = open(p).read().splitlines(); nf = sum(1 for l in lines if l.startswith('FOUND:'))
    info = json.loads([l for l in lines if l.startswith('INFO ')][0][5:])
    print('CELL (%d,%d,%d,%d): %d classes, route %s, secs %s, connected_hits %s' % (n, m, t, D, nf, info['route'], info.get('secs'), info.get('connected_hits')))
    for b in info.get('branches', []):
        print('  branch d=%d t\'=%d S\'=%d: %d decompositions, %d inputs' % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs']))
        for dec, s in b['dec']:
            if s or len(b['dec']) <= 20: print('     %s: %d' % (dec, s))
        if 'ext' in b: print('     ext_d:', ' '.join('%s=%s' % kv for kv in b['ext'].items()), '| HIT lines', b.get('hits_in_C'))
        for f in b.get('filt_chunks', []): print('     filt:', f)
