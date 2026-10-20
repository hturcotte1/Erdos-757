"""(L013, prover) Validation of the final extension steps at the sizes of this certificate (NG = 22..25).
For each listed top-level branch (cell, d, t'): the inputs are rebuilt from the cell files exactly as engine.recurse builds them
(decompositions by decomp_bf, multisets of representatives on consecutive vertex blocks);
 (i)  bin/ext_d NG t' t d d-1 noprune (no F7 pruning, no (P3) test) is run on all inputs, and every extension it prints is tested with
      the pure-Python verifier of check_cells.py: the number of those that are connected members of C with tau = t must be 0;
 (ii) on a seeded sample of inputs (up to SAMPLE inputs that have at least one extension and up to SAMPLE that have none), the set of extensions printed by `ext_d ... noprune` for that input is compared with an independent
      brute force: all d-sets of pairwise disjoint admissible pairs (not inside an edge of G, endpoints of G-degree <= d-1), kept iff
      tau(G + new vertex) >= t, decided with the minimum covers of G computed by a separate Python branching (L012 3.5 criterion: a cover of
      size t-1 of the extension cannot contain the new vertex).
Usage: python3 ext_validate.py CELLDIR SAMPLE SEED n m t D d tp [n m t D d tp ...]"""
import sys, os, itertools, subprocess, random, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from check_cells import verify, parse_edges
from decomp_bf import bf_decomps
cd = sys.argv[1]; sample = int(sys.argv[2]); rng = random.Random(int(sys.argv[3])); a = list(map(int, sys.argv[4:]))
def reps(key):
    n, m, t, D = key
    if (n, m) == (1, 0): return [[]]
    fn = os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(fn): return []
    return [parse_edges(l) for l in open(fn) if l.startswith('FOUND:')]
def inputs_for(n, m, t, D, d, tp):
    Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp; out = []
    for dec in sorted(bf_decomps(n - 1, m - d, Sp)):
        groups = {}
        for c in dec: groups[c] = groups.get(c, 0) + 1
        gl = [(typ, reps((typ[0], typ[1], typ[2], d)), k) for typ, k in sorted(groups.items())]
        for combo in itertools.product(*[list(itertools.combinations_with_replacement(range(len(cl)), k)) for typ, cl, k in gl]):
            es = []; off = 0
            for (typ, cl, k), idxs in zip(gl, combo):
                for i in idxs: es += [tuple(v + off for v in e) for e in cl[i]]; off += typ[0]
            out.append(es)
    return out
def min_covers(E, NG):
    """all minimum vertex covers of the 3-graph E on 0..NG-1 (Python branching, independent of ext_d's Gosper enumeration)."""
    def covers_le(k, rem, chosen, acc):
        if not rem: acc.add(frozenset(chosen)); return
        if k == 0: return
        for v in rem[0]: covers_le(k - 1, [f for f in rem if v not in f], chosen | {v}, acc)
    k = 0
    while True:
        acc = set(); covers_le(k, [set(e) for e in E], frozenset(), acc)
        acc = set(c for c in acc if len(c) == k)
        if acc: return k, acc
        k += 1
def brute(E, NG, t, d):
    deg = [0] * NG; inside = set()
    for e in E:
        for v in e: deg[v] += 1
        for x, y in itertools.combinations(sorted(e), 2): inside.add((x, y))
    pairs = [(x, y) for x, y in itertools.combinations(range(NG), 2) if (x, y) not in inside and deg[x] <= d - 1 and deg[y] <= d - 1]
    tg, covs = min_covers(E, NG); covs = list(covs); hits = set()
    if tg < t - 1: return tg, hits
    for S in itertools.combinations(pairs, d):
        vs = [v for p in S for v in p]
        if len(set(vs)) != 2 * d: continue
        if tg >= t or all(any(not (set(p) & c) for p in S) for c in covs): hits.add(frozenset(S))
    return tg, hits
res = []
for i in range(0, len(a), 6):
    n, m, t, D, d, tp = a[i:i + 6]; NG = n - 1; ins = inputs_for(n, m, t, D, d, tp)
    lines = ['%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) for es in ins]
    out = subprocess.run([os.path.join(HERE, 'bin', 'ext_d'), str(NG), str(tp), str(t), str(d), str(d - 1), 'noprune'],
                         input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines() if lines else ['SUMMARY none']
    hits = [parse_edges(l) for l in out if l.startswith('HIT:')]; summ = [l for l in out if l.startswith('SUMMARY')][0]
    surv = sum(1 for h in hits if verify(h, n, m, t, D) is None)
    why = {}
    for h in hits:
        r = verify(h, n, m, t, D) or 'IN_C'; why[r] = why.get(r, 0) + 1
    # sample: up to SAMPLE inputs among those with at least one noprune extension and up to SAMPLE among those without
    key_of = {frozenset(map(tuple, map(sorted, es))): j for j, es in enumerate(ins)}
    with_hits = sorted(set(key_of.get(frozenset(tuple(sorted(e)) for e in h if NG not in e), -1) for h in hits) - {-1})
    without = sorted(set(range(len(ins))) - set(with_hits))
    samp = rng.sample(with_hits, min(sample, len(with_hits))) + rng.sample(without, min(sample, len(without))); agree = 0; bfh = 0
    for j in samp:
        o = subprocess.run([os.path.join(HERE, 'bin', 'ext_d'), str(NG), str(tp), str(t), str(d), str(d - 1), 'noprune'],
                           input=lines[j] + '\n', capture_output=True, text=True).stdout.splitlines()
        eh = set(frozenset(tuple(sorted(v for v in e if v != NG)) for e in parse_edges(l) if NG in e) for l in o if l.startswith('HIT:'))
        tg, bh = brute(ins[j], NG, t, d); bfh += len(bh); agree += (eh == bh)
    r = dict(branch=[n, m, t, D, d, tp], inputs=len(ins), ext_d_noprune=summ, noprune_hits=len(hits), verdicts=why, connected_in_C_tau_t=surv,
             sampled_inputs=len(samp), sampled_with_hits=min(sample, len(with_hits)), inputs_with_hits=len(with_hits), brute_force_hits_on_sample=bfh, sample_inputs_identical=agree)
    print(json.dumps(r), flush=True); res.append(r)
json.dump(res, open(os.path.join(HERE, os.environ.get('EXTVAL_JSON', 'ext_validate_output.json')), 'w'), indent=1)
