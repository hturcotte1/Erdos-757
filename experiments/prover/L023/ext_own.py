"""(L023) Own implementation of the extension step (independent of ext_d: no code shared), compared input by input with the
HIT lines of `ext_d (n-1) t' t d (d-1) noprune`.
For an input G on vertices 0..NG-1 with tau(G) = TP (checked: no (TP-1)-cover), it lists every set of d pairwise disjoint pairs
{a_i,b_i} with (i) {a_i,b_i} inside no edge of G, (ii) deg_G(a_i), deg_G(b_i) <= d-1, such that every TP-cover of G misses some pair,
i.e. (L012 3.5) the extension G + {NG,a_i,b_i} (i = 1..d) has tau >= TP+1.  Method: all TP-covers by branching on the first uncovered
edge (with the vertices of earlier branches forbidden, so every cover is produced once); bitsets over covers; depth-first search that
branches, at each node, on the admissible unused pairs that kill the first surviving cover; when no cover survives, the remaining pairs are
chosen freely; the sets are collected in a Python set (duplicates removed).
usage: python3 ext_own.py INPUTS NOPRUNE_OUT NG TP d [first:last] [INDEXFILE]"""
import sys, itertools, time
def covers(E, NG, k):
    out = []
    masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in E]
    def rec(S, budget, forb):
        for mk in masks:
            if not mk & S: break
        else:
            out.append(S); return True
        if budget == 0: return False
        f = forb
        for v in range(NG):
            if (mk >> v) & 1 and not (f >> v) & 1:
                rec(S | (1 << v), budget - 1, f)
                f |= 1 << v
        return False
    rec(0, k, 0)
    return out
def has_cover(E, NG, k):
    masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in E]
    def rec(S, budget):
        for mk in masks:
            if not mk & S: break
        else: return True
        if budget == 0: return False
        return any(rec(S | (1 << v), budget - 1) for v in range(NG) if (mk >> v) & 1)
    return rec(0, k)
def ext_sets(E, NG, TP, d):
    assert not has_cover(E, NG, TP - 1), 'tau(G) < TP'
    C = covers(E, NG, TP); assert C, 'tau(G) > TP'
    C = [S for S in C if bin(S).count('1') == TP]
    K = len(C); ALL = (1 << K) - 1
    deg = [0] * NG
    inside = set()
    for e in E:
        for v in e: deg[v] += 1
        for p in itertools.combinations(sorted(e), 2): inside.add(p)
    B = [0] * NG
    for i, S in enumerate(C):
        for v in range(NG):
            if (S >> v) & 1: B[v] |= 1 << i
    pairs = [(a, b) for a, b in itertools.combinations(range(NG), 2) if deg[a] <= d - 1 and deg[b] <= d - 1 and (a, b) not in inside]
    kill = {p: ALL & ~(B[p[0]] | B[p[1]]) for p in pairs}
    res = set(); killers = {}
    def free(chosen, used, k, start_pairs):
        if k == 0: res.add(frozenset(chosen)); return
        for i, p in enumerate(start_pairs):
            if not (used >> p[0]) & 1 and not (used >> p[1]) & 1:
                free(chosen + [p], used | (1 << p[0]) | (1 << p[1]), k - 1, start_pairs[i + 1:])
    def rec(chosen, used, R):
        if R == 0:
            free(chosen, used, d - len(chosen), pairs); return
        if len(chosen) == d: return
        low = R & -R; i0 = low.bit_length() - 1
        kp = killers.get(i0)
        if kp is None:
            S0 = C[i0]; kp = killers[i0] = [p for p in pairs if not (S0 >> p[0]) & 1 and not (S0 >> p[1]) & 1]
        for p in kp:
            a, b = p
            if (used >> a) & 1 or (used >> b) & 1: continue
            rec(chosen + [p], used | (1 << a) | (1 << b), R & ~kill[p])
    rec([], 0, ALL)
    return res, K, len(pairs)
if __name__ == '__main__':
    fin, fout, NG, TP, d = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    import os; VERBOSE = os.environ.get('VERBOSE') == '1'
    lines = [l.split() for l in open(fin) if l.strip()]
    rng = sys.argv[6] if len(sys.argv) > 6 else '0:%d' % len(lines)
    lo, hi = map(int, rng.split(':'))
    inputs = []
    for p in lines:
        m = int(p[0]); v = list(map(int, p[1:])); inputs.append(tuple(tuple(v[3 * i:3 * i + 3]) for i in range(m)))
    index = {E: i for i, E in enumerate(inputs)}
    hits = {}
    import re
    for l in open(fout):
        if not l.startswith('HIT'): continue
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
        g = tuple(e for e in es if NG not in e); new = frozenset(tuple(sorted(x for x in e if x != NG)) for e in es if NG in e)
        hits.setdefault(index[g], set()).add(new)
    eq = df = tot = 0; t0 = time.time(); maxK = 0
    sel = range(lo, min(hi, len(inputs)))
    if len(sys.argv) > 7: sel = [int(x) for x in open(sys.argv[7]).read().split()]
    for i in sel:
        mine, K, P = ext_sets(list(inputs[i]), NG, TP, d); maxK = max(maxK, K)
        theirs = hits.get(i, set())
        if mine == theirs: eq += 1
        else: df += 1; print('DIFFERENT input', i, 'mine', len(mine), 'ext_d', len(theirs), flush=True)
        if VERBOSE: print('INPUT %d covers %d pairs %d extensions %d %s' % (i, K, P, len(mine), 'EQUAL' if mine == theirs else 'DIFFERENT'), flush=True)
        tot += len(mine)
    print('SUMMARY compared %d equal %d different %d extensions(own) %d max_covers %d secs %.1f' % (eq + df, eq, df, tot, maxK, time.time() - t0))
