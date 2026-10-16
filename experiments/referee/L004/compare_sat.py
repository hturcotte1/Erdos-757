"""Referee L004: compare SAT enumeration output(s) with the census, cube by cube (own code).
usage: python3 compare_sat.py CENSUS_KEYS.gz PREFIXES.txt RESULTS_DIR SATOUT1.gz [SATOUT2.gz ...]
For each enumerated cube c (all models with the given triples at midpoints 1,2,3, F7 allowed):
  A(c) = {labelled pattern P in my output for c : P F7-free and P canonical (P <= refl P)}
  B(c) = census prefix file for c (if c is a census prefix), else empty
  require A(c) == B(c);
  every F7-free non-canonical P in my output: orbit key must be in the census key set;
  F7-containing models: counted and written to f7_models.txt.gz for realization.
Uses ./pchk for F7, canonical form and alpha (alpha must be <= 8 for every SAT model: sanity check of the CNF)."""
import gzip, json, os, subprocess, sys, collections

KEYS, PREF, RES = sys.argv[1], sys.argv[2], sys.argv[3]
outs = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
census_keys = set()
for l in gzip.open(KEYS, "rt"):
    census_keys.add(l.split()[0])
pl = open(PREF).read().split()
pidx = {p: q for q, p in enumerate(pl)}

models = collections.defaultdict(list); cube_done = {}
for f in outs:
    for l in gzip.open(f, "rt"):
        if l.startswith("# cube"):
            w = l.split(); cube_done[w[2]] = int(w[4]); continue
        if l.startswith("#"): continue
        w = l.split(); models[w[0]].append(" ".join(w[1:]))
allm = [(c, m) for c, ms in models.items() for m in ms]
p = subprocess.run([os.path.join(HERE, "pchk"), "14"], input="".join("%s %s\n" % (c.replace(",", "/"), m.replace(";", " ")) for c, m in allm),
                   capture_output=True, text=True, check=True)
info = collections.defaultdict(list)
alph = collections.Counter()
for l in p.stdout.splitlines():
    f = l.split()
    c, sat, lin, k30, f7, al, canon, sy, key, own = f[0].replace("/", ","), *map(int, f[1:8]), f[8], f[9]
    assert sat and lin and k30, l
    alph[al] += 1
    info[c].append((f7, canon, key, own))
prob = collections.Counter(); stats = collections.Counter()
f7out = gzip.open(os.path.join(HERE, "f7_models_%s.txt.gz" % os.path.basename(outs[0]).split(".")[0]), "wt")
for c, ncount in cube_done.items():
    rows = info.get(c, [])
    assert len(rows) == ncount, (c, len(rows), ncount)
    A = set(own for f7, canon, key, own in rows if not f7 and canon)
    B = set()
    if c in pidx:
        stats["census_cubes"] += 1
        dn = json.load(open(os.path.join(RES, "n14_m12_prefix_%05d.done" % pidx[c])))
        nf7free = sum(1 for f7, _, _, _ in rows if not f7)
        if nf7free != int(dn["leaves"]):
            prob["leaves_mismatch"] += 1
            print("LEAVES MISMATCH", c, nf7free, dn["leaves"])
        with gzip.open(os.path.join(RES, "n14_m12_prefix_%05d.jsonl.gz" % pidx[c]), "rt") as g:
            for line in g:
                es = sorted(tuple(e) for e in json.loads(line))
                B.add(";".join("%d,%d,%d" % e for e in es))
    else:
        stats["noncensus_cubes"] += 1
        if any(not f7 for f7, _, _, _ in rows): prob["noncensus_cube_with_f7free_model"] += 1
    if A != B:
        prob["cube_mismatch"] += 1
        print("MISMATCH", c, "mine-census", len(A - B), "census-mine", len(B - A))
    for f7, canon, key, own in rows:
        if f7:
            stats["f7_models"] += 1; f7out.write(own.replace(";", " ") + "\n")
        elif canon:
            stats["f7free_canon"] += 1
        else:
            stats["f7free_noncanon"] += 1
            if key not in census_keys: prob["noncanon_reflection_missing"] += 1
f7out.close()
print("alpha histogram of SAT models", dict(alph))
print("cubes", len(cube_done), dict(stats))
print("PROBLEMS", dict(prob))
