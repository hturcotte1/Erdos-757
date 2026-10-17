"""Collect every cell file of out/cells (n=23 and n=24 runs) into cells_table.tsv and results.json."""
import os, re, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
def table(d):
    rows = []
    for p in glob.glob(os.path.join(d, 'cell_*.txt')):
        m = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt', os.path.basename(p)); key = tuple(map(int, m.groups()))
        L = open(p).read().splitlines(); cls = sum(1 for l in L if l.startswith('FOUND:'))
        info = json.loads([l for l in L if l.startswith('INFO ')][0][5:])
        bad = sum(b.get('ext', {}).get('bad_tau', 0) for b in info.get('branches', []))
        rows.append(dict(cell=key, classes=cls, route=info['route'], secs=info['secs'], bad_tau=bad))
    return sorted(rows, key=lambda r: (-r['cell'][0], r['cell']))
if __name__ == '__main__':
    rows = table(os.path.join(HERE, 'out', 'cells'))
    with open('cells_table.tsv', 'w') as f:
        f.write('n\tm\ttau\tDelta\tclasses\troute\tsecs\tbad_tau\n')
        for r in rows: f.write('\t'.join(map(str, list(r['cell']) + [r['classes'], r['route'], r['secs'], r['bad_tau']])) + '\n')
    top = [json.loads(l) for l in open('results_cells.jsonl')]
    print(len(rows), 'cells; total bad_tau', sum(r['bad_tau'] for r in rows), '; recursion cells', sum(r['route'] == 'recurse' for r in rows))
    print('top-level', [(t['cell'], t['classes'], t['secs']) for t in top])
