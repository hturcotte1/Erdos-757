"""(L014) python3 top_info.py CELLDIR key ... : the INFO record of the given cells (route, branches with every decomposition and its number
of inputs, ext_d counters, filt summaries, connected_hits, seconds) in readable form."""
import sys, os, json
d = sys.argv[1]
for k in sys.argv[2:]:
    key = tuple(map(int, k.split(','))); fn = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key); info = None; reps = 0
    for l in open(fn):
        if l.startswith('FOUND:'): reps += 1
        elif l.startswith('INFO '): info = json.loads(l[5:])
    print('cell %s: %d classes, route %s, %s s' % (key, reps, info['route'], info.get('secs')))
    if info['route'] == 'direct': print('   ', info.get('enum')); print('   ', info.get('filt'))
    for b in info.get('branches', []):
        print('  branch d=%d t\'=%d S\'=%d: %d decompositions, %d inputs' % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs']))
        for dec, size in b['dec']: print('      %s: %d' % (' + '.join('(%d,%d,%d)' % tuple(x) for x in dec), size))
        if 'ext' in b: print('    ext_d:', ' '.join('%s=%s' % kv for kv in b['ext'].items()), '| HIT lines', b.get('hits_in_C'))
        for f in b.get('filt_chunks', []): print('    filt:', f)
    if info['route'] == 'recurse': print('  connected_hits', info.get('connected_hits'))
