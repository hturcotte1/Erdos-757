import difflib, sys
old = open(sys.argv[1]).read().split('\n')
new = open(sys.argv[2]).read().split('\n')
assert len(old) == len(new)
for i, (a, b) in enumerate(zip(old, new), 1):
    if a == b:
        continue
    print(f"===== line {i} =====")
    aw, bw = a.split(' '), b.split(' ')
    sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        ctx_l = ' '.join(aw[max(0, i1-6):i1])
        ctx_r = ' '.join(aw[i2:i2+6])
        print(f"  [{op}] ...{ctx_l}")
        if i2 > i1:
            print(f"     - {' '.join(aw[i1:i2])}")
        if j2 > j1:
            print(f"     + {' '.join(bw[j1:j2])}")
        print(f"     ...{ctx_r}")
