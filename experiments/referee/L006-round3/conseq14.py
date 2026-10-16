"""Consistency check of the L006 Consequence on the available extremal 14-point data (the 2,910 saturated classes of L004):
every 12-point subset of an extremal 14-point (4,5)-set has h = 8 (no extremal 12-point subset). Own code, Sidon definition only."""
import gzip, json, itertools, time
def is_sidon(S):
    seen = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True
def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})
t0 = time.time()
rows = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
print('classes', len(rows), 'keys', sorted(rows[0].keys()))
bad = 0; worst = 99; n_pairs = 0
for r in rows:
    C = sorted(r['set'] if 'set' in r else r['A'])
    assert len(C) == 14 and all(nd(q) >= 5 for q in itertools.combinations(C, 4))
    S8 = [S for S in itertools.combinations(C, 8) if is_sidon(S)]
    assert S8 and not any(is_sidon(S) for S in itertools.combinations(C, 9))   # h(C) = 8
    for u, v in itertools.combinations(C, 2):
        n_pairs += 1
        if not any(u not in S and v not in S for S in S8): bad += 1
print('14-point classes', len(rows), 'pairs', n_pairs, '12-subsets with h<8 (would be extremal 12-point subsets):', bad, 'secs', round(time.time() - t0, 1))
