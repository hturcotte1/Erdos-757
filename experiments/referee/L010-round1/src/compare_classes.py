"""Referee L010 r1: compare the isomorphism-class sets of the prover's labelled component lists with genbg's class lists.
Usage: compare_classes.py NV PROVERFILE GENBGFILE   (gz allowed; lines starting with FOUND)"""
import subprocess, sys, gzip, os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin')
def lines(f):
    op = gzip.open if f.endswith('.gz') else open
    return [l for l in op(f, 'rt') if l.startswith('FOUND')]
def classes(ls, nv):
    out = subprocess.run([B + '/canon', 'x', nv], input=''.join(ls), capture_output=True, text=True).stdout.split('\n')
    return [o.split()[0] for o in out if o.strip()]
nv, pf, gf = sys.argv[1:4]
P, G = lines(pf), lines(gf)
cp, cg = classes(P, nv), classes(G, nv)
sp, sg = set(cp), set(cg)
print('%s: prover labelled %d -> %d classes; genbg %d lines -> %d classes; equal=%s; prover-only %d; genbg-only %d'
      % (os.path.basename(pf), len(P), len(sp), len(G), len(sg), sp == sg, len(sp - sg), len(sg - sp)))
