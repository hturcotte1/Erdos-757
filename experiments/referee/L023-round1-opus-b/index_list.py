"""Own canonical forms (hg.canon) of every graph of a stored cell list; writes a pickle {form: index}; reports duplicates
(two stored graphs isomorphic) and the max leaf count.  usage: python3 index_list.py LISTFILE n OUT.pkl"""
import sys, pickle, time
from hg import parse, canon
fn, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
idx = {}; dup = 0; maxl = 0; t0 = time.time(); k = 0; info = 0
with open(fn) as f:
    for l in f:
        if l.startswith('INFO'): info += 1; continue
        if not l.startswith('FOUND'): continue
        E = parse(l); c, lv = canon(n, E); maxl = max(maxl, lv)
        if c in idx: dup += 1
        else: idx[c] = k
        k += 1
        if k % 50000 == 0: print('progress', k, round(time.time() - t0), flush=True)
pickle.dump(idx, open(out, 'wb'))
print('LIST %s graphs %d distinct_forms %d duplicates %d max_leaves %d INFO_lines %d secs %.0f' % (fn, k, len(idx), dup, maxl, info, time.time() - t0), flush=True)
