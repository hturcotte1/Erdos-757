"""(L014) Cross-check (b): python3 compare_cells.py MYDIR NAME=DIR ...
For every cell file cell_n_m_t_D<D>.txt of MYDIR (complete: has an INFO line) and every reference directory that has a file of the same
name (complete), compares the sets of representatives (the FOUND lines: canonical forms of nauty via the same canon binary, so equal
classes give equal strings).  Prints one line per cell and a summary per reference.  Reference files are only read."""
import sys, os, re, json
def load(fn):
    reps = []; done = False
    with open(fn) as f:
        for l in f:
            if l.startswith('FOUND:'): reps.append(l.rstrip('\n'))
            elif l.startswith('INFO '): done = True
    return reps, done
mydir = sys.argv[1]; refs = [a.split('=', 1) for a in sys.argv[2:]]
stat = {name: [0, 0, 0] for name, _ in refs}   # common, equal, different
rows = []
for fn in sorted(os.listdir(mydir)):
    if not re.match(r'cell_\d+_\d+_\d+_D\d+\.txt$', fn): continue
    mine, done = load(os.path.join(mydir, fn))
    if not done: rows.append('%s INCOMPLETE' % fn); continue
    ms = set(mine); assert len(ms) == len(mine), ('duplicate representative', fn)
    parts = ['%s mine=%d' % (fn, len(mine))]
    for name, d in refs:
        p = os.path.join(d, fn)
        if not os.path.exists(p): continue
        rr, rdone = load(p)
        if not rdone: parts.append('%s=incomplete' % name); continue
        stat[name][0] += 1
        if set(rr) == ms and len(rr) == len(set(rr)): stat[name][1] += 1; parts.append('%s=%d EQUAL' % (name, len(rr)))
        else: stat[name][2] += 1; parts.append('%s=%d DIFFERENT (only mine %d, only ref %d)' % (name, len(rr), len(ms - set(rr)), len(set(rr) - ms)))
    rows.append(' '.join(parts))
for r in rows: print(r)
for name, (c, e, dd) in stat.items(): print('SUMMARY vs %s: common cells %d, equal %d, different %d' % (name, c, e, dd))
