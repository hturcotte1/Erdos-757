"""Referee L008 round 3: validate the generators against my labelled brute force (r3_bf) on small cells.
For n in NS and D in (3, 100): brute force counts of connected spanning linear 3-graphs on [n] by (m, tau, maxdeg).
For every (m, t) with brute-force graphs of tau >= t (and t = max+1): compare the labelled count with sum n!/|Aut| over
(i) genbg_r3 classes (TAU0=t), (ii) the authors' enum_conn outputs (classes + |Aut| via r3canon).  Also checks that the
class SETS of (i) and (ii) coincide.  Usage: validate_small.py n_min n_max"""
import subprocess, sys, math, collections, os
R = '/home/user/Erdos-757/experiments/referee/L008-round3'
def run(cmd, env=None, inp=None):
    e = dict(os.environ); e.update(env or {})
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, env=e, input=inp).stdout
def classes(found_text, nv):
    out = run(f'{R}/bin/r3canon FOUND {nv}', inp=found_text)
    d = {}
    for l in out.splitlines():
        c, a = l.split(); d[c] = int(a)
    return d
nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
cells = mism = 0; nonempty = 0
for n in range(nmin, nmax+1):
    for D in (3, 100):
        bf = collections.Counter()
        for l in run(f'nice -n 5 {R}/bin/r3_bf {n} {D}').splitlines():
            nn, m, t, md, c = map(int, l.split()); bf[(m, t)] += c
        ms = sorted({m for m, t in bf})
        for m in range(max(1, (n-1+1)//2), n-1):   # all connected cells, including empty ones
            tmax = max([t for mm, t in bf if mm == m], default=-1)
            for t in range(0, tmax + 2):
                want = sum(c for (mm, tt), c in bf.items() if mm == m and tt >= t)
                Dg = D if D < 100 else m
                g = run(f'nice -n 5 {R}/bin/genbg_r3 -q -c -Z1 -d1:3 -D{Dg}:3 {n} {m} {3*m}:{3*m}', env={'TAU0': str(t)})
                cg = classes(g, n)
                got_g = sum(math.factorial(n)//a for a in cg.values())
                Dc = D if D < 100 else 1000
                e = run(f'nice -n 5 {R}/bin/enum_conn {n} {m} {t} {Dc} 1')
                ce = classes(e, n)
                got_e = sum(math.factorial(n)//a for a in ce.values())
                cells += 1; nonempty += want > 0
                ok = (want == got_g == got_e) and set(cg) == set(ce)
                if not ok:
                    mism += 1; print(f'MISMATCH n={n} D={D} m={m} t={t}: bf={want} genbg={got_g} ({len(cg)} cl) enum_conn={got_e} ({len(ce)} cl)')
        print(f'n={n} D={D}: brute-force total connected spanning linear graphs = {sum(bf.values())}; cells so far {cells}, mismatches {mism}')
print(f'DONE cells={cells} nonempty={nonempty} mismatches={mism}')
