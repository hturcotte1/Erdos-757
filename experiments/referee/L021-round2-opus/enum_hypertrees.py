"""Independent enumeration of cell(27,13,9,3): connected members of C with n=27, m=13,
tau=9, Delta<=3. A connected 3-graph with n = 2m+1 is a (Berge-acyclic, linear)
hypertree; hypertrees have the Koenig property, so tau = 9 = n/3 means a perfect
matching M (9 'blocks'); the other 4 edges ('connectors') meet 3 distinct blocks each,
and H is connected iff the block-level 3-graph (9 nodes, 4 edges) is connected, i.e. a
hypertree. Delta<=3: each block vertex lies on <= 2 connectors. Up to isomorphism only
the partition of the connectors at a block into vertex classes (<= 3 classes of size
<= 2) matters. Here all block-level hypertrees are grown edge by edge, all partitions
are enumerated, and the resulting graphs are reduced to isomorphism classes; each class
is re-checked (tau by branching, linear, Delta, perfect matching unique) and compared
with the 18 graphs of experiments/20261027-0730-kt-cells/lists/cell_27_13_9_D3.txt.
(Membership in C is automatic for hypertrees: no Berge cycle, so no F7 and (P3).)"""
import re, sys, time
from itertools import product
import networkx as nx
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rlib import tau, is_linear, degrees, is_connected, p3_ok, iso, inc_graph

ROOT = "/home/user/Erdos-757/"
t0 = time.time()


def set_partitions_cap(items, maxparts=3, cap=2):
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions_cap(rest, maxparts, cap):
        for i in range(len(p)):
            if len(p[i]) < cap:
                yield p[:i] + [p[i] + [first]] + p[i + 1:]
        if len(p) < maxparts:
            yield p + [[first]]


# grow block-level hypertrees: connector 0 on blocks (0,1,2); connector j attaches at one
# existing block and adds two new blocks
shapes = []
def grow(conns, nb):
    if len(conns) == 4:
        shapes.append(list(conns))
        return
    for b in range(nb):
        conns.append((b, nb, nb + 1))
        grow(conns, nb + 2)
        conns.pop()
grow([(0, 1, 2)], 3)
print("labeled block-level growth sequences:", len(shapes))

classes = {}   # wl-hash -> list of edge lists
nbuilt = 0
for conns in shapes:
    inc = {b: [j for j, c in enumerate(conns) if b in c] for b in range(9)}
    per_block = [list(set_partitions_cap(inc[b])) for b in range(9)]
    for choice in product(*per_block):
        # vertex of block b used by connector j
        slot = {}
        for b in range(9):
            for k, part in enumerate(choice[b]):
                for j in part:
                    slot[(b, j)] = 3 * b + k
        E = [(3 * b, 3 * b + 1, 3 * b + 2) for b in range(9)]
        for j, c in enumerate(conns):
            E.append(tuple(sorted(slot[(b, j)] for b in c)))
        nbuilt += 1
        G = inc_graph(E)
        h = nx.weisfeiler_lehman_graph_hash(G, node_attr=None, iterations=5)
        lst = classes.setdefault(h, [])
        if not any(iso(E, F) for F in lst):
            lst.append(E)
reps = [E for lst in classes.values() for E in lst]
print("structures built:", nbuilt, "isomorphism classes:", len(reps), f"[{time.time()-t0:.0f}s]")

ok = True
for E in reps:
    n = 27
    good = (len(E) == 13 and is_linear(E) and max(degrees(n, E)) <= 3 and is_connected(n, E)
            and tau(n, E) == 9 and p3_ok(E))
    ok &= good
print("every class: linear, connected, Delta<=3, tau=9, (P3):", ok)

stored = []
for line in open(ROOT + "experiments/20261027-0730-kt-cells/lists/cell_27_13_9_D3.txt"):
    if line.startswith("FOUND:"):
        stored.append([tuple(int(x) for x in g.split(",")) for g in re.findall(r"\(([^)]*)\)", line)])
match = [sum(1 for E in reps if iso(E, F)) for F in stored]
print("stored graphs:", len(stored), "each matched by exactly one class:", all(x == 1 for x in match))
print("ALL OK" if ok and len(reps) == len(stored) == 18 and all(x == 1 for x in match) else "MISMATCH",
      f"[{time.time()-t0:.0f}s]")
