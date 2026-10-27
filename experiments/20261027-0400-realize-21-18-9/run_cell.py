"""usage: run_cell.py cellfile n tag [maxclasses] [seed]   -> results_<tag>.json ; sets_<tag>.json (explicit sets for realizable classes)"""
import sys, re, json, random, time
from rexact import *
from collections import Counter
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
if __name__ == '__main__':
    fn, n, tag = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    mc = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
    lines = [l for l in open(fn) if l.startswith('FOUND:')][:mc]
    res = []; sets = []
    for ci, l in enumerate(lines):
        E = parse(l)
        sols, st = decide(E, n, find_all=True)
        dims = Counter(s[1] for s in sols)
        # exactness of F == E, explicit sets
        ex = []; nF = Counter()
        rnd = random.Random(ci)
        for s in sols[:3]:
            iv = explicit_point(s, n, rnd)
            if iv: ex.append(iv)
        for s in sols:
            pass
        r = dict(cls=ci, n=n, m=len(E), edges=E, realizable=bool(sols), nodes=st['nodes'], realizable_labellings=len(sols),
                 dims_after_affine_norm=dict(dims), prunes=st['prunes'], prune_depth=st['prune_depth'], secs=st['secs'])
        if ex:
            r['example'] = ex[0]
            r['example_checks'] = dict(is_45=is_45_set(ex[0]), num_aps=len(ap_edges(ex[0])))
            sets.append(dict(cls=ci, set=ex[0]))
        res.append(r)
        print(tag, 'class', ci, 'REALIZABLE' if sols else 'NOT-REALIZABLE', 'labellings', len(sols), 'dims', dict(dims), 'nodes', st['nodes'], st['prunes'], st['secs'], 's', flush=True)
    json.dump(res, open(f'results_{tag}.json', 'w'))
    json.dump(sets, open(f'sets_{tag}.json', 'w'))
