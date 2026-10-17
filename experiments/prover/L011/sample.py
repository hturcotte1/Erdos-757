"""(L011) Random sample of input lines (seeded): sample.py OUT SEED SRC1:K1 [SRC2:K2 ...] (K lines from each source, without replacement)."""
import random, sys
out, seed = sys.argv[1], int(sys.argv[2]); random.seed(seed); res = []
for spec in sys.argv[3:]:
    f, k = spec.rsplit(':', 1); L = open(f).read().splitlines(); res += random.sample(L, min(int(k), len(L)))
open(out, 'w').write('\n'.join(res) + '\n'); print(out, len(res))
