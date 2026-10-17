"""Referee L010 r1: extension inputs from isomorphism-class representatives.
For a target (N, M, slack S) take every decomposition (arith.decomps: all multisets of component cells, isolated vertex
included) and, for every multiset of component CLASSES (one class per component; a cell occurring k times contributes a
k-multiset of its classes), write the disjoint union on consecutive vertex blocks.  Component classes come from the genbg
lists: out/gC_<n>_<m>_<t>.txt (INC lines = members of C) or, with mode 'all', out/g_<n>_<m>_<t>_d3.txt (every class with
Delta <= 3).  The single edge (3,1,1) and the isolated vertex (1,0,0) have one class each.  A cell without a list file is
reported (it must be one that the review shows empty).  Usage: build_reps.py N M S mode outfile"""
import sys, os, re, itertools, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.join(here, '..')
spec = importlib.util.spec_from_file_location('arith_mod', os.path.join(here, 'arith_lib.py')); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
N, M, S, mode, outf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
def classes(c):
    n, m, t = c
    if c == (3, 1, 1): return [[(0, 1, 2)]]
    if c == (1, 0, 0): return [[]]
    f = os.path.join(base, 'out', ('gC_%d_%d_%d.txt' if mode == 'C' else 'g_%d_%d_%d_d3.txt') % c)
    if not os.path.exists(f): return None
    tag = 'INC:' if mode == 'C' else 'FOUND:'
    L = [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in open(f) if l.startswith(tag)]
    for es in L: assert set().union(*map(set, es)) == set(range(n)) and len(es) == m, (c, es)
    return L
tot = 0
with open(outf, 'w') as fo:
    for d in A.decomps(N, M, S):
        cnt = {}
        for c in d: cnt[c] = cnt.get(c, 0) + 1
        lists = {c: classes(c) for c in cnt}
        missing = [c for c in cnt if lists[c] is None]
        if missing: print('  type', list(d), ': NO LIST for', missing); continue
        per = [list(itertools.combinations_with_replacement(range(len(lists[c])), k)) for c, k in cnt.items()]
        k_type = 0
        for choice in itertools.product(*per):
            es = []; off = 0
            for (c, k), idxs in zip(cnt.items(), choice):
                for i in idxs:
                    es += [tuple(v + off for v in e) for e in lists[c][i]]; off += c[0]
            assert off == N and len(es) == M
            fo.write('G: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n'); k_type += 1
        print('  type', list(d), ':', k_type, 'representatives', {c: len(lists[c]) for c in cnt}); tot += k_type
print('total representatives', tot, '->', outf)
