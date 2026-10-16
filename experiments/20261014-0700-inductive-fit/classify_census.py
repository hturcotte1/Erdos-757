"""Full core library classification of every census hypergraph (fastcores.has_core, validated against constraint_violations)."""
import sys, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/falsify/q8-abstract')
from fastcores import has_core
from multiprocessing import Pool
rows = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
import random
random.seed(7570)
SAMPLE = sorted(set(random.sample(range(len(rows)), 6000)) | set(random.Random(757).sample(range(len(rows)), 500)))
def f(i): return has_core(12, rows[i])
if __name__ == '__main__':
    t = time.time()
    with Pool(2) as p: out = p.map(f, SAMPLE, chunksize=50)
    json.dump(dict(zip(map(str, SAMPLE), out)), open('census_has_core.json', 'w'))
    print(len(SAMPLE), 'sampled; time', round(time.time() - t), 'pass(no core)', sum(1 for o in out if not o), flush=True)
