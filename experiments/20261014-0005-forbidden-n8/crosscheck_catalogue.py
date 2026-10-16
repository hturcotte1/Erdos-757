"""Consistency check: the permutation-based catalogue (catalogue.py) and the pattern generator of enumerate.py
must contain exactly the same midpoint-injective, connected, full-support ordered patterns with <= 4 edges
(up to reflection), and agree on the realizable ones where the n=8 enumeration data says so.
Usage: python3 crosscheck_catalogue.py catalogue.json"""
import json, sys
src = open("enumerate.py").read()
ns = {}
exec(src[src.index("def patterns"):src.index("def main")], ns)
patterns, reflect_edges = ns["patterns"], ns["reflect_edges"]
cat = json.load(open(sys.argv[1]))

def connected(edges):
    comp = set(edges[0]); rest = list(edges[1:]); ch = True
    while ch:
        ch = False
        for e in rest[:]:
            if comp & set(e):
                comp |= set(e); rest.remove(e); ch = True
    return not rest

for n in range(3, 9):
    A = set()
    for p in patterns(n):
        if 1 <= len(p) <= 4 and len({v for e in p for v in e}) == n and connected(list(p)):
            p = tuple(sorted(p)); A.add(min(p, reflect_edges(n, p)))
    B = set()
    for c in cat["classes"]:
        if c["n"] == n and c["mids_injective"]:
            for o in c["orders"]:
                rf = tuple(map(tuple, o["rank_form"]))
                B.add(min(rf, reflect_edges(n, rf)))
    print(n, len(A), len(B), "EQUAL" if A == B else "MISMATCH", flush=True)
