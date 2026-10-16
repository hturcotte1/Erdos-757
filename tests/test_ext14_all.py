"""Regression test for L005 (experiments/20261015-2340-ext14-all): re-run the per-class routine on classes 0 and 2440."""
import gzip, importlib.util, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXP = os.path.join(ROOT, 'experiments', '20261015-2340-ext14-all')


def _load():
    spec = importlib.util.spec_from_file_location('extend_all', os.path.join(EXP, 'extend_all.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _stored(idx):
    for line in open(os.path.join(EXP, 'results.jsonl')):
        r = json.loads(line)
        if r['class'] == idx: return r
    raise KeyError(idx)


def _census(idx):
    with gzip.open(os.path.join(ROOT, 'data', 'census_n14_m12_classes.jsonl.gz'), 'rt') as f:
        for i, line in enumerate(f):
            if i == idx: return json.loads(line)['set']


def test_rerun_classes_0_and_2440():
    E = _load()
    for idx in (0, 2440):
        S = _census(idx)
        r = E.process((idx, S))
        st = _stored(idx)
        assert r['set'] == st['set'] == S
        for k in ('hA', 'n_max_sidon', 'Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_lines', 't2_isect_pts',
                  't2_isect_45', 'min_h', 'n_2ext', 'hist', 't2_line_h'):
            assert r[k] == st[k], (idx, k, r[k], st[k])
        assert r['min_h'] == 10 and r['records'] == []
        assert r['hA'] == 8 and r['t2_precheck'] is False


def test_abase_acceptance_numbers():
    # class 2440 is A_base; numbers of the L001 / L005 acceptance
    E = _load()
    S = _census(2440)
    assert S == [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    r = E.process((2440, S))
    assert r['Px_size'] == 223 and r['n_single_45'] == 50
    assert r['n_t1b_45'] == 1743 and r['t2_lines'] == 42 and r['t2_line_h'] == [10]
    assert r['n_max_sidon'] == 143 and r['t2_isect_45'] == 0
    assert r['t1_pairs'] == 11774 and r['t2_isect_pts'] == 498
