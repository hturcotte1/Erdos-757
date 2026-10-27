"""L017, illustrative comparison of the structure theorem with the top level of the cell recursion of L013 and L016
(computation C4; Theorem 6 (i), (iii), Step 9.3, Remarks 13.1 and 13.4).  For every top-level violator cell (n, m, tau, D) of L013 (n = 23..26) and L016 (n = 27):
 - its slack s; Theorem 1 + Lemma M say: a violator at size n (with I11 below n) has Delta = 3 and s in {-1, -2};
   so cells with s <= -3 or D <= 2 are empty without computation, and in the cells with D = 3 the engine branch d = 2 is void;
 - for the branch d = 3, tp = tau - 1 (the only one with S' >= 0), S' = s + 2: the engine's decompositions of (n-1, m-3)
   with total slack S' (re-generated here with the engine's own rule, decomp22.slack_cells of L013, imported read-only),
   the number r of components, and the number of inputs (product over component types of multisets of class
   representatives, the class counts read from the stored, refereed cell lists with D = 3);
 - Theorem 4 (iii): r <= 3 for an actual violator; decompositions with r >= 4 are flagged (their inputs cannot extend to a
   violator; the engine processed them and found no hit, as it must).
Usage: python3 engine_decomps.py"""
import sys, os, glob, math, itertools, json, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L013')
from decomp22 import slack_cells
HERE = os.path.dirname(os.path.abspath(__file__))

def load_counts():
    cnt = {}
    for pat in ['out/L012/cells/*.txt', 'out/L013/cells/*.txt', 'out/L014/cells/*.txt', 'out/L016/cells_new/runA/*.txt',
                'out/L016/cells_new/runF/*.txt']:
        for p in glob.glob(os.path.join(HERE, pat)):
            b = os.path.basename(p)[5:-4].split('_'); key = (int(b[0]), int(b[1]), int(b[2]), int(b[3][1:]))
            c = sum(1 for l in open(p) if l.startswith('FOUND:'))
            if not any(l.startswith('INFO ') for l in open(p)): continue
            if key in cnt and cnt[key] != c: raise RuntimeError('inconsistent stored counts for %s' % (key,))
            cnt[key] = c
    return cnt

def pieces(N, S):
    P = [(n, m, t) for (n, m, t, s) in slack_cells(N, S) if t >= 1]
    if S >= 3: P.append((1, 0, 0))
    return P

def decompositions(N, M, S):   # the rule of engine.decompositions (L012/L013/L016 engine.py), re-typed
    P = pieces(N, S); sl = {p: 3 * p[0] + 2 * p[1] - 11 * p[2] for p in P}; sols = []
    def rec(i, n, m, s, ch):
        if n == N and m == M and s == S: sols.append(tuple(ch)); return
        if i == len(P): return
        p = P[i]; k = 0
        while n + k * p[0] <= N and m + k * p[1] <= M and s + k * sl[p] <= S:
            rec(i + 1, n + k * p[0], m + k * p[1], s + k * sl[p], ch + [p] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sols

TOP = [(23, 13, 9, 2), (23, 14, 9, 3), (23, 20, 10, 3), (24, 12, 9, 2), (24, 13, 9, 3), (24, 18, 10, 3), (25, 16, 10, 2),
       (25, 17, 10, 3), (25, 22, 11, 3), (26, 14, 10, 2), (26, 15, 10, 3), (26, 21, 11, 3),          # L013 (top_results.jsonl)
       (27, 13, 10, 2), (27, 18, 11, 2), (27, 14, 10, 3), (27, 19, 11, 3), (27, 25, 12, 3)]          # L016 (five open cells)

if __name__ == '__main__':
    cnt = load_counts(); tot = collections.Counter()
    for (n, m, t, D) in TOP:
        s = 3 * n + 2 * m - 11 * t
        src = 'L013' if n <= 26 else 'L016'
        if D <= 2 or s <= -3:
            why = 'D<=2: Lemma M' if D <= 2 else 's<=-3: Theorem 1 (no degree-3 vertex) + Lemma M'
            print('%s cell %s s=%d: EMPTY by %s (no computation needed)' % (src, (n, m, t, D), s, why)); tot['empty_by_T1M'] += 1
            continue
        dmin = max(1, math.ceil(3 * m / n))
        if dmin <= 2: print('%s cell %s s=%d: engine branch d=2 is void by Lemma M (Delta(X)=2)' % (src, (n, m, t, D), s))
        Sp = s + 2; decs = decompositions(n - 1, m - 3, Sp)
        print('%s cell %s s=%d: branch d=3 tp=%d S\'=%d: %d decompositions of (%d,%d)' % (src, (n, m, t, D), s, t - 1, Sp, len(decs), n - 1, m - 3))
        for dec in decs:
            r = len(dec); g = collections.Counter(dec); size = 1; unknown = False
            for typ, k in g.items():
                key = typ + (3,)
                if typ == (1, 0, 0): c = 1
                elif key in cnt: c = cnt[key]
                else: c = None; unknown = True
                if c is not None: size *= math.comb(c + k - 1, k)
            flag = 'r>=4: void by Theorem 4(iii)' if r >= 4 else ('r<=3' if r <= 3 else '')
            iso = any(typ == (1, 0, 0) for typ in dec)
            print('    r=%d %s inputs=%s %s%s' % (r, list(dec), 'UNKNOWN' if unknown else size, flag, ' ISOLATED VERTEX' if iso else ''))
            tot['decs'] += 1; tot['decs_r%d' % min(r, 4)] += 1
            if not unknown and size > 0: tot['used_r%d' % min(r, 4)] += 1; tot['inputs_r%d' % min(r, 4)] += size
            if iso: tot['isolated'] += 1
    print('TOTALS:', dict(tot))
    # per-cell verdicts: which top-level cells needed an extension computation after Theorem 1, Lemma M and Theorem 4(iii)
    print('VERDICTS (after Theorem 1 + Lemma M + Theorem 4(iii), using the stored class counts):')
    for (n, m, t, D) in TOP:
        s = 3 * n + 2 * m - 11 * t
        if D <= 2 or s <= -3: print('   ', (n, m, t, D), 'empty without computation'); continue
        need = 0
        for dec in decompositions(n - 1, m - 3, s + 2):
            if len(dec) >= 4: continue
            size = 1
            for typ, k in collections.Counter(dec).items():
                c = 1 if typ == (1, 0, 0) else cnt.get(typ + (3,))
                size *= math.comb(c + k - 1, k) if c is not None else 1
            need += size
        print('   ', (n, m, t, D), 'empty given the stored lists (all r<=3 decompositions have 0 inputs)' if need == 0 else
              'needs the extension step: %d inputs from r<=3 decompositions' % need)
    # tight connected cells (slack 0) with n <= 30 and their stored Delta<=3 class counts
    print('TIGHT CONNECTED CELLS (3n+2m = 11 tau, ceil((n-1)/2) <= m <= n-2, tau <= m, 17 tau <= 5n+3m), n <= 30:')
    for n in range(3, 31):
        for m in range((n - 1 + 1) // 2, n - 1):
            if (3 * n + 2 * m) % 11: continue
            t = (3 * n + 2 * m) // 11
            if t > m or 17 * t > 5 * n + 3 * m: continue
            print('    (%d,%d,%d): stored Delta<=3 classes = %s' % (n, m, t, cnt.get((n, m, t, 3), 'not computed')))
    # connected cells with slack 1 and n <= 27 and their stored Delta<=3 class counts
    print('SLACK-1 CONNECTED CELLS (3n+2m-11 tau = 1, same constraints), n <= 27:')
    for n in range(3, 28):
        for m in range((n - 1 + 1) // 2, n - 1):
            if (3 * n + 2 * m - 1) % 11: continue
            t = (3 * n + 2 * m - 1) // 11
            if t > m or 17 * t > 5 * n + 3 * m: continue
            print('    (%d,%d,%d): stored Delta<=3 classes = %s' % (n, m, t, cnt.get((n, m, t, 3), 'not computed')))
    # the violator cells at n = 28..30 with slack -1 or -2 (Theorem 6 (i)) and the decompositions of their d = 3 branch
    print('VIOLATOR CELLS n = 28..30 with s in {-1,-2} (connected, m <= n-2, HY) and their d=3 decompositions:')
    for n in range(28, 31):
        for m in range((n - 1 + 1) // 2, n - 1):
            for s in (-1, -2):
                if (3 * n + 2 * m - s) % 11: continue
                t = (3 * n + 2 * m - s) // 11
                if t > m or 17 * t > 5 * n + 3 * m or 3 * m < n: continue
                decs = decompositions(n - 1, m - 3, s + 2)
                print('    (%d,%d,%d) s=%d: %d decompositions of (%d,%d) with total slack %d, %d of them with r<=3:'
                      % (n, m, t, s, len(decs), n - 1, m - 3, s + 2, sum(1 for d_ in decs if len(d_) <= 3)))
                for dec in decs:
                    if len(dec) > 3: continue
                    cs = [cnt.get(typ + (3,), 'NC') if typ != (1, 0, 0) else 1 for typ in dec]
                    print('        r=%d %s  stored Delta<=3 counts %s' % (len(dec), list(dec), cs))
