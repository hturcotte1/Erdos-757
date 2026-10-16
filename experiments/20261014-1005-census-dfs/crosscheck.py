"""Every CP-SAT solution (experiments/20261014-0610-extremal-census) must appear in the DFS output (up to reflection)."""
import gzip, json
N=12
def canon(edges):
    t = tuple(sorted(tuple(e) for e in edges))
    r = tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in t))
    return min(t, r)
cp = set()
raw = 0
for line in open('../20261014-0610-extremal-census/results/n12_m10_solutions.jsonl'):
    raw += 1; cp.add(canon(json.loads(line)))
found = set()
for line in gzip.open('results/n12_m10_all.jsonl.gz', 'rt'):
    c = canon(json.loads(line))
    if c in cp: found.add(c)
missing = cp - found
print(json.dumps({"cpsat_raw_lines": raw, "cpsat_canonical": len(cp), "found_in_dfs": len(found), "missing": len(missing)}))
if missing: print(sorted(missing)[:3])
json.dump({"cpsat_raw_lines": raw, "cpsat_canonical": len(cp), "found_in_dfs": len(found), "missing": len(missing)}, open('results/crosscheck.json','w'))
