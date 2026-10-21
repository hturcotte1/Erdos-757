"""Separate from the referee's verifier: re-run the frozen judge's OWN fast checks on the claim
(everything except the ~69-CPU-minute branch and bound for h), loading the frozen file unmodified (read-only)."""
import importlib.util, json, time, hashlib
from pathlib import Path
p = Path('/home/user/Erdos-757/judge/judge.py')
print('frozen file sha256', hashlib.sha256(p.read_bytes()).hexdigest())
spec = importlib.util.spec_from_file_location('frozen_j', p); J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
cp = Path('/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json')
claim = json.loads(cp.read_text())
t = time.time()
A = J.parse_set(claim['set'])
print('id == stem', claim['id'] == cp.stem, '| type', claim['type'], '| n', len(A), '| in range', 4 <= len(A) <= J.MAX_N)
ok, bad = J.is_45(A); print('frozen is_45', ok, bad, f'({time.time()-t:.1f}s)')
print('frozen is_weak_sidon', J.is_weak_sidon(A))
Wt = J.parse_set(claim['witness_sidon_subset'])
print('frozen witness checks: subset', set(Wt) <= set(A), 'is_sidon', J.is_sidon(Wt), 'size', len(Wt), 'claimed_h', claim['claimed_h'])
r = J.Fraction(claim['claimed_h'], len(A))
print('ratio', r, '< RECORD', r < J.RECORD)
