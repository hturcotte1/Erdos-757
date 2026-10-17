"""(L014) python3 compare_branches.py MYDIR NAME=DIR ... : for every recursion cell present (complete) in MYDIR and in a reference
directory, compares the branch data recorded in the INFO lines: (d, t', S', number of decompositions, number of inputs, the ext_d
counters graphs/bad_tau/tg_too_small/searched/max_min_covers/nodes/hits_F7free/hits_in_C) and connected_hits."""
import sys, os, re, json
def info(fn):
    for l in open(fn):
        if l.startswith('INFO '): return json.loads(l[5:])
    return None
KEYS = ('graphs', 'bad_tau', 'tg_too_small', 'searched', 'max_min_covers', 'nodes', 'hits_F7free', 'hits_in_C')
def sig(inf):
    return ([(b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], tuple(b.get('ext', {}).get(k) for k in KEYS)) for b in inf.get('branches', [])], inf.get('connected_hits'))
mydir = sys.argv[1]
for name, d in (a.split('=', 1) for a in sys.argv[2:]):
    common = eq = 0; diffs = []
    for fn in sorted(os.listdir(mydir)):
        if not re.match(r'cell_\d+_\d+_\d+_D\d+\.txt$', fn): continue
        a = info(os.path.join(mydir, fn))
        if not a or a.get('route') != 'recurse': continue
        p = os.path.join(d, fn)
        if not os.path.exists(p): continue
        b = info(p)
        if not b or b.get('route', '').split('(')[0] != 'recurse': continue
        common += 1
        if sig(a) == sig(b): eq += 1
        else: diffs.append(fn)
    print('vs %s: common recursion cells %d, identical branch data %d, different %d %s' % (name, common, eq, len(diffs), diffs))
