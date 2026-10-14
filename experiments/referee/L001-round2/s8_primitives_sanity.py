"""Step 8: sanity of my primitives (is45, brute-force h, ILP h) on known sets: data/small_records.json, Fibonacci sets,
and {1,2,3,5} (not (4,5))."""
import json, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *
d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
for key, s in d['sets'].items():
    pts = s['set']
    pts = [F(str(v)) for v in pts]
    hb = hmax_brute(pts, 1)[0]
    print('n=%d is45=%s h_brute=%d h_ilp=%d recorded=%s' % (len(pts), is45(pts), hb, hmax_ilp(pts),
          (key, s.get('h'))))
fib = [2, 3]
while len(fib) < 16: fib.append(fib[-1] + fib[-2])
for n in (5, 8, 10, 12, 15):
    S = fib[:n]
    print('Fibonacci n=%d is45=%s h_brute=%d h_ilp=%d' % (n, is45(S), hmax_brute(S, 1)[0], hmax_ilp(S)))
print('{1,2,3,5} is45:', is45([1, 2, 3, 5]), '| {2,3,5,8} is45:', is45([2, 3, 5, 8]))
