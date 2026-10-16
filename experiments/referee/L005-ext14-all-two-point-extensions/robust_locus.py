"""Route L robustness: recompute D with the maximum Sidon sets in REVERSED order (another S_0 and other seeding sets)
and NT = 1 (candidates seeded by a single S_j); compare whole lines and the full isolated-point set with the default run."""
import json, gzip, os, sys
os.nice(15)
import locus
sets = [json.loads(l)['set'] for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') if l.strip()]
classes = [int(v) for v in sys.argv[1].split(',')]
orig = locus.max_sidon_all
allok = True
for c in classes:
    A = sorted(12 * v for v in sets[c])
    locus.NT = 4; locus.max_sidon_all = orig
    h1, M1, W1, P1 = locus.deficient_locus(A)
    locus.NT = 1
    locus.max_sidon_all = lambda P: (lambda r: (r[0], list(reversed(r[1]))))(orig(P))
    h2, M2, W2, P2 = locus.deficient_locus(A)
    ok = (W1 == W2 and P1 == P2 and M1[0] == M2[-1])
    allok &= ok
    print(c, len(W1), len(P1), ok, flush=True)
print('robust all equal:', allok)
