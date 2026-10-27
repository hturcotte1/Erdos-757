"""decomp_check.py -- referee's independent recomputation of the cell bookkeeping of L018 Corollary 7.2 and Remark 7.3.

Cells (n, m, tau) of connected members of C: ceil((n-1)/2) <= m <= n-2, tau >= 1, Henning-Yeo 17 tau <= 5n + 3m.
Violator cells at n = 28, 29: slack = 3n + 2m - 11 tau < 0.  For slack in {-1, -2} (Theorem 6(a)), a degree-3 vertex w
gives X - w of type (n-1, m-3, tau-1) with slack(X) + 2, no isolated vertex, at most 2 components (Theorem 6(b')),
each a cell as above with slack >= 0.  We list all decompositions into 1 or 2 parts and report, for each part, the
number of FOUND lines in the stored lists (L013 cells.tar.gz; L016 cells_new; the unrefereed directories).
"""
import sys, os, glob, re, tarfile, io

ROOT = '/home/user/Erdos-757'


def cells(n):
    out = []
    for m in range((n - 1 + 1) // 2, n - 1):
        for t in range(1, n + 1):
            if 17 * t <= 5 * n + 3 * m:
                out.append((n, m, t, 3 * n + 2 * m - 11 * t))
    return out


def slack(n, m, t):
    return 3 * n + 2 * m - 11 * t


def decomps(n, m, t, s):
    res = []
    # one part
    if (n - 1 + 1) // 2 <= m <= n - 2 and 17 * t <= 5 * n + 3 * m and slack(n, m, t) == s and s >= 0:
        res.append(((n, m, t),))
    for n1 in range(3, n - 2):
        n2 = n - n1
        if n2 < n1:
            continue
        for m1 in range((n1 - 1 + 1) // 2, n1 - 1):
            m2 = m - m1
            if not ((n2 - 1 + 1) // 2 <= m2 <= n2 - 2):
                continue
            for t1 in range(1, n1 + 1):
                t2 = t - t1
                if t2 < 1:
                    continue
                if 17 * t1 > 5 * n1 + 3 * m1 or 17 * t2 > 5 * n2 + 3 * m2:
                    continue
                s1 = slack(n1, m1, t1); s2 = slack(n2, m2, t2)
                if s1 < 0 or s2 < 0 or s1 + s2 != s:
                    continue
                a, b = (n1, m1, t1), (n2, m2, t2)
                key = tuple(sorted([a, b]))
                if key not in [tuple(sorted(r)) for r in res]:
                    res.append(key)
    return res


def load_counts():
    counts = {}
    # L013 lists (refereed)
    with tarfile.open(os.path.join(ROOT, 'experiments/prover/L013/cells.tar.gz')) as tf:
        for mem in tf.getmembers():
            mm = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d)\.txt$', mem.name)
            if mm and mem.isfile():
                data = tf.extractfile(mem).read().decode()
                c = sum(1 for l in data.splitlines() if l.startswith('FOUND'))
                counts[('L013',) + tuple(int(x) for x in mm.groups())] = c
    return counts


def main():
    counts = load_counts()
    for n in (28, 29):
        print('=== n = %d ===' % n)
        viol = [(nn, m, t, s) for (nn, m, t, s) in cells(n) if s < 0]
        print('violator cells (slack < 0, HY, m in range):', [(c[:3], c[3]) for c in viol])
        for (nn, m, t, s) in viol:
            if s < -2:
                continue
            print(' cell (%d,%d,%d) slack %d: X - w = (%d,%d,%d) slack %d' % (n, m, t, s, n - 1, m - 3, t - 1, s + 2))
            for d in decomps(n - 1, m - 3, t - 1, s + 2):
                parts = []
                for (a, b, c) in d:
                    k = ('L013', a, b, c, 3)
                    parts.append('(%d,%d,%d)[L013 D3: %s]' % (a, b, c, counts.get(k, 'n/a')))
                print('    ', ' + '.join(parts))


if __name__ == '__main__':
    main()
