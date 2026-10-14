"""Raw (not reflection-deduplicated) census counts from the deduplicated classification: each
non-symmetric class counts twice, a reflection-symmetric one once; the empty pattern is classified too."""
import sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from census8 import patterns, classify
from recompute import reflect
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
t0 = time.time()
pats = patterns(N)
seen = {}
for p in pats:
    c = min(p, reflect(N, p))
    seen.setdefault(c, 0)
    seen[c] += 1
cnt = Counter(); cnt_dedup = Counter()
for c, mult in seen.items():
    v = classify(N, c) if c else "R(empty)"
    cnt[v] += mult; cnt_dedup[v] += 1
print(f"n={N}: raw {len(pats)} = sum of multiplicities {sum(seen.values())}; classes up to reflection {len(seen)}")
print(f"RAW   counts: {dict(cnt)}  (R total incl. empty = {cnt['R'] + cnt['R(empty)']})")
print(f"DEDUP counts: {dict(cnt_dedup)}   {time.time()-t0:.0f}s")
