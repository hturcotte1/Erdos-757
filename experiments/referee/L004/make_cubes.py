"""Referee L004: cube lists for the SAT checks.
all depth-3 cubes = every choice of a triple with middle 1, a triple with middle 2, a triple with middle 3 (no filtering);
noncensus = those not in the census prefix list; census strata by the census per-prefix time; random sample seeded."""
import itertools, json, random, sys, os
n = 14
R = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/n14/results'
pl = open(os.path.join(R, 'n14_m12_prefixes.txt')).read().split()
ps = set(pl)
allc = []
for k1 in range(2, n):
    for i2 in range(0, 2):
        for k2 in range(3, n):
            for i3 in range(0, 3):
                for k3 in range(4, n):
                    allc.append('0-%d,%d-%d,%d-%d' % (k1, i2, k2, i3, k3))
print('all cubes', len(allc), 'census prefixes', len(pl), 'census subset of all:', ps <= set(allc))
non = [c for c in allc if c not in ps]
open('cubes_noncensus.txt', 'w').write('\n'.join(non) + '\n')
times = {}
for q, p in enumerate(pl):
    d = json.load(open(os.path.join(R, 'n14_m12_prefix_%05d.done' % q))); times[q] = float(d['time'])
cheap = [q for q in range(len(pl)) if times[q] <= 10]
rest = [q for q in range(len(pl)) if times[q] > 10]
random.seed(20261015)
samp = sorted(random.sample(rest, 200))
open('cubes_cheap.txt', 'w').write('\n'.join(pl[q] for q in cheap) + '\n')
open('cubes_sample.txt', 'w').write('\n'.join(pl[q] for q in samp) + '\n')
json.dump({'cheap_idx': cheap, 'sample_idx': samp}, open('cube_sets.json', 'w'))
print('noncensus', len(non), 'cheap', len(cheap), 'sample', len(samp), 'sample census time', sum(times[q] for q in samp), 'of', sum(times.values()))
