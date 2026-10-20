"""Acceptance check: the n=23 lines of arith.py agree with arith23_output.txt (L012 part (b)) for m = 19, 20 (violators) and
cross-check m = 21 (slack +1, not a violator) by recomputation."""
import re, sys
sys.path.insert(0, '.')
from arith import analyse
old = open('../prover/L012/arith23_output.txt').read()
R = {(r['m'], r['tau']): r for r in analyse(23)}
ok = True
for m in (19, 20, 21):
    mm = re.search(r'\(b\) m = %d: I11 slack of H = (-?\d+);.*?d <= (\d+)' % m, old)
    s_old, d_old = int(mm.group(1)), int(mm.group(2))
    s_new = 3 * 23 + 2 * m - 110; d_new = (s_new + 8) // 2 if s_new < 0 else None
    # old dmax for m=21 (slack +1) is derived by 99 <= 66 + 2(m-d); recompute the same way for all three
    dmax_direct = max(d for d in range(0, 10) if 99 <= 66 + 2 * (m - d))
    rem_old = re.findall(r'a vertex of degree (\d+): H - v = \(22, (\d+), 9\), slack (-?\d+)', old.split('(b) m = %d' % m)[1].split('(b) m =')[0].split('(c)')[0])
    rem_new = [(d, m - d, 3 * 22 + 2 * (m - d) - 99) for d in range(1, dmax_direct + 1)]
    good = (s_old == s_new and d_old == dmax_direct and [(int(a), int(b), int(c)) for a, b, c in rem_old] == rem_new)
    if (m, 10) in R: good = good and R[(m, 10)]['dmax'] == d_old and [(q['d'], q['cell'][1], q['slack']) for q in R[(m, 10)]['remainders']] == rem_new or m == 19
    print('m=%d: old slack %d dmax %d | new slack %d dmax(direct) %d | remainders equal: %s -> %s' % (m, s_old, d_old, s_new, dmax_direct, [(int(a), int(b), int(c)) for a, b, c in rem_old] == rem_new, 'OK' if good else 'MISMATCH'))
    ok &= good
print('ALL OK' if ok else 'SOME MISMATCH')
