"""Step 3: n = 27 record-adjacent cell (27,25,12) Delta<=3: slack-1 decompositions of its remainder (26,22) (d=3, tau'=11, S'=1) via
engine.decompositions (decomp22.slack_cells, unchanged); is [(23,21,10),(3,1,1)] among them?  (23,21,10): slack 3*23+2*21-110 = 1 (connected, Delta<=3
is the open degree-3 record cell of kb/open_questions.md Q14); (3,1,1): slack 0.  Component cell types needed at degree bound D=3."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells_dummy'))
sys.path.insert(0, HERE)
import engine
seeded = set(open(os.path.join(HERE, 'seed_cells.txt')).read().split())
def sl(c): return 3 * c[0] + 2 * c[1] - 11 * c[2]
n, m, t, d, tp = 27, 25, 12, 3, 11
N, M = n - 1, m - d; S = 3 * N + 2 * M - 11 * tp
print('cell (27,25,12) Delta<=3, slack %d; max degree d=3 (forced: ceil(3m/n)=3), tau\'=%d, remainder (%d,%d) slack S\'=%d' % (3*27+2*25-11*12, tp, N, M, S))
# the other tau' branch
print('tau\'=12 branch: S\' = %d (<0, impossible); d<3: ceil(3m/n)=%d so d>=3' % (3 * N + 2 * M - 11 * 12, -(-3 * m // n)))
decs = engine.decompositions(N, M, S)
print('%d decompositions of (%d,%d) with slack %d:' % (len(decs), N, M, S))
types = set()
for dec in decs:
    print('   ', ' + '.join('%dx(%d,%d,%d)[slack %d]' % (dec.count(c), *c, sl(c)) for c in sorted(set(dec))))
    types |= set(c for c in dec if c != (1, 0, 0))
target = ((3, 1, 1), (23, 21, 10))
has = any(sorted(dec) == sorted(target) for dec in decs)
print('Is [(23,21,10),(3,1,1)] a decomposition of (26,22) slack 1?  %s' % ('YES' if has else 'NO'))
print('slack of (23,21,10) = %d, (3,1,1) = %d; n 23+3 = 26, m 21+1 = 22' % (sl((23, 21, 10)), sl((3, 1, 1))))
print('component cell types (n_i,m_i,tau_i) needed at D=3 and cell-file status in the seeded out/cells:')
for c in sorted(types):
    f = 'cell_%d_%d_%d_D3.txt' % c
    print('   %s  slack %d  %s' % (c, sl(c), 'seeded' if f in seeded else 'NOT computed (new)'))

# engine branch sizes for the two new connected cells that would be needed (arithmetic only)
import math
for (cn, cm, ct) in ((23, 21, 10), (26, 22, 11)):
    print('engine branches for cell (%d,%d,%d) Delta<=3 (slack %d):' % (cn, cm, ct, sl((cn, cm, ct))))
    for dd in range(max(1, math.ceil(3 * cm / cn)), 4):
        for tq in (ct - 1, ct):
            Sp = 3 * (cn - 1) + 2 * (cm - dd) - 11 * tq
            if Sp < 0: continue
            dc = engine.decompositions(cn - 1, cm - dd, Sp)
            print('   d=%d tau\'=%d remainder (%d,%d) S\'=%d: %d decompositions' % (dd, tq, cn - 1, cm - dd, Sp, len(dc)))
