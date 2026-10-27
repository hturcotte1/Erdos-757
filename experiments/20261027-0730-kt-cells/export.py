"""Export the new cells to lists/cell_<n>_<m>_<t>_D3.txt (count header + FOUND lines) and write progress.tsv (with decompositions)."""
import ast, glob, re, hashlib
rows = []
for key in ['25,14,9,3', '26,17,10,3', '27,13,9,3', '27,20,11,3']:
    n, m, t, D = map(int, key.split(','))
    p = f'out/cells/cell_{n}_{m}_{t}_D{D}.txt'
    txt = open(p).read().splitlines()
    found = [l for l in txt if l.startswith('FOUND')]
    info = ast.literal_eval(re.search(r'INFO (.*)', [l for l in txt if l.startswith('INFO')][0]).group(1).replace('true', 'True').replace('false', 'False')) if False else None
    infol = [l for l in txt if l.startswith('INFO')][0][5:]
    import json
    try: info = json.loads(infol)
    except Exception: info = ast.literal_eval(infol)
    out = f'lists/cell_{n}_{m}_{t}_D3.txt'
    body = '\n'.join(found) + ('\n' if found else '')
    open(out, 'w').write(f'# cell({n},{m},{t},3): {len(found)} classes (connected members of C, Delta<=3, one canonical rep per isomorphism class); '
                         f'engine L012/L016 (see PROVENANCE.md)\n' + body)
    brs = info['branches']
    inputs = sum(b['inputs'] for b in brs); nodes = sum(b['ext']['nodes'] for b in brs)
    decs = '; '.join(f"d={b['d']},tp={b['tp']},S'={b['Sp']}:{b['decompositions']}dec/{b['inputs']}in" for b in brs)
    rows.append((f'({n},{m},{t},3)', len(found), inputs, nodes, info.get('secs'), decs, 'OWN out/cells (own run, own CELLDIR)', out))
with open('progress.tsv', 'w') as f:
    f.write('cell\tclasses\tinputs\tnodes\tseconds\tdecompositions(per branch)\tlist provenance\texport\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
print(open('progress.tsv').read())
