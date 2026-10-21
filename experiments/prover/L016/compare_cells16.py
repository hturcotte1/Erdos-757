"""(L016) python3 compare_cells16.py MINE REF [only_keys_file]: for every cell file of MINE that also exists in REF (or, with a key
file, for the listed keys), compare the sets of FOUND lines (canonical representatives).  Prints one line per cell and a SUMMARY."""
import os, sys
mine, ref = sys.argv[1], sys.argv[2]
keys = None
if len(sys.argv) > 3:
    keys = ['cell_%s_D%s.txt' % ('_'.join(k.split(',')[:3]), k.split(',')[3]) for k in open(sys.argv[3]).read().split()]
def found(p):
    s = set(); done = False
    for l in open(p):
        if l.startswith('FOUND:'): s.add(l.strip())
        elif l.startswith('INFO '): done = True
    return s, done
files = keys if keys is not None else sorted(f for f in os.listdir(mine) if f.startswith('cell_'))
eq = ne = miss = 0
for f in files:
    a, b = os.path.join(mine, f), os.path.join(ref, f)
    if not os.path.exists(a) or not os.path.exists(b):
        miss += 1; print('MISSING', f, os.path.exists(a), os.path.exists(b)); continue
    sa, da = found(a); sb, db = found(b)
    ok = sa == sb and da and db
    eq += ok; ne += (not ok)
    if keys is not None or not ok: print('EQUAL' if ok else 'DIFFERENT', f, len(sa), len(sb))
print('SUMMARY common', eq + ne, 'equal', eq, 'different', ne, 'missing', miss)
