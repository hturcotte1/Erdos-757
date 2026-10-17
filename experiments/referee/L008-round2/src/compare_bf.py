"""Referee round 2 (L008): compare bfs_enum against the labelled brute force bf_lab.  For every n<=9, D in {3, inf}, both modes
(CONN=1 connected spanning; CONN=0 all graphs on [n]), every m>=1 and every threshold t = 1..taumax+1: the brute-force number of
labelled graphs with tau >= t must equal sum over bfs_enum's classes of n!/|Aut|."""
import re, subprocess, sys, collections
bf = collections.defaultdict(int)
for fn in sys.argv[1:]:
    for l in open(fn):
        g = re.match(r'(ALL|CON) n=(\d+) D=(\d+) m=(\d+) tau=(\d+) count=(\d+)', l)
        if g: bf[(g.group(1), int(g.group(2)), int(g.group(3)), int(g.group(4)), int(g.group(5)))] += int(g.group(6))
keys = set((k[1], k[2]) for k in bf)
cells = mism = nonempty = 0
for (n, D) in sorted(keys):
    for mode, conn in (('CON', 1), ('ALL', 0)):
        ms = sorted(set(k[3] for k in bf if k[0] == mode and k[1] == n and k[2] == D and k[3] >= 1))
        for m in ms:
            taus = [k[4] for k in bf if k[0] == mode and k[1] == n and k[2] == D and k[3] == m]
            for t in range(1, max(taus) + 2):
                want = sum(v for k, v in bf.items() if k[0] == mode and k[1] == n and k[2] == D and k[3] == m and k[4] >= t)
                out = subprocess.run(['./bin/bfs_enum', str(n), str(m), str(t), str(D), str(conn), '0'], capture_output=True, text=True).stdout
                got = int(re.search(r'labelled=(\d+)', out).group(1))
                cells += 1; nonempty += want > 0
                if got != want: mism += 1; print('MISMATCH', mode, n, D, m, t, want, got)
print('cells compared:', cells, 'non-empty:', nonempty, 'mismatches:', mism)
