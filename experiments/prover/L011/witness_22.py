"""(L011) An explicit 22-point (4,5)-set with h = 13 (so f(22) <= 13), checked from the definitions.  Construction (the gluing idea of
Ma-Tang Lemma 3.6 with explicit numbers): the 12-point set B12 (h = 7) and the 10-point set B10 (h = 6) of data/small_records.json,
the second one scaled by q and translated by T = 5000; the first q >= 2 found by a small search that makes the union a (4,5)-set is
used.  h <= 7 + 6 = 13 is then verified directly (no Sidon 14-subset among all C(22,14) subsets), and a Sidon 13-subset is exhibited."""
import itertools, json, sys
def nd(q): return len({abs(a - b) for a, b in itertools.combinations(q, 2)})
def is45(A): return all(nd(q) >= 5 for q in itertools.combinations(A, 4))
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
B12 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
B10 = [0, 50, 73, 80, 87, 96, 100, 112, 127, 174]
assert is45(B12) and is45(B10)
T = 5000
found = None
for q in range(2, 1000):
    C = sorted(B12 + [T + q * b for b in B10])
    if len(set(C)) == 22 and is45(C): found = (q, C); break
q, C = found
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
S13 = next((S for S in itertools.combinations(C, 13) if sidon(S)), None)
n14 = sum(1 for S in itertools.combinations(C, 14) if sidon(S))
print('q =', q); print('C =', C)
print('(4,5):', is45(C), '(%d four-subsets) | APs:' % (len(list(itertools.combinations(C, 4)))), len(aps),
      '| a Sidon 13-subset:', S13, '| Sidon 14-subsets among %d:' % len(list(itertools.combinations(C, 14))), n14)
sys.path.insert(0, '/home/user/Erdos-757'); from e757.core import alpha, ap_edges, is_45_set
print('e757.core: is_45_set =', is_45_set(C), 'm =', len(ap_edges(C)), 'h =', alpha(C))
json.dump(dict(set=C, n=22, m=len(aps), h=13 if (S13 and n14 == 0) else None, q=q, T=T, sidon13=list(S13)), open('witness_22.json', 'w'))
