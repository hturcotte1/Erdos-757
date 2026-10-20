"""Referee validation on small cells: for n=3..NMAX and D in {3, unbounded}, every m and every threshold t = 0..tau_max+1,
compare the labelled brute-force count (bf_label, no symmetry reduction) with sum n!/|Aut| over the isomorphism classes output by
(i) nauty genbg + referee tau-prune hook, (ii) the prover's enum_conn, (iii) the falsifier's conn_dfs3; classes and |Aut| by nauty
(canon3).  Also checks that the three class sets are identical and that genbg outputs are pairwise non-isomorphic."""
import subprocess, sys, os, math, collections
R = '/home/user/Erdos-757/experiments/referee/L008-round1'
B = R + '/nauty_build'
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
def run(cmd, env=None, inp=None):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, input=inp).stdout
def canon(text, n):
    out = run(B + '/canon3 FOUND %d' % n, inp=text)
    res = []
    for l in out.splitlines():
        c, aut, ln = l.split(); res.append((c, int(aut)))
    return res
def classes(text, n):
    d = {}
    for c, aut in canon(text, n): d[c] = aut
    return d
bad = 0; cells = 0; nonempty = 0
for n in range(3, NMAX + 1):
    for D in (3, 100):
        bf = collections.defaultdict(lambda: collections.Counter())
        for l in open(R + '/out/bf_n%d_%s.txt' % (n, 'D3' if D == 3 else 'Dinf')):
            nn, m, t, c = map(int, l.split()); bf[m][t] += c
        ms = sorted(m for m in range(1, max(list(bf.keys()) + [1]) + 2) if n <= 2 * m + 1)
        for m in ms:
            tmax = max(bf[m].keys()) if bf[m] else 0
            for t in range(0, tmax + 2):
                Lbf = sum(c for tt, c in bf[m].items() if tt >= t)
                env = dict(os.environ, TAU0=str(t))
                g = run(B + '/genbg_tau -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d' % (min(D, 31), n, m, 3 * m, 3 * m), env=env)
                gl = canon(g, n)
                gcls = {c: a for c, a in gl}
                ec = classes(run(R + '/bin/enum_conn %d %d %d %d 1' % (n, m, t, D)), n)
                cc = classes(run(R + '/bin/conn_dfs3 %d %d %d %d 0 0' % (n, m, t, D)), n)
                Lg = sum(math.factorial(n) // a for a in gcls.values())
                Le = sum(math.factorial(n) // a for a in ec.values())
                Lc = sum(math.factorial(n) // a for a in cc.values())
                ok = (Lbf == Lg == Le == Lc) and set(gcls) == set(ec) == set(cc) and len(gl) == len(gcls)
                cells += 1; nonempty += Lbf > 0
                if not ok:
                    bad += 1; print('MISMATCH n=%d D=%d m=%d t=%d bf=%d genbg=%d enum_conn=%d conn_dfs3=%d classes %d %d %d dupes=%d' % (n, D, m, t, Lbf, Lg, Le, Lc, len(gcls), len(ec), len(cc), len(gl) - len(gcls)))
print('cells compared:', cells, 'nonempty:', nonempty, 'mismatches:', bad)
