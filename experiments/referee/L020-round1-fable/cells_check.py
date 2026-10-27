"""Referee check of Step 4.3 of L020: the connected cells (n,m,tau) with slack 0 or 1, n <= 26, and the stored
Delta<=3 lists for them in the refereed archives (L012, L013, L014, L016).  Also recomputes, with own code, tau and
max degree of every stored graph in the slack<=1 cells, and counts the Delta<=3 classes (expected total 483)."""
import sys, tarfile, io, os, re, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R

ARCH = ['/home/user/Erdos-757/experiments/prover/L012/cells.tar.gz',
        '/home/user/Erdos-757/experiments/prover/L013/cells.tar.gz',
        '/home/user/Erdos-757/experiments/prover/L014/cells.tar.gz',
        '/home/user/Erdos-757/experiments/prover/L016/cells_new.tar.gz']
L016DIR = '/home/user/Erdos-757/experiments/prover/L016/'

def cells(maxn, slacks):
    out = []
    for n in range(3, maxn + 1):
        for m in range((n - 1 + 1) // 2, n - 1):  # ceil((n-1)/2) <= m <= n-2
            for s in slacks:
                if (3 * n + 2 * m - s) % 11 == 0:
                    t = (3 * n + 2 * m - s) // 11
                    if 1 <= t <= m:
                        out.append((n, m, t, s))
    return out

def main():
    files = {}  # name -> (source, content)
    for a in ARCH:
        if not os.path.exists(a):
            print('missing archive', a); continue
        with tarfile.open(a) as tf:
            for mem in tf.getmembers():
                if mem.isfile() and 'cell_' in mem.name:
                    base = os.path.basename(mem.name)
                    files.setdefault(base, []).append((a.split('/')[-2] + ':' + mem.name, tf.extractfile(mem).read().decode()))
    for fn in os.listdir(L016DIR):
        if fn.startswith('cell_') and fn.endswith('.txt'):
            files.setdefault(fn, []).append(('L016dir', open(L016DIR + fn).read()))
    print('stored cell files found:', len(files))
    total_d3 = 0
    for (n, m, t, s) in cells(26, [0, 1]):
        found = []
        for D in (3, 4, 5, 6):
            key = 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D)
            if key in files:
                for src, content in files[key]:
                    lines = [l for l in content.split('\n') if l.startswith('FOUND')]
                    # own recount of Delta<=3 classes, tau and connectivity
                    cnt3 = 0; bad = 0
                    for l in lines:
                        toks = l.split()
                        E = [tuple(int(x) for x in g.strip('()').split(',')) for g in toks[1:]]
                        deg = R.degrees(n, E)
                        if max(deg) <= 3:
                            cnt3 += 1
                            if len(E) != m or not R.connected(n, E) or R.tau(n, E) != t:
                                bad += 1
                    found.append((D, src, len(lines), cnt3, bad))
        d3counts = sorted(set(f[3] for f in found)) if found else None
        if found and len(d3counts) == 1:
            total_d3 += d3counts[0]
        print('cell (%d,%d,%d) slack %d: ' % (n, m, t, s), 'NO STORED LIST' if not found else
              '; '.join('D%d %s: %d lines, %d with Delta<=3, %d inconsistent' % f for f in found), flush=True)
    print('total Delta<=3 classes over slack<=1 cells with stored lists (one count per cell):', total_d3)

if __name__ == '__main__':
    main()
