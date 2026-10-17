"""An explicit 16-point (4,5)-set with h = 10 (so f(16) <= 10), checked from the definitions.
Construction: A_base plus the point -323 (a (4,5) one-point extension, cf. L007 Step 7) plus one far point y; the first y >= 5000
for which the 16-point set is a (4,5)-set is taken."""
import itertools, sys, json
def nd(q): return len({abs(a - b) for a, b in itertools.combinations(q, 2)})
def is45(A): return all(nd(q) >= 5 for q in itertools.combinations(A, 4))
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B15 = sorted(AB + [-323])
print('A_base + {-323}: (4,5) =', is45(B15))
y = 5000
while not is45(sorted(B15 + [y])): y += 1
C = sorted(B15 + [y])
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
has10 = any(sidon(S) for S in itertools.combinations(C, 10))
has11 = any(sidon(S) for S in itertools.combinations(C, 11))
print('C =', C); print('(4,5):', is45(C), '| APs:', len(aps), '| Sidon 10-subset exists:', has10, '| Sidon 11-subset exists:', has11)
sys.path.insert(0, '/home/user/Erdos-757'); from e757.core import alpha, ap_edges
print('e757.core: m =', len(ap_edges(C)), 'h =', alpha(C))
json.dump(dict(set=C, n=len(C), m=len(aps), h=10 if has10 and not has11 else None), open('witness_16.json', 'w'))
