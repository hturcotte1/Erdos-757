"""Count injective midpoint labellings (SDRs: lambda(e) in e, lambda injective) of each graph of a cell list."""
import sys, re, time
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def count(E, n):
    m = len(E)
    # order edges: BFS-ish (max overlap with covered)
    order = []; rem = list(range(m)); cov = set()
    while rem:
        b = max(rem, key=lambda i: (len(cov & set(E[i])), -i)); order.append(b); rem.remove(b); cov |= set(E[b])
    E2 = [E[i] for i in order]
    cnt = 0
    def rec(k, used):
        nonlocal cnt
        if k == m: cnt += 1; return
        for v in E2[k]:
            if not (used >> v) & 1: rec(k + 1, used | (1 << v))
    rec(0, 0)
    return cnt
for ci, l in enumerate(x for x in open(sys.argv[1]) if x.startswith('FOUND:')):
    E = parse(l); n = 1 + max(max(e) for e in E); t0 = time.time()
    print(ci, n, len(E), count(E, n), round(time.time() - t0, 1), flush=True)
