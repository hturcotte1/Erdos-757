"""Referee L004: coverage of the exhaustive SAT comparisons.
An orbit {P, refl P} is 'exhaustively checked' if at least one of P, refl P lies in a cube that the SAT run enumerated
completely: for such an orbit, presence in the census was verified, and absence from the census would have been
detected. Reports #census prefixes compared, #orbits covered (of 205,529), and the census nodes in compared prefixes.
usage: python3 coverage.py SATOUT.gz [...]"""
import gzip, sys, subprocess, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
R = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/n14/results'
pl = open(os.path.join(R, 'n14_m12_prefixes.txt')).read().split(); pidx = {p: q for q, p in enumerate(pl)}
cubes = set(); models = []
for f in sys.argv[1:]:
    for l in gzip.open(f, 'rt'):
        if l.startswith('# cube'): cubes.add(l.split()[2]); continue
        if l.startswith('#') or not l.strip(): continue
        models.append(' '.join(l.split()[1:]))
out = subprocess.run([os.path.join(HERE, 'pchk'), '14'], input=''.join(m + '\n' for m in models), capture_output=True, text=True, check=True).stdout.splitlines()
orbits = set(l.split()[8] for l in out if l.split()[4] == '0')
cen = [q for c, q in pidx.items() if c in cubes]
nodes = sum(int(json.load(open(os.path.join(R, 'n14_m12_prefix_%05d.done' % q)))['nodes']) for q in cen)
tn = 113454008923
print('cubes enumerated', len(cubes), 'of which census prefixes', len(cen), '(%.1f%% of 2537); census nodes in them %.3g (%.1f%%)' % (100 * len(cen) / 2537, nodes, 100 * nodes / tn))
print('F7-free orbits with a member in an enumerated cube: %d of 205529 (%.1f%%)' % (len(orbits), 100 * len(orbits) / 205529))
