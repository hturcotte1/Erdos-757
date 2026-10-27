import json
r = json.load(open('results.json'))
cells = {tuple(map(int, k.split(','))): v for k, v in r.items() if k[0].isdigit()}
print('Table A: per (n,m): classes | Red-free (all Z) | Red_k-free for k=3,4,5,6,8 (no Red pair with |Z|<=k) | slack range of the class')
for n in range(4, 15):
    for m in sorted(mm for (nn, mm) in cells if nn == n):
        v = cells[(n, m)]; rk = v['redk_free']
        print(f'| {n} | {m} | d={n-m} | {v["classes"]} | {v["redfree"]} | {rk["3"]} | {rk["4"]} | {rk["5"]} | {rk["6"]} | {rk["8"]} | {v["slack_min"]}..{v["slack_max"]} |')
print()
print('Table B: by deficiency d=n-m: Red_k-free counts summed over n=4..14 per (d): k=4,5,6')
import collections
for k in ('4', '5', '6'):
    t = collections.defaultdict(lambda: collections.defaultdict(int))
    for (n, m), v in cells.items():
        if n >= 4: t[n-m][n] += v['redk_free'][k]
    print('k=', k)
    for d in sorted(t): print('  d=%d' % d, ' '.join('n%d:%d' % (n, c) for n, c in sorted(t[d].items())))
