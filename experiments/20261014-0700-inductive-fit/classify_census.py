"""Full core library classification of every census hypergraph (fastcores.has_core, validated against constraint_violations)."""
import sys, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/q8-abstract')
from fastcores import has_core
from multiprocessing import Pool
rows = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
def f(i): return has_core(12, rows[i])
if __name__ == '__main__':
    t = time.time()
    with Pool(2) as p: out = p.map(f, range(len(rows)), chunksize=100)
    json.dump(out, open('census_has_core.json', 'w'))
    print(len(rows), 'time', round(time.time() - t), 'pass(no core)', sum(1 for o in out if not o), flush=True)
