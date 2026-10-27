"""(L023) Soundness audit (own verifier) of stored unrefereed lists: every class (or a seeded sample) is checked from the definitions:
labels 0..n-1, m distinct triples, linear, F7-free, (P3), connected, tau = t exactly, Delta <= D.  (Soundness is not needed for
Theorem 2, which uses only completeness; the audit checks that the stored files are what they claim to be.)
usage: python3 audit_lists.py CELLFILE n m t D [sample] [seed]"""
import sys, re, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from verify_c import in_C, connected, tau_exact, degrees
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
fn = sys.argv[1]; n, m, t, D = map(int, sys.argv[2:6]); k = int(sys.argv[6]) if len(sys.argv) > 6 else 0; seed = int(sys.argv[7]) if len(sys.argv) > 7 else 23
G = [parse(l) for l in open(fn) if l.startswith('FOUND:')]
idx = list(range(len(G)))
if k and k < len(G): idx = sorted(random.Random(seed).sample(idx, k))
bad = 0
for i in idx:
    E = G[i]
    ok = len(E) == m and len(set(map(frozenset, E))) == m and in_C(E, n)[0] and connected(E, n) and max(degrees(E, n)) <= D and tau_exact(E, n)[0] == t
    if not ok: bad += 1; print('PROBLEM class', i)
print('AUDIT %s: classes %d checked %d problems %d' % (fn.split('/')[-1], len(G), len(idx), bad))
