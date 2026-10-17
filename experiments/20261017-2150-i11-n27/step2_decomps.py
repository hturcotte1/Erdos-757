"""Step 2/3: slack decompositions the engine would use for the open cells (n=26 and n=27), with component cell types (n_i,m_i,tau_i) and
whether each (n_i,m_i,tau_i,d) cell file exists in the seeded out/cells (from the 1645 run).  Arithmetic only (no engine run).
Usage: python3 step2_decomps.py N   (N = 26 or 27).  Uses engine.decompositions (decomp22.slack_cells) unchanged."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells_dummy'))
sys.path.insert(0, HERE)
import engine
from arith import analyse
CELLS = os.path.join(HERE, 'out', 'cells_seed')
SEED = os.path.join(HERE, 'seed_cells.txt')   # list of seeded cell file names
seeded = set(open(SEED).read().split())
def valid(n, m, t, D):
    return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
N = int(sys.argv[1]); out = {}
for r in analyse(N):
    if not r['status'].startswith('OPEN'): continue
    n, m, t, D = r['n'], r['m'], r['tau'], r['dmax']; need = set(); branches = []
    print('=== cell (%d,%d,%d) Delta<=%d  (slack %d)' % (n, m, t, D, r['slack']))
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp)
            print('  branch d=%d tau\'=%d remainder (%d,%d) slack S\'=%d: %d decompositions' % (d, tp, n - 1, m - d, Sp, len(decs)))
            for dec in decs:
                parts = [c for c in dec]
                desc = []
                for c in sorted(set(parts)):
                    k = parts.count(c)
                    if c == (1, 0, 0): desc.append('%dx isolated' % k); continue
                    f = 'cell_%d_%d_%d_D%d.txt' % (c[0], c[1], c[2], d)
                    ok = valid(c[0], c[1], c[2], d)
                    st = 'guard-empty' if not ok else ('seeded' if f in seeded else 'NEW')
                    if ok: need.add((c[0], c[1], c[2], d))
                    desc.append('%dx(%d,%d,%d)[%s]' % (k, c[0], c[1], c[2], st))
                print('     ', ' + '.join(desc))
            branches.append(dict(d=d, tp=tp, Sp=Sp, decompositions=len(decs), decs=[list(map(list, dd)) for dd in decs]))
    new = sorted(c for c in need if 'cell_%d_%d_%d_D%d.txt' % c not in seeded)
    print('  distinct nonguard-empty component cells: %d; seeded: %d; NEW: %d' % (len(need), len(need) - len(new), len(new)))
    print('  NEW (n,m,tau,D) at top level:', new)
    out['%d_%d_%d_D%d' % (n, m, t, D)] = dict(branches=[{k: v for k, v in b.items() if k != 'decs'} for b in branches], needed=sorted(need), new=new)
json.dump(out, open('step2_n%d_cells.json' % N, 'w'), indent=1)
