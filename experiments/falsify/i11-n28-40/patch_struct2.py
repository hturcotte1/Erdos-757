s=open('structure.py').read()
a=s.index("    found = None")
b=s.index("    rows.append(")
new='''    found = None
    for h in (1, 2, 3):
        lines = []; owner = []
        for H in itertools.combinations(range(n), h):
            cs = comps_after(n, es, set(H))
            if not cs: continue
            for ce in cs:
                vs = sorted(set(v for e in ce for v in e)); mp = {v: i for i, v in enumerate(vs)}
                lines.append(line(len(vs), [tuple(mp[v] for v in e) for e in ce])); owner.append(H)
        res = run_eval(lines)
        byH = collections.defaultdict(list)
        for H, r in zip(owner, res): byH[H].append(r)
        for H, rs in byH.items():
            if all(r[3] <= 1 for r in rs): found = (h, H, sorted((r[0], r[1], r[2], r[3]) for r in rs)); break
        if found: break
'''
s=s[:a]+new+s[b:]
open('structure.py','w').write(s)
