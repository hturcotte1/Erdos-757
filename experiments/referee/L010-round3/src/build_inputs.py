"""Referee L010 round 3: extension inputs from MY class representatives (one labelled representative per isomorphism class of each
component cell, taken from my genbg output and filtered by my class-C test), as disjoint unions over every decomposition.
Usage: build_inputs.py STEP MODE OUT, STEP in {X (17,9)/3, H19 (18,12)/1, H20 (19,10)/0}, MODE in {C, all}.
Output lines: "m a1 b1 c1 ..." on vertices 0..NV-1 with the isolated vertex (if any) as the last label."""
import sys, re, subprocess, itertools, os
step, mode, out = sys.argv[1:4]
D = {'X': (17, 9, 3), 'H19': (18, 12, 1), 'H20': (19, 10, 0)}[step]
# decompositions re-derived here independently (same brute force as arith.py)
def cells(nmax, smax):
    out = []
    for n in range(3, nmax + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            for t in range(0, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= smax and 17 * t <= 5 * n + 3 * m: out.append((n, m, t, s))
    return out + [(1, 0, 0, 3)]
def decomps(N, M, S):
    pieces = sorted(set(cells(N, S))); sols = []
    def rec(i, n, m, s, chosen):
        if (n, m, s) == (N, M, S): sols.append(tuple(chosen)); return
        if i == len(pieces) or n > N or m > M or s > S: return
        pn, pm, pt, ps = pieces[i]; k = 0
        while n + k * pn <= N and m + k * pm <= M and s + k * ps <= S:
            rec(i + 1, n + k * pn, m + k * pm, s + k * ps, chosen + [(pn, pm, pt)] * k); k += 1
    rec(0, 0, 0, 0, []); return sols
def reps(n, m, t):
    """one labelled representative per class of connected linear (n,m,>=t) graphs with Delta<=3 (my genbg), in C if mode=='C'"""
    if (n, m, t) == (3, 1, 1): return [[(0, 1, 2)]]
    if (n, m, t) == (1, 0, 0): return [[]]
    f = 'out/g_%d_%d_%d_d3.txt' % (n, m, t)
    if not os.path.exists(f):
        subprocess.run('TAU0=%d ./bin/genbg32 -q -c -Z1 -d1:3 -D3:3 %d %d %d:%d > %s 2>/dev/null' % (t, n, m, 3 * m, 3 * m, f), shell=True, check=True)
    lines = [l for l in open(f) if l.startswith('FOUND')]
    if mode == 'C':
        r = subprocess.run(['./bin/myfilter', 'FOUND', str(n), 'notau', 'all'], input=''.join(lines), capture_output=True, text=True).stdout
        lines = [l.split('| ', 1)[1] + '\n' for l in r.splitlines() if l.startswith('SURVIVOR')]
    can = subprocess.run(['./bin/canon', str(n)], input=''.join(lines), capture_output=True, text=True).stdout.splitlines()
    assert len(can) == len(lines)
    seen = {}; 
    for c, l in zip(can, lines):
        if c not in seen: seen[c] = [tuple(map(int, x.split(','))) for x in re.findall(r'\(([\d,]+)\)', l)]
    return list(seen.values())
total = 0; summary = []
with open(out, 'w') as fo:
    for dec in decomps(*D):
        iso = [p for p in dec if p == (1, 0, 0)]; others = [p for p in dec if p != (1, 0, 0)]
        lists = [reps(*p) for p in others]
        cnt = 0
        for combo in itertools.product(*lists):
            es = []; off = 0
            for (n, m, t), comp in zip(others, combo):
                es += [tuple(v + off for v in e) for e in comp]; off += n
            off += len(iso)
            assert off == D[0]
            fo.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
        summary.append((list(dec), [len(l) for l in lists], cnt)); total += cnt
for s in summary: print('decomposition %s: class counts %s -> %d inputs' % tuple(s))
print('total inputs:', total, '->', out)
