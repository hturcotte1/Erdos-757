import difflib, re, sys
a = open(sys.argv[1]).read().splitlines()
b = open(sys.argv[2]).read().splitlines()
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    print(f"=== {tag} old lines {i1+1}-{i2} -> new lines {j1+1}-{j2}")
    old = "\n".join(a[i1:i2]); new = "\n".join(b[j1:j2])
    # token-level diff (split on spaces)
    ta = re.split(r'(\s+)', old); tb = re.split(r'(\s+)', new)
    s2 = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    for t2, p1, p2, q1, q2 in s2.get_opcodes():
        if t2 == 'equal':
            continue
        ctx_before = "".join(ta[max(0,p1-12):p1])
        print(f"  [{t2}] ...{ctx_before[-90:]!s}")
        if p2 > p1: print(f"     OLD: {''.join(ta[p1:p2])}")
        if q2 > q1: print(f"     NEW: {''.join(tb[q1:q2])}")
