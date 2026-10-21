#!/usr/bin/env python3
"""Referee L016 round 1 (own code): build the inputs X - w of one engine branch from the cell lists.
Usage: build_inputs.py N M T D outfile [listdir_override_for_type n_m_t=path ...]
For every decomposition of (N,M,T) (own brute force, mydecomp.decomps, no K8) and every multiset choice of classes from
the lists cell(n,m,t,D) (combinations with replacement for repeated types), writes one line "m a1 b1 c1 ..." with the
components placed on consecutive labels (isolated vertices take one label each).  Lists are looked up in the seed
directories of L013/L014 and in the prover's new lists (cells_new/runF, runA); a type whose list is missing is reported."""
import sys, os, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mydecomp import decomps

BASE = '/home/user/Erdos-757/experiments/referee/L016-round1/out'
DIRS = [BASE + '/seeds/L014/cells', BASE + '/seeds/L014', BASE + '/seeds/L013/cells',
        BASE + '/new/cells_new/runF', BASE + '/new/cells_new/runA']

_cache = {}
def parse_found(line):
    body = line[len('FOUND:'):].strip()
    es = []
    for tok in body.split():
        a, b, c = map(int, tok.strip('()').split(','))
        es.append((a, b, c))
    return es

def load(n, m, t, D, override=None):
    key = (n, m, t, D)
    if key in _cache:
        return _cache[key]
    name = 'cell_%d_%d_%d_D%d.txt' % key
    found = []
    paths = []
    if override and ('%d_%d_%d' % (n, m, t)) in override:
        paths = [override['%d_%d_%d' % (n, m, t)]]
    else:
        paths = [os.path.join(d, name) for d in DIRS if os.path.exists(os.path.join(d, name))]
    if not paths:
        _cache[key] = None
        return None
    sets = []
    for p in paths:
        s = [l.rstrip('\n') for l in open(p) if l.startswith('FOUND:')]
        sets.append(s)
    for s in sets[1:]:
        if set(s) != set(sets[0]):
            raise SystemExit('lists differ for %s: %s' % (name, paths))
    res = [parse_found(l) for l in sets[0]]
    for es in res:
        if len(es) != m or any(max(e) >= n for e in es):
            raise SystemExit('bad graph in %s' % name)
    _cache[key] = res
    return res

def main():
    N, M, T, D = map(int, sys.argv[1:5]); outfile = sys.argv[5]
    override = {}
    for a in sys.argv[6:]:
        k, v = a.split('=')
        override[k] = v
    ds = decomps(N, M, T)
    total = 0
    with open(outfile, 'w') as fo:
        for dec in ds:
            groups = {}
            for ty in dec:
                groups[ty] = groups.get(ty, 0) + 1
            choices = []
            cnt = 1
            missing = []
            for ty, k in sorted(groups.items()):
                if ty == (1, 0, 0):
                    lst = [[]]
                else:
                    lst = load(ty[0], ty[1], ty[2], D, override)
                    if lst is None:
                        missing.append(ty); lst = []
                choices.append((ty, k, lst))
                cnt *= math.comb(len(lst) + k - 1, k)
            print('DEC', dec, 'inputs', cnt, ('MISSING ' + str(missing)) if missing else '', file=sys.stderr)
            total += cnt
            if cnt == 0:
                continue
            per_type = [list(itertools.combinations_with_replacement(range(len(lst)), k)) for (ty, k, lst) in choices]
            for combo in itertools.product(*per_type):
                edges = []
                off = 0
                for (ty, k, lst), idxs in zip(choices, combo):
                    for ix in idxs:
                        for (a, b, c) in lst[ix]:
                            edges.append((a + off, b + off, c + off))
                        off += ty[0]
                assert off == N
                fo.write('%d %s\n' % (len(edges), ' '.join('%d %d %d' % e for e in edges)))
    print('TOTAL inputs', total, 'decompositions', len(ds), file=sys.stderr)

if __name__ == '__main__':
    main()
