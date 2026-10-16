"""Regression test for L006 (experiments/20261016-0330-ext12-all): re-run the per-class routine on two stored
classes of the 54,243 extremal 12-point classes (the first two stored rows; the census stores its own affine
representatives, so the known record sets are not literally present)."""
import gzip, importlib.util, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXP = os.path.join(ROOT, 'experiments', '20261016-0330-ext12-all')


def _load():
    spec = importlib.util.spec_from_file_location('extend12_all', os.path.join(EXP, 'extend12_all.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _rows():
    rows, n = [], 0
    with gzip.open(os.path.join(ROOT, 'data', 'ext12_all_rows.jsonl.gz'), 'rt') as f:
        for line in f:
            n += 1
            if len(rows) < 2: rows.append(json.loads(line))
    return rows[0], rows[1], n


def test_rerun_two_classes():
    E = _load()
    first, third, n = _rows()
    assert n == 54243
    for st in (first, third):
        r = E.process((st['class'], st['set']))
        for k in ('hA', 'n_max_sidon', 'Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_lines', 't2_isect_pts',
                  't2_isect_45', 'min_h', 'n_2ext', 'hist', 't2_line_h'):
            assert r[k] == st[k], (st['class'], k, r[k], st[k])
        assert r['hA'] == 7 and r['min_h'] == 9 and r['records'] == [] and r['t2_precheck'] is False
        assert r['t2_lines'] == 36 and r['t2_line_h'] == [9]
