"""Referee: direct enumeration of one cell by UNMODIFIED nauty genbgL (connected bicoloured graphs, -Z1 = linear, edge class degree 3,
point degree 1..D) piped into the referee's filter (refx filter: linear, connected, maxdeg, F7 embedding, (P3) Hall, tau exactly);
survivors canonicalised by labelg (partition points|edges) and compared, as a set, with the prover's list canonicalised the same way.
Usage: genbg_cell.py n m t D"""
import sys, os, re, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import myengine as E
n, m, t, D = map(int, sys.argv[1:5]); t0 = time.time()
cmd = 'nice -n 10 %s/bin/genbgL -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d | %s/bin/refx filter %d %d %d %d' % (HERE, D, n, m, 3 * m, 3 * m, HERE, n, m, t, D)
out = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.splitlines()
summ = [l for l in out if l.startswith('SUMMARY')][0]
surv = [E.parse_edges(l) for l in out if l.startswith('SURV:')]
mine = sorted(E.canon(n, m, surv)); assert len(set(mine)) == len(mine), 'genbg produced isomorphic duplicates?'
p = os.path.join(E.PROVER, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
prov = [E.parse_edges(l) for l in open(p) if l.startswith('FOUND:')]
pc = sorted(E.canon(n, m, prov))
print('GENBG cell (%d,%d,%d,%d): %s | survivors %d, prover %d, %s, %.1fs' % (n, m, t, D, summ.split(' ', 2)[2], len(mine), len(prov), 'EQUAL' if mine == pc else 'DIFFERENT', time.time() - t0), flush=True)
