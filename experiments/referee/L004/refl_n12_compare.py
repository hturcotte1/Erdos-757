"""Referee L004, check V: the split driver WITH --refl at n=12 must output exactly one representative of each
reflection orbit of the certified L002 census (2,226,490 labelled = 1,113,245 orbits, no symmetric pattern).
usage: python3 refl_n12_compare.py SPLIT_OUTDIR   (own pchk for canonical keys)"""
import gzip, glob, json, sys, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
def keys_of(lines):
    out = subprocess.run([os.path.join(HERE, 'pchk'), '12'], input=''.join(lines), capture_output=True, text=True, check=True).stdout.splitlines()
    return out
L002 = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/n12_m10_all.jsonl.gz'
lines = [' '.join('%d,%d,%d' % tuple(e) for e in json.loads(l)) + '\n' for l in gzip.open(L002, 'rt')]
o = keys_of(lines)
ref = set(l.split()[8] for l in o)
print('L002 labelled', len(lines), 'orbits', len(ref), 'alpha<=7 all:', all(int(l.split()[5]) <= 7 for l in o))
sp = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*_prefix_*.jsonl.gz'))):
    sp += [' '.join('%d,%d,%d' % tuple(e) for e in json.loads(l)) + '\n' for l in gzip.open(f, 'rt')]
o2 = keys_of(sp)
canon_all = all(l.split()[6] == '1' for l in o2)
k2 = [l.split()[8] for l in o2]
print('split --refl output', len(sp), 'all canonical:', canon_all, 'distinct', len(set(k2)), 'equal to L002 orbit set:', set(k2) == ref)
